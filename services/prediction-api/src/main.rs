use actix_web::{ web, App, HttpResponse, HttpServer, Responder };
use serde::Deserialize;

use prediction_api::{ get_prediction_from_elasticsearch, PredictionOutput };

async fn health() -> impl Responder {
    println!("Health endpoint was hit");
    HttpResponse::Ok().body("Hey there!")
}


#[derive(Deserialize)]
struct RequestParams {
    pair: String
}

/// Brain of this REST API
/// Steps:
/// 1. Reads for which cryto pair the client wants predictions
/// 2. Fetches the latest predictions for that pair from Elasticsearch
/// 3. Returns the prediction as JSON
async fn predict(args: web::Query<RequestParams>) -> impl Responder {
    println!("The client request price prediction for {}", args.pair);
    
    let prediction_output: Result<PredictionOutput, std::io::Error> = get_prediction_from_elasticsearch(args.pair.clone()).await;

    match prediction_output {
        Ok(output) => {
            HttpResponse::Ok().json(output)
        }
        Err(err) => {
            HttpResponse::InternalServerError().body(format!("Error: {}", err))
        }
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Hello, world!");

    HttpServer::new(|| {
        App::new()
            .route("/health", web::get().to(health))
            .route("/predict", web::get().to(predict))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
