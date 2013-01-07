#include <QtGui/QApplication>
#include <QDBusConnection>
#include <QGraphicsObject>
#include "qmlapplicationviewer.h"
#include "dbusapi.h"

Q_DECL_EXPORT int main(int argc, char *argv[])
{
    QScopedPointer<QApplication> app(createApplication(argc, argv));

    QmlApplicationViewer viewer;
    viewer.setOrientation(QmlApplicationViewer::ScreenOrientationAuto);
    viewer.setMainQmlFile(QLatin1String("qml/videoplayer/main.qml"));
    viewer.showExpanded();

    DbusApi dbusApi(viewer.rootObject());

    QDBusConnection connection = QDBusConnection::sessionBus();
    Q_ASSERT(connection.isConnected());
    bool ret = false;
    ret = connection.registerObject("/player", &dbusApi, QDBusConnection::ExportAllSlots);
    Q_ASSERT(ret);
    ret = connection.registerService("org.hs5w.VideoPlayer");
    Q_ASSERT(ret);
    return app->exec();
}
