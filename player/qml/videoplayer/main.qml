import QtQuick 1.1
import Qt 4.7
import QtMultimediaKit 1.1
Rectangle {
    id: videoPlayer
    width: 640
    height: 400
    color: "black"
    state: "STOPPED"

    function playFile(filenum) {
        if(nextVideoNum == filenum) return;
        if(filenum > 0) {
            nextVideoNum = filenum
            if(videoElement.playing) {
                state = "CHANGING_SOON"
                nextVideoTimer.restart()
            } else {
                videoElement.source = videoPath + "/" + nextVideoNum
                state = "PLAYING"
                videoElement.playing = true
            }
        } else {
            state = "PLAYING"
            nextVideoTimer.stop()
        }
    }
    property int nextVideoNum: 0
    property int videoCount: 0
    property string videoPath: ""

    onStateChanged: console.log("State: " + state)
    states: [
        State {
            name: "STOPPED"
            PropertyChanges { target: videoElement; playing: false }
            PropertyChanges { target: overlayImage; opacity: 0 }
        },
        State {
            name: "PLAYING"
            PropertyChanges { target: videoElement; playing: true }
            PropertyChanges { target: overlayImage; opacity: 0 }
            PropertyChanges { target: videoElement; opacity: 1 }
        },
        State {
            name: "CHANGING_SOON"
            PropertyChanges { target: overlayImage; opacity: 1 }
            PropertyChanges { target: videoElement; playing: true }
        },
        State {
            name: "CHANGING"
            PropertyChanges { target: videoElement; opacity: 0 }
            PropertyChanges { target: videoElement; playing: true }
        }
    ]
    transitions: [
        Transition {
            NumberAnimation { target: overlayImage; properties: "opacity"; easing.type: Easing.InOutExpo; duration: 1000 }
        },
        Transition {
            from: "CHANGING_SOON"; to: "CHANGING"
            SequentialAnimation {
                id: videoSwitchAnimation
                running: false
                NumberAnimation { target: videoElement; property: "opacity"; to: 0; duration: 1000 }
                PropertyAction { target: videoElement; property: "source"; value: videoPath + "/" + nextVideoNum }
                PropertyAction { target: videoPlayer; property: "state"; value: "PLAYING" }
            }
        }
    ]

    Video {
        id: videoElement
        anchors.fill: parent
        focus: true
        volume: opacity
        onStatusChanged: {
            if(status == Video.EndOfMedia) {
                var nextVideo = nextVideoNum + 1
                if(nextVideo > videoCount) nextVideo = 1
                playFile(nextVideo)
            }
        }
    }
    Image {
        id: overlayImage
        source: nextVideoNum ? videoPath + "/" + nextVideoNum + ".png" : ""
        z: 10
    }
    Timer {
        id: nextVideoTimer
        interval: 2000
        onTriggered: {
            state = "CHANGING"
        }
    }
    StatusDisplay {
        text: "State: " + videoPlayer.state
        z: 20
        anchors.bottom: parent.bottom
    }

    Keys.onEscapePressed: Qt.quit()
}
