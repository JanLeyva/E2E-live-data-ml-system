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
