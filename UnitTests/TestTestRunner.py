
from zenlog import log
from typing import  Dict,List,Tuple
from PyMatAnalyzer.Tests.BaseClasses.TestRunOutcome import TestRunOutcome
from PyMatAnalyzer.Tests.BaseClasses.Enums import RunOutcomeEnum
from PyMatAnalyzer.Tests.BaseClasses.IRunMetaDataMonitorWriter import IRunMetaDataMonitorWriter
from PyMatAnalyzer.Tests.BaseClasses.ITestFramework import ITestFramework
from UnitTests.DummyTestConfigProvider import DummyTestConfigProvider
from PyMatAnalyzer.Tests.Engine.TestsRunner import TestsRunner
import pathlib
import copy
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch

class Test_TestRunner(TestCase):
    def setUp(self):
        self.__summery={}
        self.__summery[RunOutcomeEnum.OK]=[]
        self.__summery[RunOutcomeEnum.Warning] = []
        self.__summery[RunOutcomeEnum.Error] = []
        self.__summery[RunOutcomeEnum.Exception] = []
    def tearDown(self):
        self.__summery.clear()
        self.__summery[RunOutcomeEnum.OK]=[]
        self.__summery[RunOutcomeEnum.Warning] = []
        self.__summery[RunOutcomeEnum.Error] = []
        self.__summery[RunOutcomeEnum.Exception] = []
    def WriteSummeryLocal(self, summery: Dict[RunOutcomeEnum, List[Tuple[str, TestRunOutcome]]]):
        self.__summery=summery.copy()

    def test_creation_success_1(self):

        mock_test_1 = create_autospec(ITestFramework)
        mock_test_1.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.OK,Description="")
        mock_test_1.get_params.return_value = {}
        mock_meta_data_writer=create_autospec(IRunMetaDataMonitorWriter)
        with patch.object(mock_meta_data_writer,'WriteSummery',new=self.WriteSummeryLocal):
            runner=TestsRunner(None,{'1':mock_test_1},mock_meta_data_writer)
            runner.Execute()
            self.assertEqual(len(self.__summery[RunOutcomeEnum.OK]),1)
    def test_creation_success_several(self):
        mock_test_1 = create_autospec(ITestFramework)
        mock_test_1.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.OK,Description="")
        mock_test_1.get_params.return_value = {}

        mock_test_2 = create_autospec(ITestFramework)
        mock_test_2.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.OK, Description="")
        mock_test_2.get_params.return_value = {}

        mock_test_3 = create_autospec(ITestFramework)
        mock_test_3.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.OK, Description="")
        mock_test_3.get_params.return_value = {}

        mock_meta_data_writer=create_autospec(IRunMetaDataMonitorWriter)
        with patch.object(mock_meta_data_writer,'WriteSummery',new=self.WriteSummeryLocal):
            runner=TestsRunner(None,{'1':mock_test_1,'2':mock_test_2,'3':mock_test_3},mock_meta_data_writer)
            runner.Execute()
            self.assertEqual(len(self.__summery[RunOutcomeEnum.OK]),3)

    def test_creation_mixed_several(self):
        mock_test_1 = create_autospec(ITestFramework)
        mock_test_1.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.Error,Description="")
        mock_test_1.get_params.return_value = {}

        mock_test_2 = create_autospec(ITestFramework)
        mock_test_2.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.OK, Description="")
        mock_test_2.get_params.return_value = {}

        mock_test_3 = create_autospec(ITestFramework)
        mock_test_3.Run.return_value = TestRunOutcome(Outcome=RunOutcomeEnum.OK, Description="")
        mock_test_3.get_params.return_value = {}

        mock_meta_data_writer=create_autospec(IRunMetaDataMonitorWriter)
        with patch.object(mock_meta_data_writer,'WriteSummery',new=self.WriteSummeryLocal):
            runner=TestsRunner(None,{'1':mock_test_1,'2':mock_test_2,'3':mock_test_3},mock_meta_data_writer)
            runner.Execute()
            self.assertEqual(len(self.__summery[RunOutcomeEnum.OK]),2)
            self.assertEqual(len(self.__summery[RunOutcomeEnum.Error]), 1)

