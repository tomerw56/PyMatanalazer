import pandas as pd
from munch import munchify
from collections import defaultdict
import re
from PyMatAnalyzer.Utils.PandaToObjectConvertor import PandaToObjectConvertor
def CreateComplexObjectFromDict(indict:dict):
    ResultsDict={}
    RemovedKeys=[]
    InvestigatedKeysGroups=defaultdict(list)
    #first we handle what we have
    for key in indict.keys():
        if "." not in key:
            ResultsDict[key]=indict[key]
            RemovedKeys.append(key)
        else:
            sub_key=key.split(".")[0]
            InvestigatedKeysGroups[sub_key].append(key)


    #group every key to sub group
    for InvestigatedKey in InvestigatedKeysGroups:
        IsListOfItems=False
        #is list
        FoundNum = re.findall('\(\d\)', InvestigatedKey)
        IsListOfItems=len(FoundNum)>0
        #create sub dictonery
        Sub_Dict={}
        for SubInvestigatedKey in InvestigatedKeysGroups[InvestigatedKey]:
            New_Sub_Dict_Key=SubInvestigatedKey.replace(f"{InvestigatedKey}.","")
            Sub_Dict[New_Sub_Dict_Key]=indict[SubInvestigatedKey]
        if (not IsListOfItems):
            ResultsDict[InvestigatedKey]=CreateComplexObjectFromDict(Sub_Dict)
        else:
            New_Key=InvestigatedKey.replace(f"{FoundNum[0]}","")
            if (New_Key not in ResultsDict):
                ResultsDict[New_Key]=[]
            ResultsDict[New_Key].append(CreateComplexObjectFromDict(Sub_Dict))


    return ResultsDict


rows=[]

for i in range(20):
    row={}
    row["name"]=i
    row["seaats"]=i*1.5
    row["name"]=i*i
    row["name2.name3"] = i * i*i
    row["name2.name4"] = i * i * i*i
    row["person(1).name"]=i*2
    row["person(1).kids(1).name"] = i * 3
    row["person(1).kids(2).name"] = i * 4
    row["person(2).name"] = i * 5
    row["person(2).kids(1).name"] = i * 6
    row["person(2).kids(2).name"] = i * 7
    rows.append(row)

data=pd.DataFrame(rows)
print(data.head(3))
#splited=data.to_dict('records')

#complexobjets=[]
#for i in range(20):
   #resultdict={}
    #resultdict=CreateComplexObjectFromDict(splited[i])
    #x = munchify(resultdict)
    #k = 0
conv=PandaToObjectConvertor(data)
for item in conv:
    print(f"item ### {item}")



