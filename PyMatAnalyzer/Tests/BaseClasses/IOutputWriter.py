from typing import Dict
from abc import ABC,abstractmethod,ABCMeta
class IOutputWriter(metaclass=ABCMeta):
    @abstractmethod
    def WriteTestOutput(self, **kwargs)->bool:
        pass

    @abstractmethod
    def SupportedKeys(self)->Dict[str,str]:
        pass


    def EndTestWriting(self):
        pass

    def PreTestWriting(self):
        pass