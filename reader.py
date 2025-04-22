import pandas as pd
from monai.transforms import LoadImage, ToTensor, Compose


class GenericReader:
    # usually implementation is defined in `Node.DatasetManager`
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
        sniffer = csv.Sniffer()
        with open(path, 'r') as file:
            delimiter = sniffer.sniff(file.readline()).delimiter
            file.seek(0)
            header = 0 if sniffer.has_header(file.read()) else None

        return pd.read_csv(csv_file, index_col=index_col, sep=delimiter, header=header)
        return self._reader(path, **kwargs)
    



