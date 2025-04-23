# QUestions related to design

1. data type: it has been made clear that we don't want to import libraries for representing data in dataset generic classes. But there is a need to convert data into a generic format in order to switch from one datatype to another (eg from pandas to pytorch). I think numpy should be previliged as a standard format over plain python lists (for efficiency reasons)


2. Regarding MedicalFolderDataset design

2.1 Why `data_modality` in the `__init__` defaults to `"T1"`? is there any good reasons?


3. Imagine a `Dataset` like for numpy, using a `__get_item__` method