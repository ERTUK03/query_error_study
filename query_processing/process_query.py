def process_query(dataset, configs):
    for config in configs:
        for ratio in config["ratios"]:    
            processed_dataset = dataset.map(
                config["mapping"], 
                fn_kwargs={
                    "ratio": ratio
                },
                batched=False
            )
            
            processed_dataset.save_to_disk(f"datasets/raw_datasets/{config['mapping'].__name__}/ratio_{str(ratio)}")