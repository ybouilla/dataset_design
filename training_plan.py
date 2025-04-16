
from typing import Dict, Iterator


class TrainingPlan:

    def training_data(self):
        # user defined TP

        # 1. loading from csv
        csv = pd.read_csv(self.dataset_path, delemiter=";")

        return DataManager(csv[1, :], csv[0])
    


class SKLearnTrainingPlan(BaseTrainingPlan):

    ...

    def set_data_loaders(self, train_data_loader: SklearnDataLoader | None, test_data_loader: SklearnDataloader | None):
        self.training_data_loader = train_data_loader
        self.testing_data_loader = test_data_loader



class TorchTrainingPlan(BaseTrainingPlan):
    ...
    def set_data_loaders(self, train_data_loader: TorchDataLoader | None, test_data_loader: SklearnDataloader | None):
        self.training_data_loader = train_data_loader
        self.testing_data_loader = test_data_loader


    def training_routine(self, history_monitor = None, node_args: Dict | None = None):
        ...

        training_data_iter: Iterator = iter(self.training_data_loader)