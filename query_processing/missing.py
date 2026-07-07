import random

def missing(example, ratio):
    to_delete = round(len(example["query"])*ratio)

    query = example["query"]
    for i in range(to_delete):
        index = random.randint(0, len(query)-1)
        query = query[:index] + query[index + 1:]
    example["query"]=query
    return example