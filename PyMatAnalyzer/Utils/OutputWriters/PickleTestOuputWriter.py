from pandas._libs.parsers import k

from PyMatAnalyzer.Tests.BaseClasses.IOutputWriter import IOutputWriter
from pprint import pformat
from typing import Dict
import os
import  pickle
class PickleTestOutputWriter(IOutputWriter):
    def __init__(self,logger,write_folder):
        self.__logger=logger
        self.__write_folder=write_folder
        self.__supported_keys={'file_name':'file name and folder','value':'value itself'}

    def WriteOutput(self,**kwargs)->bool:
        if all(elem in kwargs for elem in self.__supported_keys.keys() ):
            try:
                detination=os.path.join(self.__write_folder,kwargs["file_name"])
                with open(detination,'wb') as outfile:
                    pickle.dump(kwargs["value"],outfile)
            except Exception as e:
                self.__logger.error(f'could not write data validate params-> [{detination}] {e}')
                return False
            return True
        else:
            self.__logger.error(f'could not find needed params')
            return False
    def SupportedKeys(self)->Dict[str,str]:
        return self.__supported_keys