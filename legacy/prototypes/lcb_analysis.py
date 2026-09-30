import argparse
import json
from pprint import pformat

import numpy as np
import pandas as pd
from datasets import DatasetDict, load_from_disk
from concurrent.futures import ProcessPoolExecutor

dataset = load_from_disk("data/lcb")

def check(args):
    row = args
    platform = row.get("platform",None)
    return platform,row.get("question_id", -1), row.get("contest_id", -1)
    

def check_dataset(dataset,num_workers = 16):
    args = [dataset[i] for i in range(len(dataset))]
    question_ids = []
    contest_ids = []
    platforms = []
    with ProcessPoolExecutor(max_workers=num_workers) as ex:
        for i,(platform,question_id,contest_id) in enumerate(ex.map(check,args)):
            platforms.append(platform)
            question_ids.append(question_id)
            contest_ids.append(contest_id)
    return np.array(platforms),np.array(question_ids),np.array(contest_ids)

platforms,question_ids,contest_ids = check_dataset(dataset)
# print(f"total number of data:",len(question_ids))
# print("leetcode question ids:", np.count_nonzero(question_ids != '-1'))
# print("leetcode contest ids:", np.count_nonzero(contest_ids != '-1'))

# # print(question_ids[:20])

df = pd.DataFrame({
    "platform":platforms,
    "question_id": question_ids,
    "contest_id": contest_ids,
})
df.to_csv("platform_info.csv")

# print("Example of non leetcode dataset:")
# print(dataset[5].keys())
# print(dataset[5]["question_content"])
# print(dataset[5]["platform"])
# print(dataset[5]["question_id"])


            
            
            
        
        
    
