from dataset import FrameworkNativeDataset, GenericDataset, StructuredDataset


import torch


class GenericDataLoader:
    pass

# quite useless...
class TorchDataLoader(GenericDataLoader):
    def __init__(self, dataset: GenericDataset):
        self._dataloader = torch.DataLoader(dataset.to_pytorch())

    def load(self):
        return self._dataloader

class SklearnDataLoader(GenericDataLoader):
    def __init__(self, dataset: GenericDataset):

        self._dataloader = NPDataLoader(dataset.to_sklearn())

    def load(self):
        return self._dataloader
    

class NPDataLoader:
    # keep current implementation
    pass