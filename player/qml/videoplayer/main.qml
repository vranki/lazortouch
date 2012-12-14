import QtQuick 1.1
import Qt 4.7
import QtMultimediaKit 1.1

Video {
    function playFile(filename) {
        source = filename
        playing = true
    }

    width: 640
    height: 400
    source: "../../../../videos/1"
    focus: true
    playing: true

    Keys.onEscapePressed: Qt.quit()
    Image {
        source: "../../../../videos/overlay.png"
    }
}
