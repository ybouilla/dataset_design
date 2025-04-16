from typing import Any, Dict, List, Optional, Tuple, Union
from reader import CSVReader

import pandas as pd
import torch

class GenericDataset:
    
    def shape(self):
    
    def add_description(self):



class FrameworkNativeDataset:
    # wrapper for dataset that has been implemented in a specific framework, and is reused in FBM
    def __init__(self, dataset: Union[Tuple[Any, Any], Any],
                 target: Optional[Any] = None, kwargs_loader: Optional[Dict] = None, kwargs_reader: Optional[Dict]=None):
        self._dataset = dataset
        self._target = target

    def process(self):
        if isinstance(self._dataset, (pd.Series, pd.DataFrame)):
            self._dataset = CSVDataset(self._dataset, self._target)

        elif isinstance(self._dataset, (torch.Dataset, monai.Dataset)):
            self._dataset = NativeImageDataset(self._dataset)

    def shape(self) -> List[int]:
        return self._dataset.shape()
    def add_description(self) -> str:
        return self._dataset.add_description()
    

class StructuredDataset:
    # wrapper for FedBioMed "handmade" datasets
    def __init__(self, dataset: GenericDataset, target = None):
        self._dataset = dataset

    def process(self):
        pass

    def shape(self) -> List[int]:
        return self._dataset.shape()
    def add_description(self) -> str:
        return self._dataset.add_description()

class NativeImageDataset(GenericDataset):
    def __init__(self, dataset: torch.Dataset, target = None):
        self._dataset = dataset

    def to_pytorch(self):

        return self._dataset
    
    def to_sklearn(self):
            # TODO: implement conversion from pytorch to sklearn
        return self._dataset
    
    def shape(self) -> List[int]:

    def add_description(self) -> str:


class CSVDataset(GenericDataset):

    def __init__(self, dataset:Any = None, target: Any = None):
        self._path = None
        self._dataset = dataset  # case where dataset is passed as pd.dtafarme
        self._target = target

    def set_path(self, path: str):
        self._path = path

    def read(self, **kwargs):
        self._dataset = CSVReader().read(self._path, **kwargs)

    def to_pytorch(self):
        # return a pytorch dataset
        class TabularDataset(torch.Dataset):
            def __init__(self, dataset, target = None):
                self._dataset = dataset
                self._target = target
            def __len__(self):
                return len(self._target)
            
            def __getitem__(self, idx):

                return self._dataset[idx], self._target[idx]
            
        return TabularDataset(self._dataset, self._target)
            
    def to_sklearn(self):

        return self._dataset.to_sklearn(), self._target.to_sklearn()
        
    def shape(self) -> List[int]:

    def add_description(self) -> str:

class ImageFolder(GenericDataset):
    def __init__(self):
        self._folder_path = []


class NiftiiImageFolder(ImageFolder):
    def read(self, path):
        return

class MedicalFolderDataset(DataLoadingPlanMixin, GenericDataset):
    pass


class MedicalFolderController:
    pass