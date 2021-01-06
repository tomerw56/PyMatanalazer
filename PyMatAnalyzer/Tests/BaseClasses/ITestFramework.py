import logging
from typing import Dict
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.IOutputWriter import IOutputWriter
class ITestFramework():

    def __init__(self,logger,params:Dict[str,object],outputwriters:Dict[str,IOutputWriter]):
        self.__writers=outputwriters
        self.__params=params
        self.__logger=logger


    def PreEndOfRun(self,**kwargs):
        pass
    def PreStartOfRun(self,**kwargs):
        pass

    def Run(self,**kwargs)->TestRunOutcome:
        pass


