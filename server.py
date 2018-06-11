# -*- coding utf-8 -*-

from flask import Flask, request, jsonify
from Node import Node

app = Flask(__name__)

my_node = Node()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    获取结点发来的新的交易，
    :return: 交易信息
    """
    transaction = request.get_json()
    required = ['sender', 'signature', 'message']
    msg = ['receiver', 'amount', 'data']
    msg1 = transaction['message']
    if not all(k in transaction for k in required):
        return "Missing values", 400
    if not all(k in msg1 for k in msg):
        return "Missing values", 400
    if my_node.add_new_transaction(transaction):  # ###################
        return "Get transaction successfully !", 201
    else:
        return "Invalid transaction", 400


@app.route("/chain", methods=['GET'])
def send_all_chain():
    """
    根据请求，发送自己的区块链
    :return: 区块链
    """
    response = {"chain": my_node.chain,
                "length": len(my_node.chain)}
    return jsonify(response), 200


@app.route("/consensus", methods=['POST'])
def consensus():
    """
    合约机制，选择最长的链作为主链
    :return: 是否执行合约的消息
    """
    msg = request.get_json()
    chain = msg['chain']
    if my_node.chain.resolve_conflicts(chain):
        return "accept chain", 200
    return "reject chain", 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
