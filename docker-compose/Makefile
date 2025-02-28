# manage redpanda (kafka)
start-redpanda:
	docker compose -f redpanda.yaml up -d

stop-redpanda:
	docker compose -f redpanda.yaml down

add-one-partition-to-trades-topic:
	docker compose -f redpanda.yaml exec redpanda rpk topic add-partitionss trades --num 1


## Elastic search compose
start-elasticsearch:
	docker compose -f elasticsearch.yaml up -d

stop-elasticsearch:
	docker compose -f elasticsearch.yaml down

# Technical indicators pipeline management
# for live data
build-technical-indicators-live:
	docker compose -f technical-indicators-live.yaml build

start-technical-indicators-live: build-technical-indicators-live
	docker compose -f technical-indicators-live.yaml up -d

stop-technical-indicators-live:
	docker compose -f technical-indicators-live.yaml down

# for historical data
build-technical-indicators-historical:
	docker compose -f technical-indicators-historical.yaml build
	
backfill-technical-indicators: build-technical-indicators-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill with RUN_ID: $(RUN_ID)"
	RUN_ID=$(RUN_ID) docker compose -f technical-indicators-historical.yaml up -d


stop-backfill-technical-indicators: 
	docker compose -f technical-indicators-historical.yaml down

# News signal pipeline management
build-news-signal-live:
	docker compose -f news-signal-live.yaml build

start-news-signal-live: build-news-signal-live
	docker compose -f news-signal-live.yaml up -d

stop-news-signal-live:
	docker compose -f news-signal-live.yaml down


clean-backfill-kakfa-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yaml exec redpanda rpk topic delete -r ".*historical.*"

########################################
## News signal pipeline 
########################################


# for historical data
build-news-signal-historical:
	docker compose -f news-signal-historical.yaml build

backfill-news-signals: build-news-signal-historical
	$(eval RUN_ID := $(shell uuidgen))
	@echo "Starting backfill of news signals with RUN_ID: $(RUN_ID)"
	RUN_ID=$(RUN_ID) docker compose -f news-signal-historical.yaml up -d


