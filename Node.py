# -*- coding utf-8 -*-

from utils import *
import json
import os
import requests
from urllib.parse import urlparse
from time import time
from block import Block
from blockchain import BlockChain


class Node(object):
    def __init__(self):
        self.chain = BlockChain()  # 初始情况，默认先查看本地文件
        self.neighbors = set()  # 邻接点
        self.transactions = []  # 交易的集合
        self.new_block = None  # 新的区块，用于挖矿
        self.pk, self.sk = self.get_key()  # 产生结点的公钥和私钥

    @staticmethod
    def get_key():
        """
        获取公钥和私钥，注意字符串和byte之间的转化
        :return: <pk,sk>
        """
        pk = None
        sk = None
        if not os.path.exists('/node_key.json'):  # 不存在就新建
            with open('node_key.json', 'w') as json_file:
                sk = SigningKey.generate(curve=NIST384p)
                pk = sk.get_verifying_key()
                msg = {
                    "pk": str(pk),
                    "sk": str(sk.to_string())
                }
                json_file.write(json.dumps(msg, sort_keys=True))
        else:
            with open('node_key.json') as json_file:  # 存在直接读取
                msg = json_file.read()
                pk = msg['pk'].encode("utf8")  # 转化成bytes
                sk1 = msg['vk'].encode()
                sk = SigningKey.from_string(sk1, curve=NIST384p)
        return pk, sk

    def add_new_neighbor(self, address):
        """
        添加新的邻居结点
        :param address: url地址
        :return: <None>
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc or parsed_url.path:
            self.neighbors.add(address)
        else:
            raise ValueError('Invalid URL')

    def broadcast_transaction(self, transaction):
        """
        向邻接结点广播新的交易
        :return: <None>
        """
        for url in self.neighbors:
            try:
                requests.get(url=url + "/", timeout=0.2)  # 0.2秒的延迟等待，否则就当做掉线处理
                requests.post(url=url + "/transactions/new", data=json.dump(transaction, sort_keys=True))
            except:
                self.neighbors.remove(url)  # 删除掉线的结点
                print(f'node {url} not online !')

    def add_new_transaction(self, transaction):
        """
        根据签名合法性添加新的交易
        :return: <bool>
        """
        pk_string = str(transaction['sender'])
        signature = transaction['signature']
        message = json.dump(transaction['message'], sort_keys=True)
        # 签名正确，而且不是重复的交易
        if is_valid_transaction(pk_string, message, signature) and transaction not in self.transactions:
            self.broadcast_transaction(transaction)
            self.transactions.append(transaction)
            return True
        return False

    def get_new_chain(self):
        """
        对于新上线的结点，需要获得最长的有效的区块链
        :return: <None>
        """
        for url in self.neighbors:
            try:
                reponse = requests.get(url=url + "/chain", timeout=0.2)  # 获取区块链的数据
            except:
                self.neighbors.remove(url)  # 删除掉线的结点
                print(f'node {url} not online !')
                continue
            # length = reponse['length']
            chain = reponse['chain']
            # 最长的有效区块链
            self.chain.resolve_conflicts(chain)

    def mine(self):
        """
        产生新的区块，相当于挖矿
        :return: 新的区块
        """
        nonce = 0
        last_block = self.chain[-1]
        while not proof_of_work(last_block, nonce):
            nonce += 1

        message = {
            "receiver": self.pk,  # 发给自己
            "amount": 1,  # 奖励的数目
            "data": "a new block",  # 一些其他的信息
        }
        transaction = {
            "sender": "0",  # 发送者为0
            "signature": "0",  # 签名为0
            "message": message  # 自定义的消息
        }
        msg = {
            "index": len(self.chain.blocks),
            "time_stamp": time(),
            "previous_hash": last_block.current_hash,
            "nonce": nonce,
            "data": "",
            "transaction": transaction
        }
        block = Block(msg)
        self.chain.add_block(block)
        return block
