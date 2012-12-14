#ifndef DBUSAPI_H
#define DBUSAPI_H

#include <QObject>

/*
To command:
dbus-send --type=method_call --print-reply  --dest=org.hs5w.VideoPlayer / org.hs5w.VideoPlayer.playFile string:'kek'
*/

class DbusApi : public QObject
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.hs5w.VideoPlayer")
public:
    explicit DbusApi(QObject *rootObj);

public slots:
    void playFile(const QString &filename);
private:
    QObject *qmlRootObject;
};

#endif // DBUSAPI_H
