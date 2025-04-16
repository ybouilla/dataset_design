


class Round:

    ...

    def _set_training_testing_data_loaders(self):
        """
        Method for setting training and validation data loaders based on the training and validation
        arguments.
        """

        # Set requested data path for model training and validation
        self.training_plan.set_dataset_path(self.dataset['path'])

        # Get validation parameters
        test_ratio = self.testing_arguments.get('test_ratio', 0)
        self.is_test_data_shuffled = self.testing_arguments.get('shuffle_testing_dataset', False)
        test_global_updates = self.testing_arguments.get('test_on_global_updates', False)
        test_local_updates = self.testing_arguments.get('test_on_local_updates', False)

        # Inform user about mismatch arguments settings
        if test_ratio != 0 and test_local_updates is False and test_global_updates is False:
            logger.warning("Validation will not be performed for the round, since there is no validation activated. "
                           "Please set `test_on_global_updates`, `test_on_local_updates`, or both in the "
                           "experiment.",
                           researcher_id=self.researcher_id)

        if test_ratio == 0 and (test_local_updates is True or test_global_updates is True):
            logger.warning(
                'Validation is activated but `test_ratio` is 0. Please change `test_ratio`. '
                'No validation will be performed. Splitting dataset for validation will be ignored',
                researcher_id=self.researcher_id
            )

        # Setting validation and train subsets based on test_ratio
        training_data_loader, testing_data_loader = self._split_train_and_test_data(
                test_ratio=test_ratio,
                #random_seed=rand_seed
            )
        # Set models validating and training parts for training plan
        self.training_plan.set_data_loaders(train_data_loader=training_data_loader,
                                            test_data_loader=testing_data_loader)
        
    def _split_train_and_test_data(self, test_ratio: float = 0) -> DataManager:
        # FIXME: incorrect type output
        """
        Method for splitting training and validation data based on training plan type. It sets
        `dataset_path` for training plan and calls `training_data` method of training plan.

        Args:
            test_ratio: The ratio that represent validating partition. Default is 0, means that
                            all the samples will be used for training.

        Raises:

            FedbiomedRoundError: - When the method `training_data` of training plan
                                    has unsupported arguments.
                                 - Error while calling `training_data` method
                                 - If the return value of `training_data` is not an instance of
                                   `fedbiomed.common.data.DataManager`.
                                 - If `load` method of DataManager returns an error
        """

        training_plan_type = self.training_plan.type()  # FIXME: type is not part of the BaseTrainingPlan API
        try:
            data_manager = self.training_plan.training_data()
        except TypeError as e:
            pass

        # Set loader arguments
        data_manager.extend_loader_args(self.loader_arguments)

        # Specific datamanager based on training plan
        try:
            data_manager.set_tp_type(tp_type=training_plan_type)
            # This data manager can be data manager for PyTorch or Sk-Learn
            data_manager.load()

        except FedbiomedError as e:
            raise
        # Get dataset property

        # For MedicalFolderDataset
        if hasattr(data_manager.dataset, "set_dataset_parameters"):
            dataset_parameters = self.dataset.get("dataset_parameters", {})
            data_manager.dataset.set_dataset_parameters(dataset_parameters)

        if self._dlp_and_loading_block_metadata is not None:
            if hasattr(data_manager.dataset, 'set_dlp'):
                dlp = DataLoadingPlan().deserialize(*self._dlp_and_loading_block_metadata)
                data_manager.dataset.set_dlp(dlp)
            else:
                raise FedbiomedRoundError(f"{ErrorNumbers.FB314.value}: Attempting to set DataLoadingPlan "
                                          f"{self._dlp_and_loading_block_metadata['name']} on dataset of type "
                                          f"{data_manager.dataset.__class__.__name__} which is not enabled.")

        # All Framework based data managers have the same methods
        # If testing ratio is 0,
        # self.testing_data will be equal to None
        # self.training_data will be equal to all samples
        # If testing ratio is 1,
        # self.testing_data will be equal to all samples
        # self.training_data will be equal to None

        # setting testing_index (if any)
        data_manager.load_state(self._testing_indexes)

        # Split dataset as train and test

        training_loader, testing_loader = data_manager.split(
            test_ratio=test_ratio,
            test_batch_size=self.testing_arguments.get('test_batch_size'),
            is_shuffled_testing_dataset = self.is_test_data_shuffled
        )
        # retrieve testing/training indexes
        self._testing_indexes = data_manager.save_state()

        return training_loader, testing_loader
