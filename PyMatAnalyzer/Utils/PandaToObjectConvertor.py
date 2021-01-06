import pandas as pd
from munch import munchify
from collections import defaultdict
import re
class PandaToObjectConvertor:
    def __init__(self,dataframe:pd.DataFrame):
        self.__Items=[]
        self.__ProcessDataFrame(dataframe)

    def __CreateComplexObjectFromDict(self,indict: dict):
        ResultsDict = {}
        RemovedKeys = []
        InvestigatedKeysGroups = defaultdict(list)
        # first we handle what we have
        for key in indict.keys():
            if "." not in key:
                ResultsDict[key] = indict[key]
                RemovedKeys.append(key)
            else:
                sub_key = key.split(".")[0]
                InvestigatedKeysGroups[sub_key].append(key)

        # group every key to sub group
        for InvestigatedKey in InvestigatedKeysGroups:
            IsListOfItems = False
            # is list
            FoundNum = re.findall('\(\d\)', InvestigatedKey)
            IsListOfItems = len(FoundNum) > 0
            # create sub dictonery
            Sub_Dict = {}
            for SubInvestigatedKey in InvestigatedKeysGroups[InvestigatedKey]:
                New_Sub_Dict_Key = SubInvestigatedKey.replace(f"{InvestigatedKey}.", "")
                Sub_Dict[New_Sub_Dict_Key] = indict[SubInvestigatedKey]
            if (not IsListOfItems):
                ResultsDict[InvestigatedKey] = self.__CreateComplexObjectFromDict(Sub_Dict)
            else:
                New_Key = InvestigatedKey.replace(f"{FoundNum[0]}", "")
                if (New_Key not in ResultsDict):
                    ResultsDict[New_Key] = []
                ResultsDict[New_Key].append(self.__CreateComplexObjectFromDict(Sub_Dict))

        return ResultsDict

    def __ProcessDataFrame(self,dataframe:pd.DataFrame):
        splited = dataframe.to_dict('records')
        for i in range(len(splited)):
            resultdict = {}
            resultdict = self.__CreateComplexObjectFromDict(splited[i])
            self.__Items.append(munchify(resultdict))
    def __iter__(self):
        return self.__Items.__iter__()