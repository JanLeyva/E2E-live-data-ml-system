# News Service

This service does 2 things:
1. Polls the [Cryptopanic](https://cryptopanic.com) REST API for news and removes duplicate values.
    * In case `data_source`=**live** polls news from Cryptopanic REST API.
    * `data_source`=**historical** gets the news from CSV file from *https://github.com/soheilrahsaz/cryptoNewsDataset/raw/refs/heads/main/CryptoNewsDataset_csvOutput.rar*.
1. Pushes them to a Kafka topic.


## Extra: More details

### Setup

1. This service depends on 5 enviorament variables that are read in `config.py`.

```python
kafka_broker_address: str # redpanda adress
kafka_topic: str # kafka topic to push data
data_source: Literal['live', 'historical']
polling_interval_sec: Optional[int] = 10 # sleep time beetween requests
historical_data_source_url_rar_file: Optional[str] = None # In case data_source=historical 
historical_data_source_csv_file: Optional[str] = None # In case data_source=historical
historical_days_back: Optional[int] = 180 # back days to get news data
api_key: str # Cryptopanic API KEY
```

2. Once the variables are set, you can run any of the `Dockerfile` to run the service. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/news-signal-historical.yml`
    - `docker-compose/news-signal-live.yml`

Disclaimer: **Docker compose** is not working currenly as `news-signal` service depends on [Ollama](https://ollama.com) (possible solution, migrate to [vLLM](https://docs.vllm.ai/en/latest/) for inference).

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).