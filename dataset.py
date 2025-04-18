from typing import Any, Dict, List, Optional, Tuple, Union
from converter import GenericConverter
from reader import CSVReader, ImageReader

import pandas as pd
import torch

class GenericDataset:
    
    def shape(self):
    
    def add_description(self):
        # returns shape and other information about the dataset


    def to_pytorch(self):
        # return a pytorch Dataset that checks all the requirements to 
        # be used in a torch.DataLoader
        pass



class FrameworkNativeDataset:
    # wrapper for dataset that has been implemented in a specific framework, and is reused in FBM
    def __init__(self, dataset: Union[Tuple[Any, Any], Any],
                 target: Optional[Any] = None, kwargs_loader: Optional[Dict] = None, kwargs_reader: Optional[Dict]=None):
        self._dataset = dataset
        self._target = target

    def process(self):
        if isinstance(self._dataset, (pd.Series, pd.DataFrame)):
            self._dataset = CSVDataset(self._dataset, self._target)

        elif isinstance(self._dataset, torchvision.ImageFolder):
            self._dataset = NativeImageDataset(self._dataset)

        elif isinstance(self._dataset, (torch.Dataset,  monai.data.Dataset)):
            self._dataset = NativeCustomDataset(self._dataset)

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


class NativeGenericDataset(GenericDataset):
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
                self._dataset = torch.Tensor(dataset.to_numpy())
                self._target = torch.Tensor(target.to_numpy())
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

    def read(self, path):
        self._reader = ImageReader()
        return self._reader(path)

class NiftiiImageFolder(ImageFolder):
    def read(self, path):
        pass
        return self._reader(path)

class MedicalFolderDataset(DataLoadingPlanMixin, GenericConverter, GenericDataset):
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


