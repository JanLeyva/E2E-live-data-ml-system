# Candles Service

This service does 3 things:
1. Get the data from Trades Kafk topic (`kafka_input_topic`).
1. Calculate the candle for each currency and the windows defined in `candle_seconds`.
1. Upload the candles to the Kafka topic (`kafka_output_topic`)

In this case data_source is just informative as all the sources must be calculated equal.

## Extra: More details

### Setup

1. This service depends on 7 enviorament variables that are read in `config.py`.

```python
    kafka_broker_address: str # redpanda:19092
    kafka_input_topic: str # trades kafka topic
    kafka_output_topic: str # candles output kafka topic
    kafka_consumer_group: str # consumer group shared for this workflow
    candle_seconds: int # seconds to calculate candles
    data_source: Literal['live', 'historical', 'test']
    emit_incomplete_candles: Optional[bool] = True
```

2. Once the variables are set, you can run `Dockerfile` to run the service. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/technical-indicators-historical.yml`
    - `docker-compose/technical-indicators-live.yml`

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).
