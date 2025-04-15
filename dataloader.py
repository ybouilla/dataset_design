class GenericDataLoader:
    pass


class TorchDataLoader(GenericDataLoader):
    def __init__(self, dataset):

        self._dataloader = pytorch.dataloader(dataset)
        