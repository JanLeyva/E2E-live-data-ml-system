run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t technical_indicators:multistage .

run-docker: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		technical_indicators:multistage
