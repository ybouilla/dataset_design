

class GenericConverter:
    # @to_sklearn
    # @from_torch
    # def something(self):

    def __init__(self):

        self._input_type = None
        self._output_type = None
        global _output_type
        global _input_type
        self._fct: list = None

    def process(self,  type_convert):
        pass
    
    @staticmethod
    def to_sklearn( func):
        def wrapper(self, *args, **kwargs):

            global _output_type
            _output_type = 'sklearn'
           
        return wrapper

    @staticmethod
    def to_torch(func):
        
        def wrapper(*args, **kwargs):
            print("-> torch")
            global _output_type
            _output_type = 'torch'
            return args
        
        return wrapper
    @staticmethod
    def to_generic(func):
        def wrapper(*args, **kwargs):
            global _output_type
            
            print("-> generic")
            _output_type= 'generic'

            return func(*args,**kwargs)
        return wrapper

    @staticmethod
    def from_sklearn( func):
        print("HJKL")
        def wrapper12(self, *args, **kwargs):
            print("sklearn ->")
            global _output_type
            if _output_type is None:
                raise
            global _input_type
            _input_type = 'sklearn'
            print('got ', _input_type, _output_type)
            fct = _direct_fct.get(
                _input_type+ '-' +_output_type
            )
            if fct is not None:
                # case where there is a direct way to convert data type
                data = fct(self, *args, **kwargs)
            else:
                fct_output = _direct_fct.get(_output_type)
                fct_input = _direct_fct.get(_input_type)

                data = fct_output(fct_input(self, *args, **kwargs))
            return data
        return wrapper12

    @staticmethod
    def from_pandas( func):
        def wrapper(*args, **kwargs):
            
            print("pandas ->")
            print('out', _output_type)
            return args
            #return func(*args, **kwargs)
        return wrapper
    @staticmethod
    def from_sklearn_to_torch(data):
        # for specific methods, do the import here
        # existing method provided by library
        #return data.to_torch()
        print("used specific fct sklearn-> torch")

        return torch.as_tensor(data)
    @staticmethod
    def from_torch_to_sklearn(data):
        #return from_numpy(data)
        return

class TorchConverter:
    def __init__(self):
        pass
    @staticmethod
    def to_standard(data):
        print(' torch to standard')
    @staticmethod
    def from_standard(data):
        print("from standard to torch")
        # class TorchDataset(pytorch.Dataset):
        #     def __init__(self, data):
        #         self._data = data

        #     def __getitem__(self, idx):
        #         return self._data[idx]

        #     def __len__(self):
        #         return len(data)

        map(torch.as_tensor, data)

    # define here method related to pytorch
    # idea: we import here torch dependencies

# alternative:  use a @register like decorator
_direct_fct = {
            'sklearn_torch' : GenericConverter.from_sklearn_to_torch,
        }

_from_standard = {

    'torch': TorchConverter.from_standard
}



# # code for testing decorator chaining 
# def decor1(func): 
#     def inner(): 
#         x = func() 
#         return x * x 
#     return inner 

# def decor2(func): 
#     def inner(): 
#         x = func() 
#         return 2 * x 
#     return inner 

# @decor1
# @decor2
# def num(): 
#     return 10

# @decor2
# @decor1
# def num2():
#     return 10
  
# print(num()) -> return 400
# print(num2()) -> return 200

# example:
# import torch
# import tensorflow as tf

# pytorch_tensor = torch.zeros(10)
# tf_tensor = tf.convert_to_tensor(pytorch_tensor)

# torchvision image folder equivalent in tensorfkow

# import tensorflow as tf
# import tensorflow_datasets as tfds

# builder = tfds.ImageFolder('/content/image_dir/')
# print(builder.info)  # num examples, labels... are automatically calculated
# ds = builder.as_dataset(split='train', shuffle_files=True)
# tfds.show_examples(ds, builder.info)  

