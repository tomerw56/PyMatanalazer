from PyMatAnalyzer.Tests.BaseClasses.ITestConfigProvider import ITestConfigProvider
from PyMatAnalyzer.Tests.Engine.LoadingData import LoadingData
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
from PyMatAnalyzer.Tests.BaseClasses.RunMetaDataMonitor import RunMetaDataMonitor
from PyMatAnalyzer.Tests.Engine.DefaultImplimentations.LoggerRunMetaDataMonitorWriter import LoggerRunMetaDataMonitorWriter
from zenlog import log
import logging
import importlib.util
from typing import Dict,NamedTuple
from pprint import pformat
from timeit import default_timer as timer
import sys
class TestsRunner():
    def __init__(self,configProvider:ITestConfigProvider,testsList:Dict[str,LoadingData],meta_data_monitor:RunMetaDataMonitor=None,logger=None):
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
                if(not value.is_file_valid):
                    self.__meta_data_monitor.WriteRunOutput(key,TestRunOutcome(RunOutcomeEnum.Error,f"test {key} file is invalid"))
                    continue
                success,params=self.__configProvider.GetConfigValuesForTest(key)
                if(not success):
                    self.__meta_data_monitor.WriteRunOutput(key, TestRunOutcome(RunOutcomeEnum.Error,
                                                                                f"test {key} failed to get config"))
                    continue
                self.__meta_data_monitor.WriteParmas(key,params )
                testActivator=self.__CreateTestDynamic(value,params)
                testActivator.PreStartOfRun()
                start=timer()
                outcome=testActivator.Run()
                end=timer()
                self.__meta_data_monitor.WriteRunOutput(key,end-start, outcome)

                testActivator.PreEndOfRun()
            except Exception as e:
                self.__meta_data_monitor.WriteException(key,e.__str__())
        self.__meta_data_monitor.WriteSummery()
    def __CreateTestDynamic(self,loadingdata:LoadingData,params:Dict[str,object],outputwriters=None):
        return self.__create_instance(loadingdata,params,outputwriters)

    def __create_instance(self,loadingdata:LoadingData,params:Dict[str,object],outputwriters=None):
        """
        Create a class instance from a full path to a class constructor
        :param class_str: module name plus '.' plus class name and optional parens with arguments for the class's
            __init__() method. For example, "a.b.ClassB.ClassB('World')"
        :return: an instance of the class specified.
        """
        logger=self.__logger
        class_str = format(f"{loadingdata.full_module_and_class_name}.DummyTestFramework(logger,params, outputwriters)")

        try:
            if "(" in class_str:
                full_class_name, args = class_name = class_str.rsplit('(', 1)
                args = '(' + args
            else:
                full_class_name = class_str
                args = ()
            # Get the class object
            module_path, _, class_name = full_class_name.rpartition('.')
            spec = importlib.util.spec_from_file_location(loadingdata.full_module_and_class_name, loadingdata.file_path)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            klazz = getattr(foo, class_name)
#            spec = importlib.util.spec_from_file_location(loadingdata.full_module_and_class_name, loadingdata.file_path)
            #mod = importlib.util.module_from_spec(spec)

            #mod = importlib.import_module(module_path)
            #klazz = getattr(mod, class_name)
            # Alias the the class so its constructor can be called, see the following link.
            # See https://www.programiz.com/python-programming/methods/built-in/eval
            alias = class_name + "Alias"
            instance = eval(alias + args, {alias: klazz,"logger":self.__logger,"params":params,"outputwriters":outputwriters})
            return instance
        except Exception as e:
            raise ImportError(class_str)