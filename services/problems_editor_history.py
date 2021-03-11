from abc import ABC, abstractmethod
from datetime import datetime

from services.problems_editor import ProblemsEditor


# class Snapshot(ABC):

#     @abstractmethod
#     def get_timestamp(self) -> str:
#         pass 


# class EditorSnapshot(Snapshot):

#     def __init__(self, init:dict, to_add:dict, to_remove:dict, next_id:int) ->None:
#         self._problems_init     = init  
#         self._problems_to_add   = to_add  
#         self._problems_to_strip = to_remove
#         self._next_id           = next_id
#         self._timestamp         = str(datetime.now())[:19]


#     def get_timestamp(self) -> str:
#         return self._timestamp

#     @property
#     def problems_init(self) -> dict:
#         return self._problems_init
    
#     @property
#     def problems_to_add(self) -> dict:
#         return self._problems_to_add
    
#     @property
#     def problems_to_strip(self) -> dict:
#         return self._problems_to_strip

#     @property
#     def next_id(self) -> int:
#         return self._next_id


class ProblemsEditorHistory():
    # new snapshot is insert at index 0 = current saved view 
    # previous snapshot is at index 1

    def __init__(self, editor:ProblemsEditor) -> None:
        self._snapshots = []
        self._index     = 1  # index to revert to  
        self._editor = editor
        

    def backup(self):
        self._snapshots = self._snapshots[self._index -1:]
        self._snapshots.insert(0, self._editor.save_snapshot())
        self._index = 1

    def undo(self):
        # will try to undo until it can, else do nothing
        if self._index > len(self._snapshots) - 1:
            return
        index = self._index
        self._index += 1  
        try:
            self._editor.restore_from(self._snapshots[index])
        except Exception:
            self.undo()
    
    def redo(self):
        if self._index >1:
            self._index -= 1
            self._editor.restore_from(self._snapshots[self._index-1])
    
    def clear(self):
        self._snapshots = []
        self._index     = 1 

