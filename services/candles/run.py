from datetime import timedelta
from typing import Any, List, Literal, Optional, Tuple

from loguru import logger
from quixstreams.models import TimestampType


def custom_ts_extractor(
    value: Any,
    header: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specify a custom timestamp extractor to use the timestamp from the message playload
    instead of a Kafka timestamp.
    """
    return value['timestamp_ms']


def init_candle(trade: dict) -> dict:
    """
    Initialize a candle with the first trade
    """
    # breakpoint()
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['volume'],
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair'],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Update the candle with the latest trade
    """
    # breakpoint()
    candle['close'] = trade['price']
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['volume'] += trade['volume']
    candle['timestamp_ms'] = trade['timestamp_ms']
    candle['pair'] = trade['pair']
    return candle


def format_sdf(data: dict) -> dict:
    """
    Extract open, high, low, close, volume, timestamp_ms, pair from the dataframe
    and keep only relevant columns.
    Args:
        data: dict containing stream data frame.
    Returns:
        data: dict
    """
    data['open'] = data['value']['open']
    data['high'] = data['value']['high']
    data['low'] = data['value']['low']
    data['close'] = data['value']['close']
    data['volume'] = data['value']['volume']
    data['timestamp_ms'] = data['value']['timestamp_ms']
    data['pair'] = data['value']['pair']

    # Extract window start and end timestamps
    data['window_start_ms'] = data['start']
    data['window_end_ms'] = data['end']

    # keep only the relevant columns
    return data[
        [
            'pair',
            'timestamp_ms',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'window_start_ms',
            'window_end_ms',
        ]
    ]


def main(
    kafka_broker_adress: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
    emit_incomplete_candles: bool,
    data_source: Literal['live', 'historical', 'test'],
):
    """
    3 steps:
        1. Integrate trades from Kafka
        2. Generate candles using tumbling windows and
        Output Candles Kandles
        3. Output candles to Kafka

    Args:
        kafka_broker_adress (str): Kafka broker adress
        kafka_input_topic (str): Kafka input topic
        kafka_output_topic (str): Kafka output topic
        kafka_consumer_group (str): Kafka consumer group
        candle_seconds (int): Candles seconds
        emit_incomplete_candles (bool): Emit incomplete candles or just the final one
        data_source (Literal['live', 'historical', 'test']): Data source
    Returns:
        None
    """
    logger.info('Init candles services!')

    from quixstreams import Application

    # Initializate Quix strams application
    app = Application(
        broker_address=kafka_broker_adress,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='latest' if data_source == 'live' else 'earliest',
    )

    # Define the input and ouput topics
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        timestamp_extractor=custom_ts_extractor,
    )

    output_topic = app.topic(
        name=kafka_output_topic,
        value_deserializer='json',
    )

    # Create a straming DataFrame from the input topic
    sdf = app.dataframe(topic=input_topic)

    # Define the tumbling windows
    sdf = (
        # Define the tumbling windows
        sdf.tumbling_window(timedelta(seconds=candle_seconds))
        # Create a "reduce" aggregation with "reducer" and "initializer" functions
        .reduce(reducer=update_candle, initializer=init_candle)
    )

    # Extract open, high, low, close, volume, timesstamp_ms, pair from the dataframe
    if emit_incomplete_candles:
        # Emit all intermediate candles to make the system more responsive
        sdf = sdf.current()
    else:
        # Emit only the final candle
        sdf = sdf.final()

    sdf = format_sdf(sdf)

    sdf['candle_seconds'] = candle_seconds

    # debugged "bug", we need to log our data, for this reason we were not seeing it in Kafka
    sdf = sdf.update(
        lambda value: logger.info(f'Candle value: {value}')
    )  # OR, sdf.print()
    # sdf = sdf.update(lambda value: breakpoint())

    # push the candle to the Kafka topic
    sdf = sdf.to_topic(topic=output_topic)

    # start the application
    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_adress=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
        emit_incomplete_candles=config.emit_incomplete_candles,
        data_source=config.data_source,
    )
