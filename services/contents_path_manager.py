import os

from services.signal import Signal

class ContentsPathManager():
    # maintains 
    #  - current directory
    #  - filepath of the set on screen
    #  - filename to save

    filepathChanged   = Signal(str)
    _filepath         : str        # to be used to show all the problems on the screen
    _filenames        : list[str]  # contains all filenames in ../contents/current/
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
    def filename(self):
        return self.get_filename(self.filepath)

    @filename.setter
    def filename(self, value:str):
        name = value + '.json'
        self.filepath = os.path.join(self.current_dir, name)

    @property
    def filenames(self):
        return self._filenames

    @property
    def filename_to_save(self):
        return self._filename_to_save

    @filename_to_save.setter
    def filename_to_save(self, value:str):
        self._filename_to_save = value

    @property
    def filepath_to_save(self):
        filename = self.filename_to_save
        if filename != '':
            _filename = filename + '.json'
            return os.path.join(self.current_dir, _filename)
        return ''

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value:str):
        self._directory = value
        if not self._current_directory_exists(value):
            json_dir = os.path.join(value, 'current')
            os.mkdir(json_dir)
        self.filepath = self._latest_set_filepath()

    def _current_directory_exists(self, directory:str):
        json_dir = os.path.join(directory, 'current')
        return os.path.isdir(json_dir)    # true if exist
    
    @property
    def current_dir(self):
        return os.path.join(self.directory, 'current')

    @property
    def history_dir(self):
        return os.path.join(self.directory, 'history')

    def _latest_set_filepath(self):
        json_files      = self._json_filter(self.current_dir)
        if len(json_files) > 0:
            json_files.sort(reverse=True)
            self._filenames = list([ f.split('.')[0] for f in json_files])
            latest_file     = json_files[0]
            return os.path.join(self.current_dir, latest_file)
        return ''

    def _json_filter(self, directory: str):
        if os.path.isdir(directory): 
            return [name for name in os.listdir(directory) if name.endswith('.json')]
        return []

    def get_filename(self, filepath:str):
        filename = os.path.basename(filepath)
        return filename.split('.')[0]

    def get_filepath_for_stripped_problem(self, name:str) -> str:
        return os.path.join(self.history_dir, name + '.json')