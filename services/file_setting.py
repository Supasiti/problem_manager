class FileSetting():
    # contains all data related to file paths 

    def __init__(self, content_path:str):
        self._content_path = content_path

    @property
    def content_path(self) -> str:
        return self._content_path

