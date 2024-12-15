# Set up

- we use uv as a package init and manager.
- we use Makefile to record our most common commands.
- We use Docker to run redpanda and we will dockerize all our microservices.


# Lesson 1: 2024.12.02

Build a microservice that ingests live trades from [Kraken API](https://docs.kraken.com/) and pushes them to a Kafka topic. We want a modular design, so you can easily plug different real time data sources.

* We are using redpanda (as a Kafka) as a broker. We have define the first pipeline where we get trade date from Kraken and push it to Kafka topic. This happens here: `services/trades/kraken_api`

What else?
1. Set up redpanda locally, running in a docker-composer.
1. We build a `pydantic_settings` that reads and validate our `.env` file.
1. We used `quixstreams` to push the date to **redpanda**.
1. We build a class `KrakenWebsocketAPI` that connects though websockets to Kraken API and starts getting date (base on the pairs defined in .env).
1. Also, this `KrakenWebsocketAPI` is returning a `Trade` object we have defined, validated by **pydantic**.

# Lesson 2: 2024.12.04

1. container our application with Docker. Write `Dockerfile` Build an `Image` -> Run the `container`.
    There are some strategies to optimize the dockerization:
    - You can cache parts of your image, to avoid re-build every time the whole image.
    - Do a multistage image (e.g. `services/trades/multi.Dockerfile`).
        * What does it means? We first build our image installing all the dependencies that we will need, in this case **uv** (we used it to build our service/app/module/package). Once you have all installed, crates a second image with the just necessaries thing, a minimalist image to run our serice/app.

# Lesson 3: 2024.12.05

1. Today we have fixed the bug of candles (there was no bug, we jsut haven't logged the candles). Also, we have dokarized the candles services.
1. Build the technical indicators services. Where we calculate a banch of indicators from the candles and we upload it to Kafka topic (redpanda) again. To calculate the technical indicators we use [talib](https://github.com/TA-Lib/ta-lib-python).
1. We have started to build the ingest to feature store [hopsworks](https://c.app.hopsworks.ai/account/api)

# Lesson 5: 2024.12.11

wrap up all together in a docker composer. Running the whole historical and live pipeline together. This is composed by 4 services:
1. Trades: get from websocket the latest date for the crypto currency.
1. Candles: calcualte the candles indicator for each currency.
1. Technical indicators: calculate techinical indicators from thoese candles (features).
1. To feature store: we use HopsWorks as a feature store pushing data from redpanda (kafka) to HopsWorks.
