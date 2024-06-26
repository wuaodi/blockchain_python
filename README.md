# blockchain_python
Understand the principle of blockchain by python code (minimum viable product)

使用python代码完成区块链的原理理解，构建最小可用snakecoin

讲解视频： https://www.bilibili.com/video/BV1Y94y1C782/

ref: https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d

ref: https://www.liaoxuefeng.com/wiki/1207298049439968/1311929706479649


**名词说明**

节点 = 矿工

block = 区块

blockchain = 区块链/账本

**使用说明**

在部分或所有节点运行

    1、运行 snakecoin_server.py 矿工服务端代码
    
    2、运行 dig.py 控制本地矿工不断挖矿
    
在局域网中任意地方运行

    3、transaction.py 记录一笔交易
    
在局域网中任意地方运行

    4、inquiry.py 查询所有矿工的账本

**代码功能解释**

snakecoin_server.py 矿工服务端代码

    √ 1、提供交易记录功能

    √ 2、提供挖矿功能

    √ 3、提供账本查询功能

    × 4、没有实现钱包功能

dig.py 控制本地矿工不断挖矿

    当挖到币并通过一致性检验时：

        1、系统会奖励该矿工一个币
    
        2、该矿工会打包所有记录的交易上链
    
    当挖到币未通过一致性检验时：

        使用所有矿工手里最长的账本替代自己的账本，重新开始挖矿

transaction.py 记录一笔交易

    通过更改交易信息，向所有节点（矿工）发送记录交易请求

inquiry.py  查询所有矿工的blockchain(账本)
