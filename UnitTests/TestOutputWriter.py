from unittest import TestCase
from zenlog import log
import os
from unittest.mock import Mock, create_autospec, patch
from PyMatAnalyzer.Utils.OutputWriters.LoggerTestOutputWriter import LoggerTestOutputWriter
from PyMatAnalyzer.Utils.OutputWriters.PickleTestOuputWriter import PickleTestOutputWriter
from PyMatAnalyzer.Utils.OutputWriters.CsvTestOutputWriter import CsvTestOutputWriter
import pandas as pd
import csv
import pathlib
class TestOutputWriter(TestCase):
    def setUp(self):
        self.__pickle_file='dummy_file_name.dat'
        self.__csv_file = 'dummy_file_name.csv'
        self.__doc_file = 'dummy_file_name.docx'
        self.__clean_file(self.__pickle_file)
        self.__clean_file(self.__csv_file)
        self.__clean_file(self.__doc_file)



    def __clean_file(self,file_name):
        folder = pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),file_name)
        if(pathlib.Path.exists(pathlib.Path(folder))):
            os.remove(folder)

    def test_logger_writer_full_values(self):
        test_writer=LoggerTestOutputWriter(log)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        result=test_writer.WriteOutput(value="the_value",headline="the_header")
        self.assertEqual(result,True)
    def test_logger_writer_part_values_but_write_anyway(self):
        test_writer=LoggerTestOutputWriter(log,write_unknown_values=True)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        result=test_writer.WriteOutput(value="the_value")
        self.assertEqual(result,True)

    def test_logger_writer_part_values_fail(self):
        test_writer=LoggerTestOutputWriter(log,write_unknown_values=False)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        result=test_writer.WriteOutput(value="the_value")
        self.assertEqual(result,False)

    def test_pickle_writer_full_values(self):
        folder=pathlib.Path(__file__).parent.absolute()
        test_writer=PickleTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__pickle_file
        result=test_writer.WriteOutput(value={'just_some_value':0},file_name=test_file_name)
        self.assertEqual(result,True)
        self.assertEqual(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name)).is_file(),True)
        self.__clean_file(self.__pickle_file)
    def test_pickle_writer_write_fail_with_invalid_folder(self):
        folder=r"No_such_folder:\\"
        test_writer = PickleTestOutputWriter(log, write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()), 2)
        test_file_name = self.__pickle_file
        result = test_writer.WriteOutput(value={'just_some_value': 0}, file_name=test_file_name)
        self.assertEqual(result, False)

    def test_pickle_writer_partial_values(self):
        folder = pathlib.Path(__file__).parent.absolute()
        test_writer = PickleTestOutputWriter(log, write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()), 2)
        test_file_name = self.__pickle_file
        result = test_writer.WriteOutput(file_name=test_file_name)
        self.assertEqual(result, False)

    def test_csv_writer_full_values_list_of_dictoneries(self):
        folder=pathlib.Path(__file__).parent.absolute()
        test_writer=CsvTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__csv_file
        data=[]
        data.append({'name': 'Tomer1', 'key': 1, 'age': 'old1'})
        data.append({'name': 'Tomer2', 'key': 2, 'age': 'old2'})
        data.append({'name':'Tomer3','key':3,'age':'old3'})
        result=test_writer.WriteOutput(value=data,file_name=test_file_name)
        self.assertEqual(result,True)
        self.assertEqual(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name)).is_file(),True)
        self.__clean_file(self.__pickle_file)

    def test_csv_writer_full_values_append_list_of_dictoneries(self):
        folder=pathlib.Path(__file__).parent.absolute()
        test_writer=CsvTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__csv_file
        data=[]
        data.append({'name': 'Tomer1', 'key': 1, 'age': 'old1'})
        data.append({'name': 'Tomer2', 'key': 2, 'age': 'old2'})
        data.append({'name':'Tomer3','key':3,'age':'old3'})
        result=test_writer.WriteOutput(value=data,file_name=test_file_name)
        with open(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name))) as csvfile:
            reader = csv.DictReader(csvfile)
            self.assertEqual(len(list(reader)),3)
        data.clear()
        data.append({'name': 'Tomer4', 'key': 4, 'age': 'old4'})
        result = test_writer.WriteOutput(value=data, file_name=test_file_name)

        self.assertEqual(result,True)
        with open(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name))) as csvfile:
            reader = csv.DictReader(csvfile)
            self.assertEqual(len(list(reader)),4)

        self.__clean_file(self.__pickle_file)

    def test_csv_writer_full_values_data_frame(self):
        folder=pathlib.Path(__file__).parent.absolute()
        test_writer=CsvTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__csv_file
        names=['Tomer1','Tomer2','Tomer3']
        ages=['old1','old2','old3']
        names_series = pd.Series(names)
        ages_series = pd.Series(ages)
        frame = {'Name': names_series, 'Age': ages_series}
        data = pd.DataFrame(frame)
        result=test_writer.WriteOutput(value=data,file_name=test_file_name)
        self.assertEqual(result,True)
        self.assertEqual(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name)).is_file(),True)
        self.__clean_file(self.__pickle_file)

    def test_csv_writer_full_values_append_list_of_dictoneries(self):
        folder=pathlib.Path(__file__).parent.absolute()
        test_writer=CsvTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__csv_file
        names = ['Tomer1', 'Tomer2', 'Tomer3']
        ages = ['old1', 'old2', 'old3']
        names_series = pd.Series(names)
        ages_series = pd.Series(ages)
        frame = {'Name': names_series, 'Age': ages_series}
        data = pd.DataFrame(frame)
        result=test_writer.WriteOutput(value=data,file_name=test_file_name)
        with open(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name))) as csvfile:
            reader = csv.DictReader(csvfile)
            self.assertEqual(len(list(reader)),3)

        names = ['Tomer4']
        ages = ['old4']
        names_series = pd.Series(names)
        ages_series = pd.Series(ages)
        frame = {'Name': names_series, 'Age': ages_series}
        data2 = pd.DataFrame(frame)
        result = test_writer.WriteOutput(value=data2, file_name=test_file_name)

        self.assertEqual(result,True)
        with open(pathlib.Path(pathlib.Path.joinpath(folder,test_file_name))) as csvfile:
            reader = csv.DictReader(csvfile)
            self.assertEqual(len(list(reader)),4)

        self.__clean_file(self.__pickle_file)

    def test_csv_writer_fail_partial_values(self):
        folder = pathlib.Path(__file__).parent.absolute()
        test_writer = CsvTestOutputWriter(log, write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()), 2)
        test_file_name = self.__pickle_file
        result = test_writer.WriteOutput(file_name=test_file_name)
        self.assertEqual(result, False)

    def test_csv_writer_fail_no_folder(self):
        folder="x:\\No_Such_Folder"
        test_writer=CsvTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__csv_file
        names=['Tomer1','Tomer2','Tomer3']
        ages=['old1','old2','old3']
        names_series = pd.Series(names)
        ages_series = pd.Series(ages)
        frame = {'Name': names_series, 'Age': ages_series}
        data = pd.DataFrame(frame)
        result=test_writer.WriteOutput(value=data,file_name=test_file_name)
        self.assertEqual(result,False)

    def test_csv_writer_fail_not_supported_type(self):
        folder="x:\\No_Such_Folder"
        test_writer=CsvTestOutputWriter(log,write_folder=folder)
        self.assertEqual(len(test_writer.SupportedKeys().keys()),2)
        test_file_name=self.__csv_file
        names=['Tomer1','Tomer2','Tomer3']
        ages=['old1','old2','old3']
        #data type not supported
        data = [names,ages]
        result=test_writer.WriteOutput(value=data,file_name=test_file_name)
        self.assertEqual(result,False)