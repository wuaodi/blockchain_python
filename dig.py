"""控制本地矿工不断挖矿
当挖到币并通过一致性检验时：
    1、系统会奖励该矿工一个币
    2、该矿工会打包所有记录的交易上链
当挖到币未通过一致性检验时：
    使用所有矿工手里最长的账本替代自己的账本，重新开始挖矿
"""

import requests
import pickle
import hashlib as hasher
import json

my_node = 'http://localhost:5000/'

class Block:
    # 初始化函数
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    # SHA-256 哈希算法实现
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8')
                   + str(self.timestamp).encode('utf-8')
                   + str(self.data).encode('utf-8')
                   + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.blockchain = []

# 挖矿请求
while True:
    # 开始挖矿，在这里会停留一段时间，直到做完题挖到一个币
    response = requests.get(my_node + 'mine')
    blockchain = requests.get(my_node + 'blocks')
    blockchain = pickle.loads(blockchain.content)

    blocks = []
    for block in blockchain:
        blocks.append({
            "index": block.index,
            "timestamp": str(block.timestamp),
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    blocks_json = json.dumps(blocks, indent=2)
    # print("当前账本", blocks_json)
    print("账本的最后一个区块：", blocks[-1])

