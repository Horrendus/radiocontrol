import QtQuick 2.7
import QtQuick.Controls 2.0
import QtGraphicalEffects 1.0

ApplicationWindow {
    title: qsTr("Radiocontrol QML UI")
    width: 1920
    height: 1080
    visible: true

    ListView {
        width: 100
        height: 1000
        model: playlistModel
        spacing: 5

        delegate: Rectangle {
            width: 100
            height: model.length
            color: "green"
            Text {
                text: model.name
            }
        }
    }
}
