from loguru import logger
from quixstreams import Application
from sink import HopsworksFeatureStoreSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    output_sink: HopsworksFeatureStoreSink,
):
    """
    2 things:
    1. Read messages from Kafka topic
    2. Push messages to Feature Store

    """
    logger.info("Hello from to-feature-store!")

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )
    input_topic = app.topic(kafka_input_topic, value_deserializer="json")

    sdf = app.dataframe(input_topic)

    # Do some processing here ...
    # We need to extract the features we want to push to the feature store
    # TODO: Implement
    # Sink data to a CSV file
    # sdf.sink(csv_sink)

    # Sink data to the feature store
    sdf.sink(output_sink)

    app.run()


if __name__ == "__main__":
    from config import config

    hopeworks_sink = HopsworksFeatureStoreSink(
        # Hopeworks credentials
        api_key=config.hopsworks_api_key,
        project_name=config.hopsworks_project_name,
        # Feature group configuration
        feature_group=config.feature_group_name,
        feature_group_verserion=config.feature_group_version,
        feature_group_primary_key=config.feature_group_primary_keys,
        feature_group_event_time=config.feature_group_event_time,
    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        output_sink=hopeworks_sink,
    )
