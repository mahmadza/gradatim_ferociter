#!/anaconda3/bin/python3.7

import boto3
import requests
import uuid
import time
import json
import random

client = boto3.client('kinesis', region_name = 'ap-southeast-1')
partition_key = str(uuid.uuid4())
print(partition_key)

#an infinite loop
while True:
    #grab data from random user generator
    x = requests.get('https://randomuser.me/api/?exc=login')
    data = json.dumps(x.json())
    #call the PutRecord API
    client.put_record(StreamName='MyKinesisStream', Data = data, PartitionKey = partition_key)
    print(data)
    time.sleep(random.uniform(0,1))
    


