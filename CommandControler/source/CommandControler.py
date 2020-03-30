# -*- coding: utf-8 -*-
import difflib

class CommandControler:
    def __init__(self,commandDict:dict,name:str="未命名",prefix:str='/',version:str="1.0.0.0",introduce:str=""):
        '''
        :param commandDict: 指令集字典
        格式要求:
        {
            '指令名(ps:可通过|表示同义指令 示例-add|--a)': {
                'message': "指令信息 使用[{指令集前缀}?|help {该指令名}] 会得到该条信息",
                'helpMessage': "帮助信息 使用[{指令集前缀}?|help]时，该指令后方显示",
                'function': [调用该指令时执行的函数 详情见后],
                'childCommand': {子指令集字典，格式相同},
            },
        }
        function示例:
        def 函数名(
            param[该指令后方的切片字符串数组，已切割],
            (*args,**kwargs[doCommand方法指令字符串参数的后方参数不需要时设置为此])
            |(a,b,c[doCommand方法指令字符串参数的后方参数]))
        :param name: 指令集名
        :param prefix: 指令集识别前缀
        :param version: 指令集版本
        :param introduce: 指令集介绍
        '''
        self.name = name
        self.prefix = prefix
        self.version = version
        self.introduce = introduce
        self.paramERROR = "指令参数错误"
        self.commandDict = {
            'help|?': {
                'message': self.name+'指令集的帮助菜单',
                'helpMessage': '查询指令集 [pageNum:int=0|command:str]',
                'function': self.help,
            },
            'version|V': {
                'message': "{name:s}-{version:s} \n"
                           "指令集前缀为{prefix:s}\n"
                           "{introduce:s}".format(**{
                    "name":self.name,
                    "prefix":self.prefix,
                    "version":self.version,
                    "introduce":self.introduce,
                }),
                'helpMessage': '查询指令集的版本信息',
                'function': self.getVersionData,
            },**commandDict,}
    def help(self,param:list,*args,**kwargs):
        self.comamdCount = 0
        def getHelpByPage( page, commandDict,floor=0):
            rspSTR = ""
            if commandDict is None:
                commandDict = self.commandDict
            if page != -1: page -= 1
            if(page<0 and page!=-1):
                return self.paramERROR
            for command in commandDict:
                if int(self.comamdCount/10)==page or page == -1:
                    if len(command)>20:
                        rspSTR += \
                        ("  "*floor+("" if floor == 0 else "└")+"{command0:<20s}-\n"+
                        "  "*floor+"{command1:<21s}"+
                        "{helpMessage:<}"+"\n").format(
                            command0=command[:14],
                            command1=command[14:],
                            helpMessage=commandDict[command]['helpMessage'])
                    else: rspSTR += \
                        "  "*floor+("" if floor == 0 else "└")+"{command:<21s}" \
                        "{helpMessage:<}" \
                        "\n".format(
                        command=command,
                        helpMessage=commandDict[command]['helpMessage'])
                    if commandDict[command].get('childCommand'):
                        rspSTR += getHelpByPage(-1,commandDict[command].get('childCommand'),floor+1)
                else: continue
                self.comamdCount+=1
            if(page>int(self.comamdCount/10)):
                return self.paramERROR
            return rspSTR
        rspSTR = "[-----帮助-----]\n"
        if len(param) > 0:
            if len(param)==1:
                if param[0].isdigit():
                    return getHelpByPage(int(param[0]),self.commandDict)\
                           +"=========cur:{currentPage:d}|sum:{pageSum:d}"\
                               .format(currentPage=param[0],pageSum=int(self.comamdCount/10)+1)
                else:
                    command = self.__getCommandFromDict(param[0],self.commandDict)
                    if command.get('message'): rspSTR += "指令名:"+ param[0] +'\n'
                    rspSTR += "帮助信息:"+ command.get('helpMessage','未设置帮助信息').__str__()+'\n'
                    if command.get('message'): rspSTR += command.get('message').__str__() +'\n'
                    return rspSTR+"="*15
            else: return self.paramERROR
        else: return getHelpByPage(1,self.commandDict)\
                     +"=========cur:{currentPage:d}|sum:{pageSum:d}"\
                         .format(currentPage=1,pageSum=int(self.comamdCount/10)+1)
    def getVersionData(self,param,*args,**kwargs):
        if len(param) == 0:
            rspSTR = self.__getCommandFromDict("V",self.commandDict)['message']
            return rspSTR
        else: return self.paramERROR
    def __getCommandFromDict(self,commandStr,commandDict):
        maybeCommandList = []
        for commandList in commandDict:
            for command in commandList.split('|'):
                equal_rate = difflib.SequenceMatcher(None, commandStr, command).quick_ratio()
                if equal_rate==1:
                    return commandDict[commandList]
                elif equal_rate>=0.7:
                    maybeCommandList.append(command)
        if len(maybeCommandList)>0:return {
            'helpMessage':
                '\n你可能想找的指令为'+maybeCommandList.__str__()}
        else:return {'helpMessage':''}

    def __dealCommandStr(self, commandList,*args,**kwargs):
        commandDict = self.commandDict
        commandLen = len(commandList)
        commandPath = ""
        for index in range(commandLen):
            commandPath += commandList[index]
            command = self.__getCommandFromDict(commandList[index],commandDict)
            if command.get("message") is not None:
                if command.get("childCommand") and index+1<commandLen\
                    and self.__getCommandFromDict(commandList[index+1],command.get("childCommand")):
                    commandPath += '.'
                    commandDict = command.get("childCommand")
                    continue
                if commandLen==index+1: return command['function']([],*args,**kwargs)
                else: return command['function'](commandList[index+1:],*args,**kwargs)
            return "前缀为->\""+self.prefix+"\"指令集中无\""+commandPath+"\"指令"\
                   +command.get("helpMessage")
    def doCommand(self,allStr,*args,**kwargs)->str:
        if allStr[:len(self.prefix)] == self.prefix \
                and len(allStr) > len(self.prefix) \
                and allStr[len(self.prefix)] != ' ':
            commandStr = allStr[len(self.prefix):]
            return self.__dealCommandStr(' '.join(commandStr.split()).split(' '),*args,**kwargs)
        else: return "None"