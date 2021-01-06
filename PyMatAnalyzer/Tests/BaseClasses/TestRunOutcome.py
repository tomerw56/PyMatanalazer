from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
from dataclasses import dataclass


@dataclass
class TestRunOutcome():
    Outcome:RunOutcomeEnum=RunOutcomeEnum.OK
    Description:str=""