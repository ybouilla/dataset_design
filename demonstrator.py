# demonstrate the use of a generic converter
import torch
import numpy as np
import pandas as pd

from converter import GenericConverter

class MyDataset:
    def __init__(self):
        self._data1 = np.array([1, 2, 3, 4])
        self._data2 = {'a': [1, 2, 3, 4, 5], 'b': [1, 2, 3, 4, 5]}
        self._data2 = pd.DataFrame.from_dict(self._data2)
    
    # @GenericConverter.to_torch
    # @GenericConverter.from_sklearn
    @GenericConverter.to_generic
    @GenericConverter.from_pandas
    def _to_dataset(self, data):
        return data
    
    def to_dataset(self):
        # features direct convertion sklearn -> pytorch
        print("starting", self._data1)
        dataset = self._to_dataset(self._data1)
        print("ending", dataset)
        return dataset



if __name__ == "__main__":

    def decor1(func): 
        def inner(): 
            print("GHJK")
            x = func() 
            return x * x 
        return inner 

    def decor2(func): 
        def inner(): 
            print("kls")
            x = func() 
            return 2 * x 
        return inner 

    @decor1
    @decor2
    def num(): 
        return 10

    @decor2
    @decor1
    def num2():
        return 10
    
    print(num())
    MyDataset().to_dataset()