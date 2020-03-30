# -*- coding: utf-8 -*-
from CommandControler import CommandControler

def simpleExample():
    # 最小实例
    demoCC = CommandControler(
        name="控制台",
        introduce="demo",
        commandDict={
            'add|a': {
                'message': "相加俩个值",
                'helpMessage': '加 [x:int,y:int]',
                'function':
                    lambda param,*args,**kwargs:\
                        (int(param[0]) + int(param[1])),
            },
            'getId|gi': {
                'message': "获取id",
                'helpMessage': '获取id',
                'function': lambda param,userId:userId,
            },
        })
    # 使用
    while True:
        inStr = input('->')
        resp = demoCC.doCommand(inStr, userId="0001")
        if resp != 'None': print(resp);continue

def normalExample():
    def getFab(param,*args,**kwargs):
        def fab(number):
            if number==1 or number==2:
                return 1
            else:
                return fab(number-1)+fab(number-2)
        return fab(int(param[0]))
    normal_countCommandDict = {
        'add|-a': {
            'message': "相加俩个值",
            'helpMessage': '加 [x:int,y:int]',
            'function':
                lambda param,*args,**kwargs:\
                    (int(param[0]) + int(param[1])),
        },
        'minus|-m': {
            'message': "相减俩个值",
            'helpMessage': '减 [x:int,y:int]',
            'function':
                lambda param,*args,**kwargs:\
                    (int(param[0]) - int(param[1])),
        },}
    science_countCommandDict = {
        'index|-i': {
            'message': "求一个数的指数",
            'helpMessage': '指数运算 [x:int,y:int]',
            'function':
                lambda param,*args,**kwargs:\
                    pow(int(param[0]),int(param[1])),
        },
        'getFab|gf': {
            'message': "求斐波那契数列第n项",
            'helpMessage': '求斐波那契数列 [n:int]',
            'function': getFab,
        },}
    countCommandDict = {
        'normal|-n': {
            'message': "普通计算器",
            'helpMessage': '普通计算器能计算加减',
            'function':lambda param,*args,**kwargs:"一个普通计算器",
            'childCommand':normal_countCommandDict,
        },
        'science|-s': {
            'message': "科学计算器",
            'helpMessage': '科学计算器能进行指数运算',
            'function':lambda param,*args,**kwargs:"一个科学计算器",
            'childCommand':science_countCommandDict,
        },
    }
    # 实例0
    countCC = CommandControler(
        name="计算器",prefix="#-",version="1.0.0",
        introduce="一个通过指令控制的计算器",
        commandDict=countCommandDict)
    # 实例1
    scienceCC = CommandControler(
        name="科学计算器",prefix="kx",version="1.0.0",
        introduce="科学计算器",
        commandDict=science_countCommandDict)
    # 使用
    while True:
        inStr = input('->')
        resp = countCC.doCommand(inStr)
        if resp != 'None': print(resp);continue
        resp = scienceCC.doCommand(inStr)
        if resp != 'None': print(resp);continue

if __name__ == '__main__':
    normalExample()