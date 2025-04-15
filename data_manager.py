from typing import Any, Dict, Union


class GenericDataManager:
    pass

class SklearnDataManager(GenericDataManager):
    def __init__(self, dataset: Any, dataloader_kwargs: Dict = None, reader_kwargs: Dict = None):
        self._dataset = dataset
    
    def split(self):
        pass


class TorchDataManager(GenericDataManager):
    def process(self):
        if isinstance(dataset, pandas):
            dataset = CSVDataset(dataset)

class DataManager:
    # wrapper of SklearnDataManager / TorchDataManager

    def __init__(self, dataset: Any, dataloader_kwargs: Dict = None, reader_kwargs: Dict = None):
        self._tp_type = None
        self._dataset = dataset
        self._dataloader_kwargs = dataloader_kwargs
        self._reader_kwargs = reader_kwargs

    def set_tp_type(self, tp_type):
        self._tp_type = tp_type

    def load(self) -> Union[TorchDataManager, SklearnDataManager]:
        if self._tp_type is TorchTrainingPlan:
            return TorchDataManager(self._dataset, self._dataloader_kwargs, self._reader_kwargs)
        
        elif self._tp_type is SklearnTrainijngPlan:
            return SklearnDataManager(self._dataset, self._dataloader_kwargs, self._reader_kwargs)




