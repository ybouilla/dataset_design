import pandas as pd
from monai.transforms import LoadImage, ToTensor, Compose


class GenericReader:
    def read(self, path):
        pass
    pass



class ImageReader(GenericReader):
    def __init__(self):
        self._reader = Compose([
            LoadImage(ITKReader(), image_only=True),
            ToTensor()
        ])

    def read(self, path: str, **kwargs):
        return self._reader(path, **kwargs)



class CSVReader(GenericReader):
    def __init__(self):
        self._reader = pd.read_csv
    
    def read(self, path, **kwargs):
        return self._reader(path, **kwargs)
    



