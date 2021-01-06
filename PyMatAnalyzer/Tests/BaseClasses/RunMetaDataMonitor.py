from typing import Dict,List,Tuple

from contextlib import contextmanager
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
from PyMatAnalyzer.Tests.BaseClasses.IRunMetaDataMonitorWriter import IRunMetaDataMonitorWriter
class RunMetaDataMonitor(object):
    def __init__(self,writer:IRunMetaDataMonitorWriter):
        self.__SummeryHolder={}
        self.__SummeryHolder[RunOutcomeEnum.OK]=[]
        self.__SummeryHolder[RunOutcomeEnum.Warning] = []
        self.__SummeryHolder[RunOutcomeEnum.Error] = []
        self.__SummeryHolder[RunOutcomeEnum.Exception] = []
        self.__Writer=writer
    def WriteRunOutput(self,name:str,execution_time:float,outcome:TestRunOutcome):
        self.__SummeryHolder[outcome.Outcome].append((name, outcome))
        self.__Writer.WriteRunOutput(execution_time,name,outcome)


    def WriteParmas(self,name:str,params:Dict[str,object]):
        self.__Writer.WriteParmas(name,params)


    def WriteException(self,name:str,exception_string:str):
        outcome=TestRunOutcome(RunOutcomeEnum.Exception,exception_string)
        self.__SummeryHolder[outcome.Outcome].append((name,outcome))
        self.__Writer.WriteException(name,exception_string)

    def WriteSummery(self):
        self.__Writer.WriteSummery(self.__SummeryHolder)
