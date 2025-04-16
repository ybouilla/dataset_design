# Scheme for the redesign of `Dataset` class

**disclaimer**: This repos is merly a scheme for the redesign of `Dataset` class, it cannot be used "as is", as it is lacking fedbiomed classes.
This work is WIP

## 1. Goal 1: make it extendable to other kinf of datasets

one can include a `BidsDataset` for instance


## 2. Goal 2: extend it to other frameworks

minor modifications on the FrameworkNativeDataset, DatasetManager are expected to include other machine learning frameworks such as tensorflow
One also has to create a `TensorflowDataManager`

## 3. Limit dependecies in Dataset object and sub-classes


## 4. prepare for Federated Analytics
## Explaination: a big picture

1. `DataManager` loads dataset (can be either a Fedbiomed dataset or a framework specific dataset). ( `round` calls `DataManager` in order to a) load the data and to b) split the data into a training and testing data loaders)

3. depending on the type of dataset recieved, `DataManager` either convert the dataset into a) `FrameworkNativeDataset` ot b) `StructuredDataset`

4. `FrameworkNativeDataset`  identifies from the type of `dataset` the format of dataset used (csv, images, ...). For `StructuredDataset` it is transparent

5. `DataManager` gets access in `Round` to the training plan type, and loads the `GenericDataset` into a `TorchDataManager` or `SklearnDataManager` given the type of training Plan. 

6. `GenericDataManager` loads the `GenericDataset` into the franework specific `DataLoader`. Here happens the convertion from a `Generic data type` into a pytorch or sklearn object

7. `DataManager` splits dataset into a training and testing data loader




## Uses cases

### 1. Loading a csv file (`FrameworkNativeDataset`)

**User input**:
```python
class TrainingPlan:

    def training_data(self):
        # user defined TP

        # 1. loading from csv
        csv = pd.read_csv(self.dataset_path, delemiter=";")

        return DataManager(csv[1, :], csv[0])

```

### 2. Loading a Mnist dataset / Image folder (`FrameworkNativeDataset`)


```python
class TrainingPlan:
    def training_data(self):
        transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.1307,), (0.3081,))])
        dataset1 = datasets.MNIST(self.dataset_path, train=True, download=False, transform=transform)
        loader_arguments = { 'shuffle': True}
        return DataManager(dataset1, **loader_arguments)
```

### 3. Loading a MedNist dataset form MONAI (`FrameworkNativeDataset`)


```python
class TrainingPlan:
    def training_data(self):
    # The training_data creates the Dataloader to be used for training in the general class Torchnn of fedbiomed
        common_shape = (48, 60, 48)
        training_transform = Compose([AddChannel(), Resize(common_shape), NormalizeIntensity(),])
        target_transform = Compose([AddChannel(), Resize(common_shape), AsDiscrete(to_onehot=2)])

        mfd = MedicalFolderDataset()
        dataset = mfd.read(
            root=self.dataset_path,
            data_modalities='T1',
            target_modalities='label',
            transform=training_transform,
            target_transform=target_transform,
            demographics_transform=UNetTrainingPlan.demographics_transform)
        loader_arguments = { 'shuffle': True}

        return DataManager(dataset, **loader_arguments)

```


### 4. Loading from a medical folder dataset

### 5. Loading from Flamby dataset