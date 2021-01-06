from dataclasses import dataclass
from pathlib import Path
@dataclass
class LoadingData:
    full_module_and_class_name: str
    file_path:str

    @property
    def is_file_valid(self):
        return Path(self.file_path).is_file()
