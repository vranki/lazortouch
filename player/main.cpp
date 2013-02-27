#include <QtGui/QApplication>
#include <QDBusConnection>
#include <QGraphicsObject>
#include <QDebug>
#include <QDir>
#include <QFile>
#include "qmlapplicationviewer.h"
#include "dbusapi.h"

Q_DECL_EXPORT int main(int argc, char *argv[]) {
    QScopedPointer<QApplication> app(createApplication(argc, argv));

    QmlApplicationViewer viewer;
    viewer.setOrientation(QmlApplicationViewer::ScreenOrientationAuto);
    viewer.setMainQmlFile(QLatin1String("qml/videoplayer/main.qml"));
    viewer.showExpanded();
//    viewer.showFullScreen();

    DbusApi dbusApi(viewer.rootObject());

    QDBusConnection connection = QDBusConnection::sessionBus();
    Q_ASSERT(connection.isConnected());
    bool ret = false;
    ret = connection.registerObject("/player", &dbusApi, QDBusConnection::ExportAllSlots);
    Q_ASSERT(ret);
    ret = connection.registerService("org.hs5w.VideoPlayer");
    Q_ASSERT(ret);

    QString videoPath = "qml/videoplayer/videos";
    if(argc>=2) videoPath = argv[1];

    qDebug() << Q_FUNC_INFO << "Looking for videos in" << videoPath;
    viewer.rootObject()->setProperty("videoPath", "videos");

    int fileCount = 0;
    QFile videoFile;
    do {
        videoFile.setFileName(videoPath + "/" + QString().number(fileCount+1));
        if(videoFile.exists()) {
            qDebug() << Q_FUNC_INFO << "Found file " + videoFile.fileName();
            fileCount++;
        }
    } while(videoFile.exists());
    qDebug() << Q_FUNC_INFO << "File count is " << fileCount;
    viewer.rootObject()->setProperty("videoCount", fileCount);

    return app->exec();
}
