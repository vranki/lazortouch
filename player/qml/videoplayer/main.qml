import QtQuick 1.1
import Qt 4.7
import QtMultimediaKit 1.1
Rectangle {
    width: 640
    height: 400
    color: "black"
    function playFile(filenum) {
        nextVideoNum = filenum
        if(filenum > 0) {
            nextVideoTimer.restart()
        } else {
            nextVideoTimer.stop()
        }
    }
    property int nextVideoNum: 0
    property int videoCount: 0
    property string videoPath: ""
    Video {
        id: videoElement
        anchors.fill: parent
        focus: true
        playing: false
        Keys.onEscapePressed: Qt.quit()
        Image {
            id: overlayImage
            source: videoPath + "/overlay.png"
            visible: nextVideoTimer.running
        }
    }
    Timer {
        id: nextVideoTimer
        interval: 5000
        onTriggered: {
            videoElement.source = videoPath + "/" + nextVideoNum
            videoElement.playing = true
        }
    }
}
