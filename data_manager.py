from typing import Any, Dict, Tuple, Union

from dataloader import SklearnDataLoader, TorchDataLoader
from dataset import FrameworkNativeDataset, GenericDataset, StructuredDataset


class GenericDataManager:
    pass

class SklearnDataManager(GenericDataManager):
    def __init__(self, dataset: Union[FrameworkNativeDataset, StructuredDataset], dataloader_kwargs: Dict = None, reader_kwargs: Dict = None):
        self._dataloader = SklearnDataLoader(dataset)

    
    def split(self) -> Tuple[SklearnDataLoader, SklearnDataLoader]:
        pass


class TorchDataManager(GenericDataManager):
    def __init__(self, dataset: Union[FrameworkNativeDataset, StructuredDataset], dataloader_kwargs: Dict = None, reader_kwargs: Dict = None):
        self._dataloader = TorchDataLoader(dataset)
    def split(self) -> Tuple[torch.DataLoader, torch.DataLoader]:
        ...



class DataManager:
    # wrapper of SklearnDataManager / TorchDataManager

    def __init__(self, dataset: Any, dataloader_kwargs: Dict = None, reader_kwargs: Dict = None):
        self._tp_type = None
        self._dataset = dataset
        self._dataloader_kwargs = dataloader_kwargs
        self._reader_kwargs = reader_kwargs


    def process(self):
        if isinstance(self._dataset, GenericDataset):
            self._dataset = StructuredDataset(self._dataset)
        else:
            self._dataset = FrameworkNativeDataset(self._dataset)

    def set_tp_type(self, tp_type):
        self._tp_type = tp_type

    def load(self) -> Union[TorchDataManager, SklearnDataManager]:
        self.process()

        if self._tp_type is TorchTrainingPlan:
            
            self._dataset = TorchDataManager(self._dataset, self._dataloader_kwargs, self._reader_kwargs)
        
        elif self._tp_type is SklearnTrainingPlan:
            self._dataset = SklearnDataManager(self._dataset, self._dataloader_kwargs, self._reader_kwargs)




