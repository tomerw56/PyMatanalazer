from PyMatAnalyzer.Tests.BaseClasses.ITestFramework import ITestFramework
from PyMatAnalyzer.Tests.BaseClasses.IOutputWriter import IOutputWriter
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from typing import Dict
class DummyTestFrameworkNotIheritingFromFrameWork(object):

    def __init__(self,logger,params:Dict[str,object],outputwriters:Dict[str,IOutputWriter]):
        pass

    def PreEndOfRun(self,**kwargs):
        self._ITestFramework__logger.info("called PreEndOfRun")

    def PreStartOfRun(self,**kwargs):
        self._ITestFramework__logger.info("called PreStartOfRun")

    def Run(self,**kwargs)->TestRunOutcome:
        self._ITestFramework__logger.info("called Run")
        return TestRunOutcome()
