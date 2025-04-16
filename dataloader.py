from dataset import FrameworkNativeDataset, GenericDataset


import torch


class GenericDataLoader:
    pass


class TorchDataLoader(GenericDataLoader):
    def __init__(self, dataset: GenericDataset):

        if isinstance(dataset, FrameworkNativeDataset):
            self._dataloader = torch.DataLoader(dataset.to_pytorch())
        else:

            class TorchDataset(torch.Dataset):
                def __init__(self, dataset: GenericDataset):
                    self._dataset = dataset

                def __len__(self):
                    return len(self._dataset)
                
                def __getitem__(self, idx: int):
                    return self._dataset[idx]
                
            self._dataloader = torch.DataLoader(TorchDataset(self._dataset))
    

    def save(self):

    def load(self):


class SklearnDataLoader(GenericDataLoader):



class NPDataLoader:
    pass