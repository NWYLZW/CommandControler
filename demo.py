# -*- coding: utf-8 -*-
from CommandControler import CommandControler

def userContro(param,*args,**kwargs):
    return "这是userContro"+str(param)
def userContro_a(param,fromUser):
    return "这是userContro_a"+str(param)+fromUser
def userContro_d(param,fromUser):
    return "这是userContro_d"+str(param)+fromUser
def userContro_gmd(param,fromUser):
    return "这是userContro_d"+str(param)+fromUser

if __name__ == '__main__':
    # 最小示例
    demoCC = CommandControler(
        name="控制台",
        introduce="demo",
        commandDict={
            'add|a': {
                'message': "添加",
                'helpMessage': '添加',
                'function': lambda param,x:str(param)+x,
            },
        })
    mcc = CommandControler(
        prefix="#",
        name="打卡控制台",
        version="1.0.0.0",
        introduce="疫情打卡控制台",
        commandDict={
            'userContro|uc': {
                'message': "用户管理",
                'helpMessage': '对在进行签到的用户进行管理',
                'function': userContro,
                'childCommand': {
                    '-add|--a': {
                        'message': "添加用户",
                        'helpMessage': '添加一个用户到签到管理中 [userName:str,PWD:str]',
                        'function': userContro_a,
                    },
                    '-delete|--d': {
                        'message': "删除用户",
                        'helpMessage': '通过用户名从签到管理中删除一个用户 [userName:str]',
                        'function': userContro_d,
                    },
                    '-getMyData|--gmd': {
                        'message': "获取签到信息",
                        'helpMessage': '获取最近我的签到信息 [len:int<3]',
                        'function': userContro_gmd,
                    },
                }
            },
        })
    while True:
        inStr = input('->')
        resp = demoCC.doCommand(inStr)
        if resp!='None': print(resp);continue
        resp = mcc.doCommand(inStr)
        if resp!='None': print(resp);continue
