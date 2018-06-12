# -*- coding utf-8 -*-

import json
from config import *
import hashlib


class Block(object):
    def __init__(self, dictionary):
        self.index = dictionary['index']  # 当前区块在区块链中的索引位置
        self.time_stamp = dictionary['time_stamp']  # 时间戳
        self.previous_hash = dictionary['previous_hash']  # 前一个区块的哈希值
        self.current_hash = dictionary['current_hash']  # 当前区块的哈希值，注意进行哈希计算的时候，不要把该值作为参数
        self.nonce = dictionary['nonce']  # 挖矿的工作量证明
        self.data = dictionary['data']  # 一些其他的数据
        self.transactions = []  # 交易数据

    def update_self_hash(self):
        self.current_hash = \
            hashlib.sha256((self.hash_parameter()).encode("utf8")).hexdigest()

    def block_to_json(self):
        """
        区块把区块数据转换成字典数据
        :return:<dict> 字典化后的数据
        """
        self.update_self_hash()
        message = {
            'index': self.index,
            'time_stamp': self.time_stamp,
            'previous_hash': self.previous_hash,
            'current_hash': self.current_hash,
            'nonce': self.nonce,
            'data': self.data,
            'transaction': self.transactions
        }
        return message

    def save_self(self):
        """
        存储区块到指定的目录
        :return:<None>
        """
        file_index = str(self.index).zfill(8)  # 方便字典序排列
        # filename = f'{DATA_DICTIONARY}{file_index}.json'
        filename = DATA_DICTIONARY + file_index + '.json'
        with open(filename, 'w') as block_file:
            json.dump(self.block_to_json(), fp=filename, sort_keys=True)

    def hash_parameter(self):
        """
        返回用于哈希计算的参数，注意，不包括self.current_hash
        :return: str
        """
        return str(self.index) + str(self.time_stamp) + str(self.previous_hash) \
               + str(self.nonce) + str(self.data) + str(self.transactions)
