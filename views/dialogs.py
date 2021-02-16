from PyQt5.QtWidgets import QMessageBox

class SaveAsDialog(QMessageBox):

    def __init__(self, filename:str, save_command:callable):
        assert(type(filename) == str)
        super().__init__()
        self.setIcon(QMessageBox.NoIcon)
        self.setWindowTitle('Save as')
        self.setText('Save the current set as')
        self.setInformativeText(filename)
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Save)
        self.on_save_clicked = save_command

    def show(self):
        ret = self.exec()
        if ret == QMessageBox.Save:
            self.on_save_clicked()


class SaveDialog(QMessageBox):

    def __init__(self, filename:str, save_command:callable):
        assert(type(filename) == str)
        super().__init__()
        self.setIcon(QMessageBox.NoIcon)
        self.setWindowTitle('Save')
        self.setText('Save the current set')
        self.setInformativeText('This will override the file: {}'.format(filename))
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Save)
        self.on_save_clicked = save_command

    def show(self):
        ret = self.exec()
        if ret == QMessageBox.Save:
            self.on_save_clicked()