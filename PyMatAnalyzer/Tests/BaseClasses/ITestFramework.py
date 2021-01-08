import logging
from typing import Dict
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.IOutputWriter import IOutputWriter
class ITestFramework():

    def __init__(self,test_name:str,logger,params:Dict[str,object],outputwriters:Dict[str,IOutputWriter]):
        self.__writers=outputwriters
        self.__params=params
        self.__logger=logger
        self.__test_name=test_name


    def PreEndOfRun(self,**kwargs):
        pass
    def PreStartOfRun(self,**kwargs):
        pass

    def Run(self,**kwargs)->TestRunOutcome:
        pass

    def SignalWritersToStop(self):
        if(self.__writers==None):
            return
        for key,value in self.__writers.items():
            self.__logger.info(f"signaling writer {key} to stop")
            value.EndWriting()
    def SignalWritersToStart(self):
        if (self.__writers == None):
            return
        for key,value in self.__writers.items():
            self.__logger.info(f"signaling writer {key} to start")
            value.PreWriting()
    @property
    def get_params(self):
        return self.__params


