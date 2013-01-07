#include "dbusapi.h"
#include <QDebug>

DbusApi::DbusApi(QObject *rootObj) : QObject() {
    Q_ASSERT(rootObj);
    qmlRootObject = rootObj;
}

void DbusApi::playFile(const int filenum)
{
    qDebug() << Q_FUNC_INFO << filenum;

    QMetaObject::invokeMethod(qmlRootObject, "playFile",
            Q_ARG(QVariant, filenum));
}
