import os
from datasets import load_from_disk
from datasets import Dataset
from .process import process

async def get_predictions(base_dir, save_dir, process_fn): 
    for base_datasets in os.listdir(base_dir):
        base_datasets_path = f"{base_dir}/{base_datasets}"
        save_datasets_path = f"{save_dir}/{base_datasets}"
        for dataset in os.listdir(base_datasets_path):
            base_dataset_path = f"{base_datasets_path}/{dataset}"
            save_dataset_path = f"{save_datasets_path}/{dataset}"
            if os.path.isdir(save_dataset_path):
                continue
            
            loaded_dataset = load_from_disk(base_dataset_path)
            
            results = await process(loaded_dataset, base_dataset_path, process_fn)
    
            results.sort(key=lambda r: r["id"])
            
            hf_dataset = Dataset.from_list(results)
            
            hf_dataset.save_to_disk(save_dataset_path)