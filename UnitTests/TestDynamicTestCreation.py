import unittest
from UnitTests.DummyTestConfigProvider import DummyTestConfigProvider
from PyMatAnalyzer.Tests.Engine.TestsRunner import TestsRunner
from PyMatAnalyzer.Tests.Engine.LoadingData import LoadingData
class TestDynamicTestCreation(unittest.TestCase):
    def test_creation(self):
        config=DummyTestConfigProvider()
        test_to_run={}
        data_for_loading=LoadingData(file_path=r"C:\Repos\MyLittleMathAnalazer\UnitTests\DummyTestFramework.py", full_module_and_class_name="DummyTestFramework")
        test_to_run["1"]=data_for_loading
        runner=TestsRunner(config,test_to_run)
        runner.Execute()
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()