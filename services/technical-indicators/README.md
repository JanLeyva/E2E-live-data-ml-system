# Technical Indicators Service

This service does 3 things:
1. Ingests candles from the kafka input topic
2. Computes technical indicators
3. Sends the technical indicators to the kafka output topic

## Calculate Indicators

To calculate the technical indicators we use [talib](https://github.com/TA-Lib/ta-lib-python) base on TA-LIB but in Cython instead of SWIG.

## Extra: More details

### Setup

1. This service depends on 5 enviorament variables that are read in `config.py`.

```python
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    max_candles_in_state: int
    candle_seconds: int
    data_source: Literal['live', 'historical', 'test']
```

2. Once the variables are set, you can run any of the `Dockerfile` to run the service. You will see 3 Dockerfile each one is more optimized (naive.Docker < opt.Dockerfile < Dockerfile (multistage)) use the last one for faster cached. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/technical-indicators-historical.yml`
    - `docker-compose/technical-indicators-live.yml`

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).