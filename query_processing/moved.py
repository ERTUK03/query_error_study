import random

def moved(example, ratio):
    to_move = round(len(example["query"])*ratio)

    query = example["query"]
    for i in range(to_move):
        index = random.randint(1, len(query)-2)
        if random.random()>0:
            query = query[:index-1] + query[index] + query[index-1] + query[index + 1:]
        else:
            query = query[:index] + query[index + 1] + query[index] + query[index + 2:]
    example["query"]=query
    return example