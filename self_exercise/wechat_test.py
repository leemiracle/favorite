#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 18-7-3
@Author  : leemiracle
"""

import itchat, time
from itchat.content import *


def test_send_filehelper():
    itchat.send('Hello, filehelper', toUserName='filehelper')


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # 群聊
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))


def search_friends():
    # 用户搜索
    # 获取自己的用户信息，返回自己的属性字典
    itchat.search_friends()
    # 获取特定UserName的用户信息
    itchat.search_friends(userName='@abcdefg1234567')
    # 获取任何一项等于name键值的用户
    itchat.search_friends(name='littlecodersh')
    # 获取分别对应相应键值的用户
    itchat.search_friends(wechatAccount='littlecodersh')
    # 三、四项功能可以一同使用
    itchat.search_friends(name='LittleCoder机器人', wechatAccount='littlecodersh')


def main():
    # 扫二维码， 一定时间重新开启也不用扫码
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    test_send_filehelper()
    itchat.run()


if __name__ == '__main__':
    main()
