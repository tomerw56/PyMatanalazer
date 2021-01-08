from PyMatAnalyzer.Tests.BaseClasses.IOutputWriter import IOutputWriter
from pprint import pformat
from typing import Dict
class LoggerTestOutputWriter(IOutputWriter):
    def __init__(self,logger,write_unknown_values=False):
        self.__logger=logger
        self.__write_unknown_values=write_unknown_values
        self.__supported_keys={'headline':'header to print','value':'value itself'}

    def WriteTestOutput(self, **kwargs)->bool:
        if all(elem in kwargs for elem in self.__supported_keys.keys() ):
            self.__logger.info(format(f"{kwargs['headline']}  {kwargs['value']}"))
        else:
            if(self.__write_unknown_values):
                self.__logger.info(f'{pformat(kwargs)}')
            else:
                return False
        return True
    def SupportedKeys(self)->Dict[str,str]:
        return self.__supported_keys