

# usage in previous implementation:

# 0. user call MedicalFolderDataset in the trainingplan, and optionnally defines 
# a)methods to access data in the training plan to access to data in the demographics
# and b) dlp explicitly set in the dataset
# 1. check medical folder datastructure 
# 2. load data from demographics (if any). User should convert it into torch tensor
# to use it in his/her model
# 3. inhereting from `torch.Dataset`, it only implements the `__getintem__` method

class DataLoadingPlan(Dict[DataLoadingPlanTypes, DataLoadingBlock]):

    def serialize(self):
        # convert dlp into json so it can be saved into database 
        pass

    def desrialize(self):
        pass

    def infer_dataset_types(self):
        pass


class DataLoadingBlock(MapperBlock):

    pass

class MapperBlock:
    pass