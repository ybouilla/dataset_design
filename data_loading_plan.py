

# usage in previous implementation:

# 0. user call MedicalFolderDataset in the trainingplan, and optionnally defines 
# a)methods to access data in the training plan to access to data in the demographics
# and b) dlp explicitly set in the dataset
# 1. check medical folder datastructure 
# 2. load data from demographics (if any). User should convert it into torch tensor
# to use it in his/her model
# 3. inhereting from `torch.Dataset`, it only implements the `__getintem__` method

from abc import abstractmethod
from typing import Dict


class DataLoadingPlanMixIn:
    #  wrapper for dataloading plan tools for dataset 
    def set_dlp(self):
        pass

    def apply_dlp(self):
        pass

class DataLoadingPlan(Dict[DataLoadingPlanTypes, MapperBlock]):
    # NB: in the original code, it is `DataLoadingBlock` instead of `MapperBlock`
    def serialize(self):
        # convert dlp into json so it can be saved into database 
        pass

    def desrialize(self):
        pass

    def infer_dataset_types(self):
        pass


    def _requries_dlp(self):
        # currently belongs to Flamby Dataset: proposal, move it to DataLoadingPlan
        pass

class DataLoadingBlock:
    # provide logic on how to handle a specific modality in the DataLoadingPlan
    # a DataLoadingPlanTypes is considered as a modality
    def serialize(self):
        pass
    
    def deserialize(self):
        # load file and code
        pass

    @abstractmethod
    def apply(self):
        pass


class MapperBlock(DataLoadingBlock):
    # extend DataLoadingBlock with a mapping facility
    # in the current code, used when loading a new data loading plan
    pass