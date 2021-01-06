from  abc import  abstractmethod,ABCMeta
from typing import Dict,Tuple,List
from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
class IRunMetaDataMonitorWriter(metaclass=ABCMeta):
    @abstractmethod
    def WriteRunOutput(self, time: float, name: str, outcome: TestRunOutcome):
        pass

    @abstractmethod
    def WriteParmas(self, name: str, params: Dict[str, object]):
        pass

    @abstractmethod
    def WriteException(self, name: str, exception_string: str):
        pass
    @abstractmethod
    def WriteSummery(self,summery:Dict[RunOutcomeEnum,List[Tuple[str,TestRunOutcome]]]):
        pass


