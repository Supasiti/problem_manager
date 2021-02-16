import os

class PathBuilder():
    # build correct paths I/O - util

    def get_latest_gym_filepath(self, directory:str):

        json_dir    = self.current_dir(directory)
        json_files  = self._json_filter(json_dir)
        if len(json_files) > 0:
            json_files.sort(reverse=True)
            latest_file = json_files[0]
            return os.path.join(json_dir, latest_file)
        return ''

    def current_dir(self, directory: str):
        return os.path.join(directory, 'current')

    def _json_filter(self, directory: str):
        if os.path.isdir(directory): 
            return [path for path in os.listdir(directory) if path.endswith('.json')]
        return []

    def get_filename(self, filepath:str):
        filename = os.path.basename(filepath)
        return filename.split('.')[0]

    def new_gym_filepath(self, directory:str, filename:str):
        _filename = filename + '.json'
        return os.path.join(directory, _filename)