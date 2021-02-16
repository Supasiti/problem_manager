import os

from services.signal import Signal

class ContentsPathManager():
    # maintains 
    #  - current directory
    #  - filepath of the set on screen
    #  - filename to save

    filepathChanged   = Signal(str)
    _filepath         : str
    _directory        : str
    _filename_to_save : str

    def __init__(self):
        pass

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value:str):
        self._filepath = value
        self.filepathChanged.emit(value)
    
    @property
    def filename_to_save(self):
        return self._filename_to_save

    @filename_to_save.setter
    def filename_to_save(self, value:str):
        self._filename_to_save = value

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value:str):
        if self._validate_directory(value):
            self._directory = value
            self.filepath = self._latest_set_filepath()

    def _validate_directory(self, directory:str):
        json_dir = os.path.join(directory, 'current')
        return os.path.isdir(json_dir)    # true if exist
    
    @property
    def current_dir(self):
        return os.path.join(self.directory, 'current')

    def _latest_set_filepath(self):
        json_files  = self._json_filter(self.current_dir)
        if len(json_files) > 0:
            json_files.sort(reverse=True)
            latest_file = json_files[0]
            return os.path.join(self.current_dir, latest_file)
        return ''

    def _json_filter(self, directory: str):
        if os.path.isdir(directory): 
            return [path for path in os.listdir(directory) if path.endswith('.json')]
        return []

    def filepath_to_save(self):
        filename = self.filename_to_save
        if filename != '':
            _filename = filename + '.json'
            return os.path.join(self.current_dir, _filename)
            
    def get_filename(self, filepath:str):
        filename = os.path.basename(filepath)
        return filename.split('.')[0]