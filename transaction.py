"""记录一笔交易
通过更改交易信息，向所有节点发送记录交易请求
"""

import requests

# 设置超时时间为2秒
timeout = 2
# 配置节点信息
node1 = 'http://10.2.29.126:5000/'    # 矿工1 911台式机
node2 = 'http://10.2.29.165:5000/'    # 矿工2 902台式机
node3 = 'http://10.2.29.240:5000/'    # 矿工3 我的 macbook
all_nodes = {node1, node2, node3}

# 交易信息
data = {
    'from': 'dsdscdsce23f23ffdscdscds',
    'to': 'dscwevervfevbgrtbtrgverc2',
    'amount': 6
}

# 把一笔交易同时发给所有节点（矿工）来记录, POST请求
for node_url in all_nodes:
    try:
        response = requests.post(node_url+'txion', json=data, timeout=timeout)
        print('节点{}返回交易结果如下: '.format(node_url))
        print(response.status_code)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print("节点{}连接失败, 该节点不记录交易: ".format(node_url))
        # print(e)
