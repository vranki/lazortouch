# Add more folders to ship with the application, here
folder_01.source = qml/videoplayer
folder_01.target = qml
DEPLOYMENTFOLDERS = folder_01

# Additional import path used to resolve QML modules in Creator's code model
QML_IMPORT_PATH =

QT += mobility multimediakit dbus

CONFIG += mobility
MOBILITY += multimedia

# The .cpp file which was generated for your project. Feel free to hack it.
SOURCES += main.cpp \
    dbusapi.cpp

# Please do not modify the following two lines. Required for deployment.
include(qmlapplicationviewer/qmlapplicationviewer.pri)
qtcAddDeployment()

HEADERS += \
    dbusapi.h
