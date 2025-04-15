
class TrainingPlan:

    def training_data(self):
        # user defined TP

        # 1. loading from csv
        csv = pd.read_csv(self.dataset_path, delemiter=";")

        return DataManager(csv[1, :], csv[0])
    


