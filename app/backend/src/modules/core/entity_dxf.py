from pathlib import Path
from ezdxf.filemanagement import readfile

class EntityDxf:
    def __init__(self, doc_path: Path | str):
        self.doc = readfile(str(doc_path))
        self.msp = self.doc.modelspace()