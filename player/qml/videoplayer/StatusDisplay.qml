import QtQuick 1.1

Text {
    color: "white"
    font.pointSize: 25
    text: parent.text
    Rectangle {
        color: "black"
        opacity: 0.5
        anchors.fill: parent
        z: -1
    }
}
