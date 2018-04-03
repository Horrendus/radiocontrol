import sys

import random

from PySide2.QtQml import QQmlApplicationEngine

from PySide2.QtCore import QAbstractListModel, QTimer
from PySide2.QtGui import QGuiApplication


class PlaylistModel(QAbstractListModel):

    _COLUMNS = ('name', 'length')

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == self._COLUMNS.index('name'):
            return d['name']
        if role == self._COLUMNS.index('length'):
            return d['length']
        return None

    def roleNames(self):
        return dict(enumerate(self._COLUMNS))

    def populate(self):
        self._data = []
        for i in range(5):
            playlist_name = f"PL{random.randint(1, 35)}"
            playlist_length = random.randint(35, 70)
            self._data.append({"name": playlist_name, "length": playlist_length})
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(len(self._data)-1, 0))


def main():
    random.seed()

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    timer = QTimer()
    timer.start(1500)

    playlist_model = PlaylistModel(engine)
    playlist_model.populate()

    timer.timeout.connect(playlist_model.populate)

    engine.rootContext().setContextProperty("playlistModel", playlist_model)
    engine.load('playlists_view.qml')

    app.exec_()


if __name__ == '__main__':
    main()
