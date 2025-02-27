# To Feature Store Service

This service does 2 things:
1. Get the streaming data from Kafka topic.
1. Upload the data to the Feature Store.

## Extra: More details

### Setup

1. This service depends on 5 enviorament variables that are read in `config.py`.

```python
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str

    feature_group_name: str
    feature_group_version: int
    feature_group_primary_keys: list[str]
    feature_group_event_time: str
    feature_group_materialization_interval_minutes: Optional[int] = 15
    data_source: Literal['live', 'historical', 'test']
```

2. Once the variables are set, you can run any of the `Dockerfile` to run the service. You will see 3 Dockerfile each one is more optimized (naive.Docker < opt.Dockerfile < Dockerfile (multistage)) use the last one for faster cached. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/technical-indicators-historical.yml`
    - `docker-compose/technical-indicators-live.yml`

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).
