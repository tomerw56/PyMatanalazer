from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.IRunMetaDataMonitorWriter import IRunMetaDataMonitorWriter
from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
import logging
from prettytable import prettytable
from typing import Dict,List,Tuple
from pprint import pformat
class LoggerRunMetaDataMonitorWriter(IRunMetaDataMonitorWriter):
    def __init__(self, logger):
        self.__logger=logger
    def WriteRunOutput(self, time: float, name: str, outcome: TestRunOutcome):
        self.__logger.info(f"Test {name} finished in {time} sec with outcome {pformat(outcome)}")

    def WriteParmas(self, name: str, params: Dict[str, object]):
        self.__logger.info(f"Test {name} initiated with params: {pformat(params)} ")

    def WriteException(self, name: str, exception_string: str):
        self.__logger.exception(f"Test {name} got an exception{pformat(exception_string)}")

    def WriteSummery(self,summery:Dict[RunOutcomeEnum,List[Tuple[str,TestRunOutcome]]]):
        t=prettytable.PrettyTable(['State','count'])
        t.add_row(['OK',len(summery[RunOutcomeEnum.OK])])
        t.add_row(['Error', len(summery[RunOutcomeEnum.Error])])
        t.add_row(['Warning', len(summery[RunOutcomeEnum.Warning])])
        t.add_row(['Exception', len(summery[RunOutcomeEnum.Exception])])
        self.__logger.info(t)
        self.__WriteTestsStatus('OK',summery[RunOutcomeEnum.OK])
        self.__WriteTestsStatus('Warning', summery[RunOutcomeEnum.Warning])
        self.__WriteTestsStatus('Error', summery[RunOutcomeEnum.Error])
        self.__WriteTestsStatus('Exception', summery[RunOutcomeEnum.Exception])

    def __WriteTestsStatus(self,test_state,summery:List[Tuple[str,TestRunOutcome]]):
        self.__logger.info(f"Tests with state {test_state}")
        t = prettytable.PrettyTable(['Name'])

        for pair in summery:
            t.add_row([pair[0]])
        self.__logger.info(t)
