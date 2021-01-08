import unittest
from zenlog import log
from PyMatAnalyzer.Utils.DynamicTestLoader import DynamicTestLoader
from UnitTests.DummyTestConfigProvider import DummyTestConfigProvider
from PyMatAnalyzer.Tests.Engine.TestsRunner import TestsRunner
from PyMatAnalyzer.Utils.LoadingData import LoadingData
import pathlib

class TestDynamicTestCreation(unittest.TestCase):
    def test_creation_success_1(self):
        config=DummyTestConfigProvider()
        test_to_run={}
        data_for_loading=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["1"]=data_for_loading
        loader=DynamicTestLoader(log)
        constructor_params={}
        constructor_params['test_name'] = '1'
        constructor_params['logger']=log
        constructor_params['params']=config.GetConfigValuesForTest('1')[1]
        constructor_params['outputwriters']= {}
        results=loader.GetTestInstances(test_to_run,constructor_params)
        self.assertEqual(len(results),1)
    def test_creation_success_multi(self):
        config=DummyTestConfigProvider()
        test_to_run={}
        data_for_loading_1=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["1"]=data_for_loading_1
        data_for_loading_2=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["2"]=data_for_loading_2
        data_for_loading_3=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["3"]=data_for_loading_3
        loader=DynamicTestLoader(log)
        constructor_params={}
        constructor_params['test_name'] = '1'

        constructor_params['logger']=log
        constructor_params['params']=config.GetConfigValuesForTest('1')[1]
        constructor_params['outputwriters']=None
        results=loader.GetTestInstances(test_to_run,constructor_params)
        self.assertEqual(len(results),3)
    def test_creation_missing_file(self):
        config=DummyTestConfigProvider()
        test_to_run={}
        data_for_loading_1=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["1"]=data_for_loading_1
        data_for_loading_2=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFrameworkNotIheritingFromFrameWork.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["missing_file"]=data_for_loading_2
        data_for_loading_3=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["3"]=data_for_loading_3
        loader=DynamicTestLoader(log)
        constructor_params={}
        constructor_params['test_name'] = '1'

        constructor_params['logger']=log
        constructor_params['params']=config.GetConfigValuesForTest('1')[1]
        constructor_params['outputwriters']=None
        results=loader.GetTestInstances(test_to_run,constructor_params)
        self.assertEqual(len(results),2)
    def test_creation_success_diffrent_types(self):
        config=DummyTestConfigProvider()
        test_to_run={}
        data_for_loading_1=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["1"]=data_for_loading_1
        data_for_loading_2=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["2"]=data_for_loading_2
        data_for_loading_3=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFrameworkResultInput.py"), full_module_and_class_name="DummyTestFrameworkResultInput")
        test_to_run["3"]=data_for_loading_3
        loader=DynamicTestLoader(log)
        constructor_params={}
        constructor_params['test_name'] = '1'

        constructor_params['logger']=log
        constructor_params['params']=config.GetConfigValuesForTest('1')[1]
        constructor_params['outputwriters']=None
        results=loader.GetTestInstances(test_to_run,constructor_params)
        self.assertEqual(len(results),3)

    def test_creation_fail_not_inherinig(self):
        config=DummyTestConfigProvider()
        test_to_run={}
        data_for_loading_1=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFramework.py"), full_module_and_class_name="DummyTestFramework")
        test_to_run["1"]=data_for_loading_1
        data_for_loading_2=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFrameworkNotIheritingFromFrameWork.py"), full_module_and_class_name="DummyTestFrameworkNotIheritingFromFrameWork")
        test_to_run["2"]=data_for_loading_2
        data_for_loading_3=LoadingData(file_path=pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),"DummyTestFrameworkResultInput.py"), full_module_and_class_name="DummyTestFrameworkResultInput")
        test_to_run["3"]=data_for_loading_3
        loader=DynamicTestLoader(log)
        constructor_params={}
        constructor_params['test_name'] = '1'

        constructor_params['logger']=log
        constructor_params['params']=config.GetConfigValuesForTest('1')[1]
        constructor_params['outputwriters']=None
        results=loader.GetTestInstances(test_to_run,constructor_params)
        self.assertEqual(len(results),2)




if __name__ == '__main__':
    unittest.main()