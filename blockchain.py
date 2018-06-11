# -*- coding utf-8 -*-

from utils import is_valid_chain
from config import *
import json


class BlockChain(object):
    def __init__(self):
        self.blocks = self.get_chain_from_file()

    @staticmethod
    def get_chain_from_file():
        """
        从文件中读取区块链的结构
        :return:
        """
        if not os.path.exists(DATA_DICTIONARY):
            return None
        chain = []
        # 读取目录下所有的数据
        files = os.listdir(DATA_DICTIONARY)
        for file in files:
            file_path = DATA_DICTIONARY + file
            with open(file_path) as json_file:
                block = json.load(json_file)
                chain.append(block)
        return chain

    def save_chain(self):
        """
        整个区块链存储到硬盘中
        :return:<None>
        """
        for b in self.blocks:
            b.save_self()

    def resolve_conflicts(self, blocks):
        """
        出现冲突时，选择最长的有效链
        :return: <bool>
        """
        if is_valid_chain(blocks) and len(blocks) > len(self.blocks):  # 替换
            self.blocks = blocks
            return True
        return False

    @property
    def last_block(self):
        """
        返回最后一个区块
        :return: <block> or <None>
        """
        if len(self.blocks) > 0:
            return self.blocks[-1]
        else:
            raise ValueError('Wrong index')

    def add_block(self, block):
        self.blocks.append(block)

    def find_block_by_index(self, index):
        """
        通过索引找区块
        :param index: 索引值
        :return: <bool> or block
        """
        if 0 <= index < len(self.blocks):
            return self.blocks[index]
        else:
            raise ValueError('Wrong index')

    def find_block_by_hash(self, hash_value):
        """
        通过哈希值找区块
        :param hash_value: 哈希值
        :return: <bool> or block
        """
        for b in self.blocks:
            if hash_value == b.current_hash:
                return b
        raise ValueError('No hash')
