from PyMatAnalyzer.Tests.BaseClasses.ITestConfigProvider import ITestConfigProvider
from PyMatAnalyzer.Tests.BaseClasses.ITestFramework import ITestFramework
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
from PyMatAnalyzer.Tests.BaseClasses.RunMetaDataMonitor import RunMetaDataMonitor
from PyMatAnalyzer.Tests.Engine.DefaultImplimentations.LoggerRunMetaDataMonitorWriter import LoggerRunMetaDataMonitorWriter
from zenlog import log
import importlib.util
from typing import Dict
from timeit import default_timer as timer


class TestsRunner():
    def __init__(self,configProvider:ITestConfigProvider,testsList:Dict[str,ITestFramework],meta_data_monitor:RunMetaDataMonitor=None,logger=None):
        self.__testList=testsList
        self.__configProvider=configProvider
        if logger==None:
            self.__logger=log
        else:
            self.__logger = logger
        if meta_data_monitor==None:
            self.__meta_data_monitor=RunMetaDataMonitor(LoggerRunMetaDataMonitorWriter(self.__logger))
        else:
            self.meta_data_monitor=meta_data_monitor

    def Execute(self):
        for key,value in self.__testList.items():
            try:
                self.__logger.info(f"Handeling test {key}")
                self.__meta_data_monitor.WriteParmas(key,value.get_params )
                value.PreStartOfRun()
                start=timer()
                outcome=value.Run()
                end=timer()
                self.__meta_data_monitor.WriteRunOutput(key,end-start, outcome)

                value.PreEndOfRun()
            except Exception as e:
                self.__meta_data_monitor.WriteException(key,e.__str__())
        self.__meta_data_monitor.WriteSummery()
