import pandas as pd

class GenericReader:
    pass



class ImageReader(GenericReader):
    def __init__(self):
        self._reader = MonaiImageReader

    def read(self, path: str, **kwargs):
        return self._reader(path, **kwargs)



class CSVReader(GenericReader):
    def __init__(self):
        self._reader = pd.read_csv
    
    def read(self, path, **kwargs):
        return self._reader(path, **kwargs)


