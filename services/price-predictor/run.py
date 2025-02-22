import os

from loguru import logger

if __name__ == '__main__':
    try:
        mode = os.environ['TRAINING_OR_INFERNCE']
    except KeyError as e:
        raise ValueError('TRAINING_OR_INFERNCE environment variable is not set') from e

    if mode == 'training':
        logger.info('Training mode!')
        from training.training import main

        main()

    elif mode == 'inference':
        logger.info('Inference mode!')
        from inference.inference import main

        main()

    else:
        raise ValueError(
            f'Invalid mode: {mode}. It has to be either "training" or "inference"'
        )
