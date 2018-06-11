# -*- coding utf-8 -*-
from ecdsa import SigningKey, NIST384p, VerifyingKey
import hashlib
from config import *


def generate_key():
    """
    产生公钥和私钥
    :return: 二者组合
    """
    sk = SigningKey.generate(curve=NIST384p)
    vk = sk.get_verifying_key()
    return vk, sk


def make_transaction(sk, message):
    """
    加密交易
    :param sk: 私钥，用于签名
    :param message: 消息
    :return: 签名
    """
    signature = sk.sign(str(message).encode("utf8"))  # 统一编码格式
    return signature


def is_valid_transaction(vk_string, message, signature):
    """
    验证交易是否合法
    :param vk_string: 公钥的字符串
    :param message: 消息
    :param signature: 签名
    :return: <bool> True合法，False不合法
    """
    vk = VerifyingKey.from_string(vk_string, NIST384p)
    try:
        print(vk.verify(signature, str(message).encode("utf8")))  # 统一编码格式
        return True
    except:
        return False


def hash_block(block):
    """
    返回区块链的哈希值
    :param block: 传入的区块链参数
    :return: 区块链的哈希值
    """
    block_string = block.hash_parameter()
    return hashlib.sha256(block_string).hexdigest()


def proof_of_work(last_block, new_block):
    """
    验证工作量是否合理
    :param last_block: 前一个区块
    :param new_block: 挖矿出来的区块
    :return: <bool>
    """
    last_str = last_block.block_to_json()
    nonce = new_block.nonce
    hash_str = hashlib.sha256(str(last_str + nonce).encode("utf8"))
    return hash_str[:4] == '0' * NUM_PROOF


def is_valid_chain(chain):
    """
    验证是否是合法的区块链
    :param chain: 传入的区块链参数
    :return: <bool>
    """
    if len(chain) == 1:  # 仅有一个区块，没有验证的必要性
        return True

    last_block = chain[0]
    index = 1
    while index < len(chain):
        hash_value = hash_block(last_block.hash_parameter())
        if last_block.hash != chain[index]['previous_hash']:  # 前后哈希的一致性
            return False
        if last_block.hash != hash_value:  # 是否篡改了哈希值
            return False
        if not proof_of_work(last_block, chain[index].nonce):  # 工作量证明是否正确
            return False
        # 检验区块中每一笔消息的正确性，但是不检查第一笔
        for transaction in chain[index].transactions[1:]:
            pk = str(transaction['sender'])
            sig = str(transaction['signature'])
            msg = str(transaction['message'])
            if not is_valid_transaction(pk, sig, msg):
                return False

    return True
