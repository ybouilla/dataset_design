# Scheme for the redesign of `Dataset` class

**disclaimer**: This repos is merly a scheme for the redesign of `Dataset` class, it cannot be used "as is", as it is lacking fedbiomed classes.
This work is WIP

## 1. Goal 1: make it extendable to other kind of datasets

one can include a `BidsDataset` for instance


## 2. Goal 2: extend it to other frameworks

minor modifications on the FrameworkNativeDataset, DatasetManager are expected to include other machine learning frameworks such as tensorflow
For that, One also has to create a `TensorflowDataManager`, `TensorFlowTrainingPlan`

## 3. Limit 3rd dependecies in `Dataset` object and sub-classes
- only call third parties libraries in the `Reader` objects, leaving `Dataset` as generic as possible.

## 4. prepare for Federated Analytics

`Dataset` can be in charge of computing simple statistcis
we can imagine methods such as
 - `NativeImageDataset.mean()` that returns the mean of image knowing the data are images
 - converts data into a generic data type so we can easly perform statistics.

## 5. Unified  Dataset API:
    user should not modify his/her code wrt the frmework used (eg do specific things for toprch, sklearn)

## Explaination: a big picture

### A. Training Plan
1. `DataManager` loads dataset (can be either a Fedbiomed dataset or a framework specific dataset). ( `round` calls `DataManager` in order to a) load the data and to b) split the data into a training and testing data loaders)

3. depending on the type of dataset recieved, `DataManager` either convert the dataset into a) `FrameworkNativeDataset` ot b) `StructuredDataset`

4. `FrameworkNativeDataset`  identifies from the type of `dataset` the format of dataset used (csv, images, ...). For `StructuredDataset` it is transparent

5. `DataManager` gets access in `Round` to the training plan type, and loads the `GenericDataset` into a `TorchDataManager` or `SklearnDataManager` given the type of training Plan. 

6. `DataManager` a) converts dataset into the appropriate framework and b) splits dataset into a training and testing data set. Splitting is only possible if dataset is converted in the appropriate ml framework.
For `FrameworkNativeDataset`, converters are included in the `Dataset`, whereas for `StructuredDataset`, it relies on a Generic converter (to seperate 3rd parties calls from `StructuredDataset`).

7. for both training and testing dataset, `GenericDataManager` loads the splitted `GenericDataset` ( testing/ training splits) into the framework specific `DataLoader`, so it can directly be used by torch or sklearn models.



### B. Loading Dataset into the Node

To investigate
basic idea is to call readers and controllers.
for imagefolder, both torch and tensorflow has their own implementation. 
...


### C. Loading Dataset through GUI
currently, code is splitted among:
 - middleware
 - specific routes

 such splitting looks not very clear to me

### C. Specificities of the `Converter`

Converter convertd from one framework to another

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


### 4. Loading from a custom pytorch dataset (`FrameworkNativeDataset`)

```python
class TrainingPlan:
    class CelebaDataset(Dataset):
        """Custom Dataset for loading CelebA face images"""


        def __init__(self, txt_path, img_dir, transform=None):

            # Read the csv file that includes classes for each image
            df = pd.read_csv(txt_path, sep="\t", index_col=0)
            self.img_dir = img_dir
            self.txt_path = txt_path
            self.img_names = df.index.values
            self.y = df['Smiling'].values
            self.transform = transform

        def __getitem__(self, index):
            img = np.asarray(Image.open(os.path.join(self.img_dir, self.img_names[index])))
            img = transforms.ToTensor()(img)
            label = self.y[index]
            return img, label

        def __len__(self):
            return self.y.shape[0]

    def training_data(self):
        # The training_data creates the dataset and returns DataManager to be used for training in the general class Torchnn of Fed-BioMed
        dataset = self.CelebaDataset(
            os.path.join(self.dataset_path, "target.csv"), os.path.join(self.dataset_path, "data")
            )
        loader_arguments = { 'shuffle': True}
        return DataManager(dataset, **loader_arguments)

```

### 4. Loading from a medical folder dataset


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


### 5. Loading from Flamby dataset