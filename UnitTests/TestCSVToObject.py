import unittest
import pandas as pd
from PyMatAnalyzer.Utils.PandaToObjectConvertor import PandaToObjectConvertor
class TestConversion(unittest.TestCase):
    def test_creation_success_1(self):
        rows = []

        for i in range(20):
            row = {}
            row["name"] = i
            row["seaats"] = i * 1.5
            row["name"] = i * i
            row["name2.name3"] = i * i * i
            row["name2.name4"] = i * i * i * i
            row["person(1).name"] = i * 2
            row["person(1).kids(1).name"] = i * 3
            row["person(1).kids(2).name"] = i * 4
            row["person(2).name"] = i * 5
            row["person(2).kids(1).name"] = i * 6
            row["person(2).kids(2).name"] = i * 7
            rows.append(row)

        data = pd.DataFrame(rows)
        print(data.head(3))
        # splited=data.to_dict('records')

        # complexobjets=[]
        # for i in range(20):
        # resultdict={}
        # resultdict=CreateComplexObjectFromDict(splited[i])
        # x = munchify(resultdict)
        # k = 0
        conv = PandaToObjectConvertor(data)
        for item in conv:
            print(f"item ### {item}")
