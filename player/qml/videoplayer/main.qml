import QtQuick 1.1
import Qt 4.7
import QtMultimediaKit 1.1

Video {
    function playFile(filenum) {
	nextVideoNum = filenum
	if(filenum > 0) {
		nextVideoTimer.restart()
        } else {
		nextVideoTimer.stop()
	}
    }
    property int nextVideoNum: 0
    width: 640
    height: 400
    source: "../../../../videos/1"
    focus: true
    playing: true

    Keys.onEscapePressed: Qt.quit()
    Image {
	id: overlayImage
        source: "../../../../videos/overlay.png"
	visible: nextVideoTimer.running
    }
    Timer {
	id: nextVideoTimer
	interval: 5000
	onTriggered: {
        	source = "../../../../videos/" + nextVideoNum
        	playing = true
	}
    }
}
