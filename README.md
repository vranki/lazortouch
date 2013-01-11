lazortouch
==========

Laser scanner controlled multimedia player

setting up
==========

Make directory 'videos' under player/qml/videoplayer and copy
video files in it. Rename the videos to be numbers, no file
suffix. Add overlay images as PNG.

Example:

$ ls lazortouch/player/qml/videoplayer/videos/
1  1.png  2  2.png  3  3.png


Symlinks should also work..

compiling
=========

cd player
qmake
make

running
=======

./player

