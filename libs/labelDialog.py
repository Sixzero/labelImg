try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import newIcon, labelValidator

BB = QDialogButtonBox

class CustomQCompleter(QCompleter):
    def __init__(self, parent=None):
        super(CustomQCompleter, self).__init__(parent)
        self.local_completion_prefix = ""
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        super(CustomQCompleter, self).setModel(self.source_model)

    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix
        class InnerProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                searchStr = local_completion_prefix.lower()
                modelStr = self.sourceModel().data(index0,Qt.DisplayRole).lower()
                # print(searchStr,' in ',modelStr, searchStr in modelStr)
                return searchStr in modelStr


        proxy_model = InnerProxyModel()

        proxy_model.setSourceModel(self.source_model)

        super(CustomQCompleter, self).setModel(proxy_model)
        print('match :', proxy_model.rowCount())


    def splitPath(self, path):
        self.local_completion_prefix = str(path)
        self.updateModel()
        return ""

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = CustomQCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

        self.edit.setCompleter(completer)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)

        self.editAmount = QLineEdit()
        layout.addWidget(self.editAmount)

        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    def postProcessAmount(self):
        try:
            self.props['amount'] = self.editAmount.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.props['amount'] = self.editAmount.text()

    def popUp(self, text='', move=True, amount=''):
        self.edit.setText(text)
        self.editAmount.setText(amount)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return (self.edit.text(), {'amount': self.editAmount.text()}) if self.exec_() else (None, None)

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)

    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()
