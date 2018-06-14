import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0

ApplicationWindow {
    title: qsTr("Radiocontrol QML UI")
    id: appWindow
    width: 1920
    height: 1080
    visible: true

    RowLayout {
        Column {
            id: playlistsColumn
            width: 100
            height: appWindow.height

            Button {
                text: "Refresh"
                onClicked: playlistModel.populate()
            }

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
                        wrapMode: Text.WordWrap
                        width: parent.width
                    }
                }
            }
        }
        Column {
            id: mainColumn

            RowLayout {
                Column {
                    Text {
                        text: cal.selectedDate
                    }
                    TextField{
                        id:textEditTD
                        text : "00:00"
                        inputMask: "99:99"
                        inputMethodHints: Qt.ImhDigitsOnly
                        validator: RegExpValidator { regExp: /^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$ / }

                        width:100
                        height:50
                    }
                }

                Button {
                    text: "Show Calendar"
                    onClicked: cal.visible = true
                    height: 50
                    width: 50
                }

                Calendar {
                    id: cal
                    minimumDate: new Date()
                    maximumDate: new Date(2080, 1, 1)
                    visible: false
                    onClicked: visible = false
                }

                Button {
                    text: "New ScheduleEntry"
                    height: 50
                    width: 100
                    onClicked: scheduleEntryDate.text = "new date"
                }

                Text {
                    id: scheduleEntryDate
                    text: "no date"
                }
            }
        }
    }
}
