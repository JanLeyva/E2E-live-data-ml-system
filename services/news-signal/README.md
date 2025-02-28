# News Signal Service

This service does 3 things
1. Get news data from Kafka topic.
2. Calls LLM to get the signal about the new. Example structure output:
```json
{"coin": "BTC", "signal": 1},
{"coin": "ETH", "signal": 1},
{"coin": "XRP", "signal": -1},
```
3. Upload singal to the Kafka topic.

Note: You can choose between two LLM Ollama (fine-tuned locally LLM) and Cloude, REST API calls to Anthropic Claude model.


## Finetune Open Source LLM

In this project we finetuned llama3.3 1b, actually we used the quantized to speed up the training [`unsloth/Llama-3.2-1B-bnb-4bit`](https://huggingface.co/unsloth/Llama-3.2-1B-bnb-4bit). The script to finetune the LLM is here:
- `services/news-signal/finetune_src/fine_tuning.py`
It follows this steps:
1. Logging to CometML our model register and experiment tracking.
1. download model and tokenizer.
1. add lora adapters.
1. load and split dataset.
1. finetune the model.
1. quantize the model to be used with Ollama.
1. Upload the model to [HuggingFace](https://huggingface.co).

This can be run using the `Makefile`:
```bash
make fine-tune
```

To finetune the LLM and quantize it we use [Unsloth](https://unsloth.ai) an open source library that trains LLM x30 faster with less memory usage.

Note: in case it fails to create the `Modelfile` to be use in Ollama, find below an example for our template:

```bash
FROM hf.co/JanLilan/llama-3-2-1b-news-signals-ollama:latest

TEMPLATE """You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
Analyze the following news story and determine its potential impact on crypto asset prices.
Focus on both direct mentions and indirect implications for each asset.

Do not output data for a given coin if the news is not relevant to it.

## Example input
Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP

## Example output
[
    {"coin": "BTC", "signal": 1},
    {"coin": "ETH", "signal": 1},
    {"coin": "XRP", "signal": -1},
]

### Instruction:
{{ .Prompt }}

{{ .end }}### Response:
{{ .Response }}<|end_of_text|>"""


PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|eao_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|end_of_text|>"
PARAMETER stop "<|reserved_special_token|>"
```

Note: we did the finetune in [Lambda](https://lambdalabs.com/?srsltid=AfmBOoqWtAJut4mVEd3kuNlAtQnRrURsZFU-9oXme9moDxfuM7ee__18), the cost to finetune a 1b model is less than 5$.

### Setup

1. This service depends on 5 enviorament variables that are read in `config.py`.

```python
kafka_broker_address: str # redpanda adress
kafka_input_topic: str # Kafaka news service topic
kafka_output_topic: str # Kafka output topic
kafka_consumer_group: str # same consumer group as news service
model_provider: Literal['anthropic', 'ollama', 'dummy'] # choose model to run
data_source: Literal['live', 'historical'] # to track the source of the news
```

2. Once the variables are set, you can run any of the `Dockerfile` to run the service. This is a service part of a workflow, for this reason is included in the **Docker compose**:
    - `docker-compose/news-signal-historical.yml`
    - `docker-compose/news-signal-live.yml`

Disclaimer: **Docker compose** is not working currenly as `news-signal` service depends on [Ollama](https://ollama.com) (possible solution, migrate to [vLLM](https://docs.vllm.ai/en/latest/) for inference).

### Depends on

This service depends on Kafka (in this case we run redpanda). You can find a Docker compose to run it locally here: 
- `docker-compose/redpanda.yml` -> running here: `localhost:19092` (locally) `redpanda:9092` (inside docker).
