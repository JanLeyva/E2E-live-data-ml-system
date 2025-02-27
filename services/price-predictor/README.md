# Proce Predictior Service

This service does 2 main things:
- Train ML model to predict currency.
- Inference price prediction
    1. Download the model from the model register (CometML).
    1. Get data from feature store (also gets signal from Kafka topic to know when we are pushing new data).
    1. Predict currency.

Note: In order to get a base line we compare the `XGBoost` with a naive model (`DummyModel`).
Note: Model register and the store trhe metrics are save in [CometML](https://www.comet.com/site/).

## Extra: More details

### Setup

1. This service depends on 5 enviorament variables that are read in `config.py`.

* Training
```python
    feature_view_name: str # The name of the feature view
    feature_view_version: int # The version of the feature view
    pair_to_predict: str # The pair to train the model on
    candle_seconds: int # The number of seconds per candle
    prediction_seconds: int # The number of seconds into the future to predict
    pairs_as_features: list[str] # The pairs to use for the features
    technical_indicators_as_features: list[str] # The technical indicators to use for from the technical_indicators feature group
    days_back: int # The number of days to consider for the historical data
    llm_model_name_news_signals: str # The name of the LLM model to use for the news signals
    hyperparameter_tuning_search_trials: Optional[int] # The number of trials to perform for hyperparameter tuning
    hyperparameter_tuning_n_splits: Optional[int] # The number of splits to perform for hyperparameter tuning
    # model registry
    model_status: # The status of the model in the model registry
```

* Inference
```python
    pair_to_predict: str # The pair to train the model on
    candle_seconds: int # The number of seconds per candle
    prediction_seconds: int # The number of seconds into the future to predict
    model_status: Literal['Development', 'Staging', 'Production']  # The status of the model in the model registry that we want to use for inference
    kafka_broker_address: str # The address of the kafka broker
    kafka_input_topic: str # The topic to listen to for candle events
    kafka_consumer_group: str # The consumer group to use for the kafka consumer
    elasticsearch_url: str # The URL of the Elastic Search instance
    elasticsearch_index: str # The index to write the predictions to
```

2. Once the variables are set, you can run any of the `Dockerfile` to run the service. You will see 3 Dockerfile each one is more optimized (naive.Docker < opt.Dockerfile < Dockerfile (multistage)) use the last one for faster cached. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/technical-indicators-historical.yml`
    - `docker-compose/technical-indicators-live.yml`

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).