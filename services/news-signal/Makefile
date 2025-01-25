fine-tune:
	uv run finetune_src/fine_tuning.py \
		--base_llm_name unsloth/Llama-3.2-1B-bnb-4bit \
		--dataset_path ./data/instruction_dataset_ollama_11k.jsonl \
		--comet_ml_project_name news-signal-extractor \
		--max_steps 100