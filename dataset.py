from typing import Any
from reader import CSVReader


class GenericDataset:
    pass

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
        pass

    def to_sklearn(self):
        return self._dataset.to_sklearn()
        

class ImageFolder(GenericDataset):
    def __init__(self):
        pass
