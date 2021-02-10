import os

class PathBuilder():
    # build correct paths I/O - util

    def get_latest_gym_filepath(self, directory:str):

        json_dir    = self.__current_dir(directory)
        json_files  = self.__json_filter(json_dir)
        if len(json_files) > 0:
            json_files.sort(reverse=True)
            latest_file = json_files[0]
            return os.path.join(json_dir, latest_file)
        return ""

    def __current_dir(self, directory: str):
        return os.path.join(directory, 'current')

    def __json_filter(self, directory: str):
        if os.path.isdir(directory): 
            return [path for path in os.listdir(directory) if path.endswith('-problems.json')]
        return []