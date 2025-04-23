from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
from converter import GenericConverter
from data_loading_plan import DataLoadingPlanMixIn
from dataloader import NPDataLoader
from reader import CSVReader, ImageReader

import pandas as pd
import torch

class GenericDataset:
    @abstractmethod
    def shape(self):
    @abstractmethod
    def add_sescription(self):
        pass
    @abstractmethod
    def add_description(self):
        # returns shape and other information about the dataset

    @abstractmethod
    def to_pytorch(self) -> torch.Dataset:
        # return a pytorch Dataset that checks all the requirements to 
        # be used in a torch.DataLoader
        pass

    @abstractmethod
    def to_sklearn(self) -> NPDataLoader:
        pass

    @abstractmethod
    def get_dataset_type(self):
        pass 


class Statistics:
    # preparing Federated Analytics
    @abstractmethod
    def mean(self):
    @abstractmethod
    def histogram(self):


class FrameworkNativeDataset:
    # wrapper for dataset that has been implemented in a specific framework, and is reused in FBM
    def __init__(self, dataset: Union[Tuple[Any, Any], Any],
                 target: Optional[Any] = None, kwargs_loader: Optional[Dict] = None, kwargs_reader: Optional[Dict]=None):
        self._dataset = dataset
        self._target = target

    def process(self):
        if isinstance(self._dataset, (pd.Series, pd.DataFrame, np.ndarray)):
            self._dataset = CSVDataset(self._dataset, self._target)

        elif isinstance(self._dataset, torchvision.ImageFolder):
            self._dataset = NativeImageDataset(self._dataset)

        elif isinstance(self._dataset, (torch.Dataset,  monai.data.Dataset)):
            self._dataset = NativeCustomDataset(self._dataset)

    def shape(self) -> List[int]:
        # need process to be executed first
        return self._dataset.shape()
    def add_description(self) -> str:
        # need process to be executed first
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


class NativeGenericDataset(DataLoadingPlanMixIn, GenericDataset):
    def __init__(self, dataset: torch.Dataset, target = None):
        self._dataset = dataset
    def to_pytorch(self):

        return self._dataset
    
    def to_sklearn(self):
            # TODO: implement conversion from pytorch to sklearn
        return self._dataset

class NativeImageDataset(NativeGenericDataset):
    def __init__(self, dataset: torch.Dataset, target = None):
        self._dataset = dataset

    def mean(self):
        # for federated analytics
        return 
    
    def histogram(self):
        return


class NativeCustomDataset(NativeGenericDataset):
    def __init__(self, dataset: torch.Dataset, target = None):
        self._dataset = dataset

    def mean(self):
        # user has to implement `mean` by himself/herself
        raise

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
                self._dataset = torch.as_tensor(dataset)
                self._target = torch.as_tensor(target)
            def __len__(self):
                return len(self._target)
            
            def __getitem__(self, idx):

                return self._dataset[idx], self._target[idx]
            
        return TabularDataset(self._dataset, self._target)
            
    def to_sklearn(self):

        return self._dataset.to_sklearn(), self._target.to_sklearn()
        
    def shape(self) -> List[int]:

    def add_description(self) -> str:

class ImageFolder(DataLoadingPlanMixIn, GenericDataset):
    def __init__(self):
        self._folder_path = []

    def read(self, path):
        self._reader = ImageReader()
        return self._reader(path)

class NiftiiImageFolder(ImageFolder):
    def read(self, path):
        pass
        return self._reader(path)

class MedicalFolderDataset(DataLoadingPlanMixIn, GenericConverter, GenericDataset):
    
    def __init__(self, tabular_file, index_col, data_modalities, target_modalities):
        self._datasets = {}
        self._dlp = None

        self._tabular_file = tabular_file
        self._index_col = index_col

        self._data_modalities = [data_modalities] if isinstance(data_modalities, str) else data_modalities
        self._target_modalities = [target_modalities] if isinstance(target_modalities, str) else target_modalities

        self._transform


        self._tp_type = None
     
    def _check_and_reformat_transforms(self):
        # applies data loading plan
        pass
    
    def read(self, img_path, demographic_path):

        imgs = self._read_images(img_path)
        if demographic_path:
            demographics = CSVReader().read(demographic_path)
        return imgs, demographics

    def _read_images(self, path):
        subjects = {}
        for modality in modalities:
            img_folder = ImageFolder().read(path_modality)
            subjects[modality] = img_folder
        return subjects

    def validate(self, img_path, demographic_path):
        pass

    def to_standard(self):
        # returns a dataset in the standard format
        pass


    def __getitem__(self, idx):
        (data, demographics), targets = self.get_nontransformed_item(idx)

        # Apply transforms to data elements
        if self._transform is not None:
            for modality, transform in self._transform.items():
                try:
                    data[modality] = self.from_torch_to_framework(transform(data[modality]))
                except Exception as e:
                    raise 
        # Apply transforms to demographics elements
        if self._demographics_transform is not None:
            try:
                demographics = self.from_pandas_to_framework(self._demographics_transform(demographics))
            except Exception as e:
                raise 
        # Try to convert demographics to tensor one last time
        if isinstance(demographics, dict) and len(demographics) == 0:
            demographics = None# torch.empty(0)  # handle case where demographics is an empty dict
            # FIXME: would it be better by returning None instead of `torch.empty(0)`
        

        # Apply transform to target elements
        if self._target_transform is not None:
            for modality, target_transform in self._target_transform.items():
                try:
                    targets[modality] = self.from_torch_to_framework(target_transform(targets[modality]))
                except Exception as e:
                    raise
        return (data, demographics), targets
    
    def set_framework(self, tp_type):
        self._tp_type = tp_type

    @GenericConverter.to_torch
    @GenericConverter.from_pandas
    def _pandas_to_pytorch(self, data):

    def to_pytorch(self, data):
        self.from_torch_to_framework = lambda x: x
        self.from_pandas_to_framework = self._pandas_to_pytorch # or directly `TorchConverter.from_standard()`