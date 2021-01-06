from abc import ABC,abstractmethod,ABCMeta
class IOutputWriter(metaclass=ABCMeta):
    @abstractmethod
    def WriteOutput(self,field:str,sub_field:str,ouput:object):
        pass
