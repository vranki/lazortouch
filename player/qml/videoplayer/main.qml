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
        // Ignore if video is already queued or playing
        if(filenum == currentVideoNum || filenum == nextVideoSelected || filenum > videoCount) return;

        if(filenum > 0) {
            if(videoElement.playing) {
                nextVideoSelected = filenum
                videoMasterVolume = 1
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
    property double videoMasterVolume: 1
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
            NumberAnimation { target: videoPlayer; properties: "videoMasterVolume"; easing.type: Easing.InOutExpo; duration: 1000 }
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
        volume: Math.min(opacity, videoMasterVolume)
//	opacity: 1 - overlayImage.opacity
        onStatusChanged: {
            if(status == Video.EndOfMedia) { // skip to next video when end is reached, or loop
                opacity = 0;
                var nextVideo = currentVideoNum + 1
                if(nextVideo > videoCount) nextVideo = 1
                playFile(nextVideo)

                if(videoMasterVolume >= 0.2)
                    videoMasterVolume -= 0.2
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
        text: "State: " + videoPlayer.state + " " + currentVideoNum + " selected " + nextVideoSelected + " master vol " + videoMasterVolume
        z: 20
        anchors.bottom: parent.bottom
    }

    Keys.onEscapePressed: Qt.quit()
}
