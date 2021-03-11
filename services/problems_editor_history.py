
from services.problems_editor import ProblemsEditor


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

