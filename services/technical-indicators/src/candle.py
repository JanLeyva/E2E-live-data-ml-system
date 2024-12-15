from config import config
from loguru import logger
from quixstreams import State

MAX_CANDLES_IN_STATE = config.max_candles_in_state


def update_candles(
    candle: dict,
    state: State,
):
    """
    Updates the list of candles we have in our state using the latest candle
    If it corresponds to the lat windows, we replace the last candle in the list

    Args:
        candle (dict):
        state (State):
    Returns:
        (dict):
    """
    candles = state.get('candles', default=[])
    if not candles:
        # If the state is empty, we just append the latest candle to the list
        candles.append(candle)
    elif same_window(candle, candles[-1]):
        # Replace the last candle in the list with the latest candle
        candles[-1] = candle
    else:
        # Append the latest candle to the list
        candles.append(candle)

    # If the total number of candles in the state is greater than the maximum number of
    # candles we want to keep, we remove the oldest candle from the list
    if len(candles) > MAX_CANDLES_IN_STATE:
        candles.pop(0)

    # TODO: we should check the candles have no missing windows
    # This can happen for low volume pairs. In this case, we could interpoalte the missing windows

    logger.debug(f'Number of candles in state for {candle["pair"]}: {len(candles)}')

    # Update the state with the new list of candles
    state.set('candles', candles)

    return candle


def same_window(candle: dict, last_candle: dict) -> bool:
    """
    Check if the current candle are in the same windows last candle

    Args:
        candle (dict): the current candle
        last_candle (dict): last candle saved
    Returns:
        True if current candle equal last candle False otherwise
    """
    return (
        candle['window_start_ms'] == last_candle['window_start_ms']
        and candle['window_end_ms'] == last_candle['window_end_ms']
        and candle['pair'] == last_candle['pair']
    )
