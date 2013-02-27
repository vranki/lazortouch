import QtQuick 1.1

Item {
    width: parent.width/3
    height: parent.height/3
    property string text: ""
    Rectangle {
        color: "black"
        opacity: 0.5
        anchors.fill: parent
    }
    Text {
        color: "white"
        font.pointSize: 25
        anchors.fill: parent
        text: parent.text
    }
}
