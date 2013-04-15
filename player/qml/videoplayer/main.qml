import QtQuick 1.1
import Qt 4.7
import QtMultimediaKit 1.1

Rectangle {
    id: videoPlayer
    width: 640
    height: 400
    color: "black"
    state: "STOPPED"
    property int screensaver_video: 99

    function playFile(filenum) {
        // Ignore if video is already queued or playing
        if(filenum == currentVideoNum || filenum == nextVideoSelected || (filenum != screensaver_video && filenum > videoCount)) return;
        if(filenum > 0) {
            if(videoElement.playing) {
                nextVideoSelected = filenum
                state = "CHANGING_SOON"
                nextVideoTimer.restart()
            } else {
                currentVideoNum = filenum;
                videoElement.source = videoPath + "/" + currentVideoNum
                state = "CHANGING"
            }
        } else {
            state = "PLAYING"
            nextVideoSelected = 0;
            nextVideoTimer.stop()
        }
    }

    property int nextVideoSelected: 0
    property int currentVideoNum: 0
    property int videoCount: 0
    property string videoPath: ""

    onStateChanged: console.log("State: " + state)
    states: [
        State {
            name: "STOPPED"
            PropertyChanges { target: videoElement; playing: false }
            PropertyChanges { target: overlayImage; opacity: 0 }
            PropertyChanges { target: videoElement; opacity: 0 }
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
            PropertyChanges { target: videoElement; opacity: 0 }
            PropertyChanges { target: videoElement; playing: false }
        },
        State {
            name: "CHANGING"
            PropertyChanges { target: videoElement; opacity: 0 }
            PropertyChanges { target: videoElement; playing: false }
        }
    ]
    transitions: [
        Transition {
            NumberAnimation { target: overlayImage; properties: "opacity"; easing.type: Easing.InOutExpo; duration: 1000 }
        },
        Transition {
            to: "CHANGING"
            SequentialAnimation {
                id: videoSwitchAnimation
                running: false
                NumberAnimation { target: videoElement; property: "opacity"; to: 0; duration: 1 }
                PropertyAction { target: videoElement; property: "source"; value: videoPath + "/" + currentVideoNum }
                PropertyAction { target: videoPlayer; property: "state"; value: "PLAYING" }
            }
        }
    ]

    Video {
        id: videoElement
        anchors.fill: parent
        focus: true
        onStatusChanged: {
            if(status == Video.EndOfMedia) { // Play screensaver video
                if(currentVideoNum == screensaver_video) {
                    play() // Loop
                } else {
                    opacity = 0;
                    playFile(screensaver_video)
                }
            }
        }
    }
    Image {
        id: overlayImage
        source: nextVideoSelected ? videoPath + "/" + nextVideoSelected + ".png" : ""
        z: 10
    }
    Timer {
        id: nextVideoTimer
        interval: 3000
        onTriggered: {
            currentVideoNum = nextVideoSelected;
            nextVideoSelected = 0;
            state = "CHANGING"
        }
    }
    StatusDisplay {
        visible: false
        text: "State: " + videoPlayer.state + " " + currentVideoNum + " selected " + nextVideoSelected
        z: 20
        anchors.bottom: parent.bottom
    }

    Keys.onEscapePressed: Qt.quit()
    Keys.onRightPressed: videoElement.position = videoElement.duration - 3000 // Seek to end of video
}
