from pandas._libs.parsers import k

from PyMatAnalyzer.Tests.BaseClasses.IOutputWriter import IOutputWriter
import pandas as pd
import csv
import pathlib
from typing import Dict,List
import os
import  pickle
class CsvTestOutputWriter(IOutputWriter):
    def __init__(self,logger,write_folder):
        self.__logger=logger
        self.__write_folder=write_folder
        self.__supported_keys={'file_name':'file name and folder','value':'value itself'}

    def WriteOutput(self,**kwargs)->bool:
        if all(elem in kwargs for elem in self.__supported_keys.keys() ):
            try:
                if type(kwargs["value"]) is list and type(kwargs["value"][0]) is dict:
                    if len(kwargs["value"])==0:
                        self.__logger.error(f"recived list but no elements-failed to write")
                        return False
                    return self.__write_dict_to_csv(kwargs["file_name"],kwargs["value"])
                else:
                    if type(kwargs["value"])==pd.DataFrame:
                        return self.__write_data_frame_to_csv(kwargs["file_name"], kwargs["value"])
            except Exception as e:
                self.__logger.error(f'could not write data {e}')
                return False
            self.__logger.error(f'could not determine data type')
            return False
        else:
            self.__logger.error(f'could not find needed params')
            return False
    def __get_file_open_mode(self,does_file_exsist:bool)->str:
        if does_file_exsist:
            return "a"
        return "w+"
    def __write_data_frame_to_csv(self, file_name, value: pd.DataFrame) -> bool:
        try:
            csv_file = os.path.join(self.__write_folder, file_name)
            does_file_exsist = pathlib.Path.exists(pathlib.Path(csv_file))
            value.to_csv(csv_file,mode=self.__get_file_open_mode(does_file_exsist),header=not does_file_exsist)

        except Exception as e:
            self.__logger.error(f'could not write data frame to -> [{csv_file}] {e}')
            return False
        return True

    def __write_dict_to_csv(self,file_name,value:List[Dict])->bool:
        try:
            csv_columns = value[0].keys()
            csv_file = os.path.join(self.__write_folder, file_name)
            does_file_exsist=pathlib.Path.exists(pathlib.Path(csv_file))
            with open(csv_file, self.__get_file_open_mode(does_file_exsist)) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                if not does_file_exsist:
                    writer.writeheader()
                for data in value:
                    writer.writerow(data)

        except Exception as e:
            self.__logger.error(f'could not write List to -> [{csvfile}] {e}')
            return False
        return True
    def SupportedKeys(self)->Dict[str,str]:
        return self.__supported_keys