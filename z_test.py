# # -*- coding utf-8 -*-
#
# import os
# import json
# from ecdsa import SigningKey, NIST384p, VerifyingKey
#
# from ecdsa import SigningKey, NIST384p
#
#
# def get_key():
#     """
#     获取公钥和私钥，注意字符串和byte之间的转化
#     :return: <pk,sk>
#     """
#     pk = None
#     sk = None
#     if not os.path.exists('/node_key.json'):  # 不存在就新建
#         with open('node_key.json', 'w') as json_file:
#             sk = SigningKey.generate(curve=NIST384p)
#             pk = sk.get_verifying_key()
#             msg = {
#                 "pk": str(pk),
#                 "sk": str(sk.to_string())
#             }
#             json_file.write(json.dumps(msg, sort_keys=True))
#     else:
#         with open('node_key.json') as json_file:  # 存在直接读取
#             msg = json_file.read()
#             pk = msg['pk'].encode("utf8")  # 转转化成bytes
#             sk1 = msg['vk'].encode()
#             sk = SigningKey.from_string(sk1, curve=NIST384p)
#     return pk, sk
#
#
# def is_valid(vk_string, message, signature):
#     """
#     验证交易是否合法
#     :param vk_string: 公钥的字符串
#     :param message: 消息
#     :param signature: 签名
#     :return: <bool> True合法，False不合法
#     """
#     vk = VerifyingKey.from_string(vk_string, NIST384p)
#     try:
#         print(vk.verify(signature, str(message).encode("utf8")))  # 同意编码格式
#         return True
#     except:
#         return False
#
#
# def make_transaction(sk, message):
#     """
#     加密交易
#     :param sk_string: 私钥，用于签名
#     :param message: 消息
#     :return: 签名
#     """
#     signature = sk.sign(str(message).encode("utf8"))  # 统一编码格式
#     return signature
#
# vk, sk = get_key()
#
# message = "I am a transaction !"
#
# vk_string = vk.to_string()
# sig = make_transaction(sk, message)
# print(type(sig))
#
# if is_valid(vk_string, message+str("ddd"), sig):
#     print("True")
# else:
#     print("False")

# import platform
#
# print(platform.python_version())

from flask import Flask, request, jsonify
from utils import *
from Node import Node

app = Flask(__name__)

my_node = Node()


@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    """
    结点新建一笔交易
    :return:
    """
    message = request.get_json()
    signature = make_transaction(my_node.sk, message)
    transaction = {
        "sender": my_node.pk,
        "signature": signature,
        "message": message
    }
    my_node.broadcast_transaction(transaction)
    my_node.add_new_transaction(transaction)
    return "add transaction !", 200


@app.route('/receive_transaction', methods=['POST'])
def add_transaction():
    """
    获取其他结点的发来交易信息
    :return: 是否添加成功的消息
    """
    transaction = request.get_json()
    if my_node.add_new_transaction(transaction):
        return "Valid transaction", 200
    return "Invalid transaction", 200


@app.route('/mine', methods=['GET'])
def mine():
    """
    向其它结点广播挖矿的消息
    :return:
    """
    block = my_node.mine()
    if my_node.broadcast_new_block(block):
        return str("block info:\n") + jsonify(block), 200
    else:
        return "Network error", 404


@app.route('/get_mined_block', methods=['POST'])
def get_mined_block():
    """
    获取其他结点挖的区块
    :return:
    """
    block = request.get_json()
    if my_node.add_new_block(block):
        return "Ok", 200
    else:
        return "Wrong", 404


@app.route('/save_to_file', methods=['GET'])
def save_file():
    my_node.chain.save_chain()
    return "Save chain to file", 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    my_node.port = port  # 设置端口
    app.run(host='0.0.0.0', port=port)
