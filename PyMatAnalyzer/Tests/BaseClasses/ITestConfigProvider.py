from abc import ABC,abstractmethod,ABCMeta
from typing import Tuple,Dict
class ITestConfigProvider(metaclass=ABCMeta):
    @abstractmethod
    def GetConfigValuesForTest(self,testname,**kwargs)->Tuple[bool,Dict[int,object]]:
        pass