# controller classes
class GenericController:
    def validate(self, path):
        pass

class MedicalFolderController(GenericController):
    def validate(self, path):
       # see validate_MedicalFolder_root_folder
       


class ImageFolderController(GenericController):
    def validate(self, path):
        pass

class CSVController(GenericController):
    def validate(self, path):
        pass