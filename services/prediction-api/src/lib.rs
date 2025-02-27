use elasticsearch::{
    Elasticsearch, 
    SearchParts,
    http::transport::Transport,
};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::io::{Error, ErrorKind};

#[derive(Serialize, Deserialize, Debug)]
pub struct PredictionOutput {
    pair: String,
    prediction: f64,
    timestamp_ms: String,
}

pub async fn get_prediction_from_elasticsearch(pair: String) -> Result<PredictionOutput, std::io::Error> {
    // Create a transport to communicate with Elasticsearch
    let transport = match Transport::single_node("http://localhost:9200") {
        Ok(transport) => transport,
        Err(e) => return Err(Error::new(ErrorKind::Other, format!("Failed to create ES transport: {}", e))),
    };
    
    // Create the client with the transport
    let client = Elasticsearch::new(transport);
    
    // Build the search query
    let query = json!({
        "query": {
            "term": {
                "pair": pair
            }
        },
        "sort": [
            { "timestamp_ms": { "order": "desc" } }
        ],
        "size": 1
    });
    
    // Execute the search
    let response = match client.search(SearchParts::Index(&["predictions_index"]))
        .body(query)
        .send()
        .await {
            Ok(resp) => resp,
            Err(e) => return Err(Error::new(ErrorKind::Other, format!("Search failed: {}", e))),
        };
    
    // Parse the response
    let response_body = match response.json::<Value>().await {
        Ok(body) => body,
        Err(e) => return Err(Error::new(ErrorKind::Other, format!("Failed to parse response: {}", e))),
    };
    
    // Extract the hit if available
    if let Some(hit) = response_body["hits"]["hits"].as_array().and_then(|hits| hits.first()) {
        if let Some(source) = hit["_source"].as_object() {
            let prediction_output = PredictionOutput {
                pair: source["pair"].as_str()
                    .ok_or_else(|| Error::new(ErrorKind::InvalidData, "Invalid pair field"))?
                    .to_string(),
                prediction: source["prediction"].as_f64()
                    .ok_or_else(|| Error::new(ErrorKind::InvalidData, "Invalid prediction field"))?,
                timestamp_ms: source["timestamp_ms"].as_str()
                    .ok_or_else(|| Error::new(ErrorKind::InvalidData, "Invalid timestamp_ms field"))?
                    .to_string(),
            };
            return Ok(prediction_output);
        }
    }
    
    // If no results found
    Err(Error::new(ErrorKind::NotFound, format!("No prediction found for pair: {}", pair)))
}