try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from PyQt4 import QtGui,QtCore

import sys

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MyGui(QDialog):

    def __init__(self, parent=None):

        super(MyGui,self).__init__(parent)

        model = QStringListModel()
        wordList = ['John Doe','Jane Doe','Albert Einstein', 'Alfred E Newman']
        model.setStringList(wordList)

        layout = QVBoxLayout(self)
        self.line = QLineEdit(self)
        layout.addWidget(self.line)

        self.combobox = QComboBox(parent)
        layout.addWidget(self.combobox)
        self.combobox.addItems(wordList)
        self.combobox.setEditable(True)

        self.setLayout(layout)

        complete = CustomQCompleter2(self)
        complete.setModel(model)
        complete.setCaseSensitivity(Qt.CaseInsensitive)
        complete.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        complete.setWrapAround(False)

        self.line.setCompleter(complete)
        self.combobox.setCompleter(complete)
        self.combobox.setEditText('')

        self.setGeometry(200, 100, 400, 300)


class CustomQCompleter2(QCompleter):
    def __init__(self, parent=None):
        super(CustomQCompleter2, self).__init__(parent)
        self.local_completion_prefix = ""
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        super(CustomQCompleter2, self).setModel(self.source_model)

    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix
        class InnerProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                searchStr = local_completion_prefix.lower()
                modelStr = self.sourceModel().data(index0,Qt.DisplayRole).lower()
                print(searchStr,' in ',modelStr, searchStr in modelStr)
                return searchStr in modelStr


        proxy_model = InnerProxyModel()

        proxy_model.setSourceModel(self.source_model)

        super(CustomQCompleter2, self).setModel(proxy_model)
        print('match :', proxy_model.rowCount())


    def splitPath(self, path):
        self.local_completion_prefix = str(path)
        self.updateModel()
        return ""

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = MyGui()
    gui.show()
    sys.exit(app.exec_())