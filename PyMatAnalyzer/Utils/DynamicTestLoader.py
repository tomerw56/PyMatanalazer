import importlib
from PyMatAnalyzer.Utils.LoadingData import LoadingData
from PyMatAnalyzer.Tests.BaseClasses.ITestFramework import ITestFramework
from typing import Dict
import copy

class DynamicTestLoader(object):
    def __init__(self,logger):
        self.__logger=logger


    def GetTestInstances(self,tests_to_create:Dict[str,LoadingData],constructor_params:Dict[str,object])->Dict[str,object]:
        result_objects={}
        for key,value in tests_to_create.items():
            try:
                self.__logger.info(f"attempting to create {key}")
                if(not value.is_file_valid):
                    self.__logger.error(f"test {key} file is invalid")
                    continue
                generated_object=self.__create_instance(value,constructor_params)
                if isinstance(generated_object,ITestFramework):
                    self.__logger.info(f"creation of object {key} success!!!")
                    result_objects[key] =generated_object
                else:
                    self.__logger.warning(f"{key} object created but it is not a valid test framework")
            except Exception as e:
                self.__logger.error(f"failed to create {key} - {e}")
        return result_objects
    def __build_constructor_args_str(self,params_keys):
        return format(f"({','.join(params_keys)})")
    def __create_instance(self, loadingdata: LoadingData, constructor_params: Dict[str, object]):
        """
        Create a class instance from a full path to a class constructor
        :param class_str: module name plus '.' plus class name and optional parens with arguments for the class's
            __init__() method. For example, "a.b.ClassB.ClassB('World')"
        :return: an instance of the class specified.
        """


        try:

            args=self.__build_constructor_args_str(constructor_params.keys())
            # Get the class object
            spec = importlib.util.spec_from_file_location(loadingdata.full_module_and_class_name,
                                                          loadingdata.file_path)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            klazz = getattr(foo, loadingdata.class_name)
            # Alias the the class so its constructor can be called, see the following link.
            # See https://www.programiz.com/python-programming/methods/built-in/eval
            alias = loadingdata.class_name+ "Alias"
            new_params=constructor_params.copy()
            new_params[alias]=klazz
            instance = eval(alias + args, new_params)
            return instance
        except Exception as e:
            self.__logger.error(f'failed to load object')
            raise ImportError(loadingdata.full_module_and_class_name)