"""snakecoin 矿工服务端代码
√ 1、提供交易记录功能
√ 2、提供挖矿功能
√ 3、提供账本查询功能
× 4、没有实现钱包功能
"""

# ref:https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d
# ref:https://www.liaoxuefeng.com/wiki/1207298049439968/1311929706479649

# 什么叫挖矿？
## Proof-of-Work
# 怎么体现分布式，去中心化？
## 共识算法
# 一个区块能够存储多大的数据？
## 理论上多大都行，因为哈希是任意长输入映射到固定长输出

from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
from colorama import Fore
import pickle

node = Flask(__name__)


# 定义 Snakecoin 区块结构体
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

# 生成创世块
def create_genesis_block():
    # 手动构建一个 index 为 0、previous_hash 为 0 的块
    return Block(0, date.datetime.now(), {
        "proof-of-work": 9,
        "transactions": None
    }, "0")


# 配置信息和变量定义
# 本矿工的ip
my_node = 'http://10.2.29.126:5000/'  # 修改成当前电脑ip
# 本矿工地址
miner_address = "miner_winOFFICE"
# 所有矿工的ip
node1 = 'http://10.2.29.126:5000/'  # 矿工1 911台式机
node2 = 'http://10.2.29.165:5000/'  # 矿工2 我的win笔记本
all_nodes = {node1, node2}
# 其他节点的信息, 902的矿工
peer_nodes = all_nodes.difference({my_node})
# 设置超时时间为2秒
timeout = 2
# 区块链
bc = Blockchain()
bc.blockchain.append(create_genesis_block())
# 该节点的待处理交易
this_nodes_transactions = []


# 处理 POST 请求，处理区块的交易
@node.route('/txion', methods=['POST'])
def transaction():
    # 提取交易数据
    new_txion = request.get_json()
    # 添加交易到待处理列表 this_nodes_transactions 中
    this_nodes_transactions.append(new_txion)
    # 显示提交的交易
    print("New transaction")
    print("FROM: {}".format(new_txion['from'].encode('ascii', 'replace')))
    print("TO: {}".format(new_txion['to'].encode('ascii', 'replace')))
    print("AMOUNT: {}\n".format(new_txion['amount']))
    # 回应客户端交易已提交
    return "Transaction submission successful\n"


# 处理 GET 请求，返回区块链的信息
@node.route('/blocks', methods=['GET'])
def get_blocks():
    # 处理成 JSON 格式
    blocks = []
    for block in bc.blockchain:
        blocks.append({
            "index": block.index,
            "timestamp": str(block.timestamp),
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    chain_to_send = json.dumps(blocks, indent=2)
    chain_to_send_object = pickle.dumps(bc.blockchain)
    return chain_to_send_object


# 获取其他节点的数据
def find_new_chains():
    # 用 GET 请求获取每个节点的区块链
    other_chains = []
    for node_url in peer_nodes:
        # 使用try避免一个节点（矿工）没开机，网络请求失败把自己搞崩
        try:
            block = requests.get(node_url + "/blocks", timeout=timeout)
            # 将 JSON 格式转成 Python 字典
            block = pickle.loads(block.content)
            # 将获取的区块链添加到列表
            other_chains.append(block)
            print('----------已拿到其他矿工账本---------')
        except:
            print('----------没有找到其他矿工-----------')
            pass
    return other_chains


# 实现工作量证明算法，即挖矿的算法
# 返回值能够被9和上一次last_proof整除
def proof_of_work(last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor


# 处理 GET 请求 /mine，用于挖矿
@node.route('/mine', methods=['GET'])
def mine():
    # 获取上一个块的 proof of work
    last_block = bc.blockchain[len(bc.blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    # 找到当前块的 proof of work
    # 注意：程序会在此处被阻塞，直到找到一个新的
    # proof of work
    proof = proof_of_work(last_proof)
    # 当我们找到一个有效的 proof of work
    # 时，我们就知道可以挖出一个新块，因此
    # 我们通过添加交易来奖励挖矿者
    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )
    # 现在我们可以收集所需数据来
    # 创建新的块
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # 清空待处理交易列表
    this_nodes_transactions[:] = []
    # 创建新块
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    print("-------挖到一个币--------")  # 这里应该先跟别人长度对比，再决定是否把自己的加进去

    # 共识算法
    # 获取其他节点的区块链
    other_chains = find_new_chains()
    # 如果我们的区块链不是最长的，则设为最长的区块链
    longest_chain = bc.blockchain
    print("自己账本长度：", len(bc.blockchain))
    for chain in other_chains:
        print("别人的账本长度：", len(chain))
        if len(longest_chain) < len(chain):
            print('---------自己的账本不如别人长----------')
            longest_chain = chain
    # 如果自己是最长的区块或者和别人等长，那么把新挖到的区块添加进去
    if len(bc.blockchain) == len(longest_chain):
        bc.blockchain.append(mined_block)
    # 如果最长的区块链不是我们的，则停止挖矿并将我们的区块链设为其他矿工中最长的
    else:
        bc.blockchain = longest_chain
    print("共识算法后自己账本的长度：", len(bc.blockchain))
    return "okokok\n"


# 运行应用
if __name__ == "__main__":
    # node.run()    # 本机访问，Running on http://127.0.0.1:5000/
    node.run('0.0.0.0', 5000)  # 可以局域网通过IP访问
