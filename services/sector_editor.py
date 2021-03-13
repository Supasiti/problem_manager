
from services.signal import Signal
from services.problem_repository import ProblemRepository
from services.json_writer import JsonWriter

class SectorEditor():
    # handle all sector editing

    sectorsChanged = Signal(bool)

    def __init__(self) -> None:
        self._sectors = dict() # name : col

    def get_col(self, name: str) -> int:
        if name.lower() in self._sectors.keys():
            return self._sectors[name]
        raise ValueError('The sector name does not exist!: {}'.format(name))
    
    def get_sector(self, col:int) -> str:
        keys   = list(self._sectors.keys())
        values = list(self._sectors.values())
        if col in values:
            return keys[values.index(col)]
        raise IndexError('index is out of range.')

    def get_all_sectors(self) -> tuple: 
        return tuple(self._sectors.keys())
        
    def length(self) -> int:
        return len(self._sectors)
        
    def load_sectors(self, repository:ProblemRepository) -> None:  
        self._sectors = repository.get_all_sectors()

    # add sector to left/right of a sector

    def add_sector(self, name:str, col:int) -> None:
        if name in self._sectors.keys():
            raise ValueError('This sector name already exists: {}'.format(name))
        if col < 0:
            raise ValueError('column must be non-negative.')
        if col >= self.length():
            self._sectors[name] = self.length()
        else :
            self._shift_col_up(col, self.length())
            self._sectors[name] = col
        self.sectorsChanged.emit(True)

    # remove sector 
    def remove_sector(self, name:str) -> None:
        if not name in self._sectors.keys():
            raise ValueError('This sector name doesn\'t exist: {}'.format(name))
        col = self.get_col(name)
        self._sectors.pop(name)
        self._shift_col_down(col, self.length())
        self.sectorsChanged.emit(True)
    
    # move sector to index
    def move_sector(self, name:str, col:int) -> None:
        if not name in self._sectors.keys():
            raise ValueError('This sector name doesn\'t exist: {}'.format(name))
        if col < 0 or col >= self.length():
            raise ValueError('cannot move sector outside the range')

        current_col = self._sectors[name]
        if col > current_col:
            self._shift_col_down(current_col, col)
        elif current_col > col:
            self._shift_col_up(col, current_col)
        self._sectors[name] = col
        self.sectorsChanged.emit(True)
    
    def _shift_col_up(self, start:int, end:int) -> None:
        assert ( end > start)
        for key,value in self._sectors.items():
            if value >= start and value < end:
                self._sectors[key] = value + 1

    def _shift_col_down(self, start:int, end:int) -> None :
        assert ( end > start)
        for key,value in self._sectors.items():
            if value > start and value <= end:
                self._sectors[key] = value - 1

    def change_name(self, original:str, change_to:str) -> None:
        if not original in self._sectors.keys():
            raise ValueError('This sector name doesn\'t exist: {}'.format(original))
        if change_to in self._sectors.keys():
            raise ValueError('This sector name already exists: {}'.format(change_to))

        col = self._sectors[original]
        self._sectors.pop(original)
        self._sectors[change_to] = col
        self.sectorsChanged.emit(True)

    def save_sectors(self, writer:JsonWriter):
        writer.set_sectors(self._sectors.copy())