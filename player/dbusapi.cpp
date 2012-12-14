#include "dbusapi.h"
#include <QDebug>

DbusApi::DbusApi(QObject *rootObj) : QObject() {
    Q_ASSERT(rootObj);
    qmlRootObject = rootObj;
}

void DbusApi::playFile(const QString &filename)
{
    qDebug() << Q_FUNC_INFO << filename;

    QMetaObject::invokeMethod(qmlRootObject, "playFile",
            Q_ARG(QVariant, filename));
}
