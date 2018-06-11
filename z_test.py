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

from flask import Flask

app = Flask(__name__)

app.route('/', method=[])
