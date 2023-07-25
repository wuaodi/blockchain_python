"""查询所有矿工的blockchain(账本)
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

# 设置超时时间为2秒
timeout = 2
# 配置节点信息
node1 = 'http://10.2.29.126:5000/'    # 矿工1 winOFFICE
node2 = 'http://10.2.29.165:5000/'    # 矿工2 winAD
all_nodes = {node1, node2}

for node_url in all_nodes:
    try:
        blockchain = requests.get(my_node + 'blocks', timeout=timeout)
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
        print('节点{}返回账本结果如下: '.format(node_url))
        print(blocks_json)

    except requests.exceptions.RequestException as e:
        print("节点{}连接失败, 该节点不返回账本: ".format(node_url))
        # print(e)
