# Trades Service

This service does 2 things:
1. Get the Trades from **kraken API**
    - `data_source`=live: gets live data from sockets API `wss://ws.kraken.com/v2`. 
    -> logic defined: `services/trades/kraken_api/websocket.py` -> `KrakenWebsocketAPI`
    - `data_source`=historical: gets historical data from REST API `https://api.kraken.com/0/public/Trades`. 
    -> logic defined `services/trades/kraken_api/rest.py` -> `KrakenRestAPI`
    - `data_source`=test: gets tests data. 
    -> logic degined `services/trades/kraken_api/mock.py` -> `KrakenMockAPI`
1. Upload to the the data to the Kafka topic.

## Extra: More details

### Setup

1. This service depends on 5 enviorament variables that are read in `config.py`.

```python
    kafka_broker_address: str
    kafka_topic: str
    pairs: List[str]
    data_source: Literal['live', 'historical', 'test']
    last_n_days: Optional[int] = None
```

2. Once the variables are set, you can run any of the `Dockerfile` to run the service. You will see 3 Dockerfile each one is more optimized (naive.Docker < opt.Dockerfile < Dockerfile (multistage)) use the last one for faster cached. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/technical-indicators-historical.yml`
    - `docker-compose/technical-indicators-live.yml`

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).