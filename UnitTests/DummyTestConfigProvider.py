from PyMatAnalyzer.Tests.BaseClasses.ITestConfigProvider import ITestConfigProvider
from typing import Dict,Tuple
class DummyTestConfigProvider(ITestConfigProvider):
    def GetConfigValuesForTest(self,testname,**kwargs)->Tuple[bool,Dict[int,object]]:
        return (True,{})