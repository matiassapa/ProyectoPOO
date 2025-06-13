#include "DataManager.h"
#include <QJsonObject>
#include <QJsonDocument>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QUrlQuery>
#include <QUrl>
#include <QDebug>

DataManager::DataManager(QObject* parent)
    : QObject(parent)
{
    networkManager = new QNetworkAccessManager(this);
}

DataManager& DataManager::getInstance()
{
    static DataManager instance;
    return instance;
}

// 🔐 LOGIN
void DataManager::login(const QString& usuario, const QString& clave,
                        std::function<void(bool, QString)> callback)
{
    QUrl url("http://ec2-54-167-15-203.compute-1.amazonaws.com:8000/auth/login");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");

    QUrlQuery postData;
    postData.addQueryItem("username", usuario);
    postData.addQueryItem("password", clave);

    QNetworkReply* reply = networkManager->post(request, postData.toString(QUrl::FullyEncoded).toUtf8());

    connect(reply, &QNetworkReply::finished, this, [reply, callback]() {
        QByteArray response = reply->readAll();

        if (reply->error() == QNetworkReply::NoError) {
            callback(true, QString::fromUtf8(response));
        } else {
            callback(false, QString::fromUtf8(response));
        }

        reply->deleteLater();
    });
}

// 📝 REGISTRO (Corregido para extraer solo "mensaje")
void DataManager::registro(const QString& nombre, const QString& apellido,
                           const QString& usuario, const QString& mail,
                           const QString& clave,
                           std::function<void(bool, QString)> callback)
{
    QUrl url("http://ec2-54-167-15-203.compute-1.amazonaws.com:8000/auth/registro");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");

    QUrlQuery postData;
    postData.addQueryItem("nombre", nombre);
    postData.addQueryItem("apellido", apellido);
    postData.addQueryItem("usuario", usuario);
    postData.addQueryItem("mail", mail);
    postData.addQueryItem("clave", clave);

    QNetworkReply* reply = networkManager->post(request, postData.toString(QUrl::FullyEncoded).toUtf8());

    connect(reply, &QNetworkReply::finished, this, [reply, callback]() {
        QByteArray response = reply->readAll();

        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(response);
            QString mensaje = "Registro completado correctamente.";

            if (doc.isObject()) {
                QJsonObject obj = doc.object();
                if (obj.contains("mensaje"))
                    mensaje = obj["mensaje"].toString();
            }

            callback(true, mensaje);
        } else {
            callback(false, QString::fromUtf8(response));
        }

        reply->deleteLater();
    });
}

// 🤖 ANALIZAR PROMPT
void DataManager::analizarPrompt(const QString& texto, const QString& token,
                                 std::function<void(bool, QString)> callback)
{
    QUrl url("http://ec2-54-167-15-203.compute-1.amazonaws.com:8000/analizar");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");
    request.setRawHeader("Authorization", ("Bearer " + token).toUtf8());

    QUrlQuery postData;
    postData.addQueryItem("texto", texto);

    QNetworkReply* reply = networkManager->post(request, postData.toString(QUrl::FullyEncoded).toUtf8());

    connect(reply, &QNetworkReply::finished, this, [reply, callback]() {
        QByteArray response = reply->readAll();

        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(response);
            QJsonObject obj = doc.object();

            if (obj.contains("resultado")) {
                callback(true, obj["resultado"].toString());
            } else {
                callback(false, "La respuesta no contiene el campo 'resultado'.");
            }
        } else {
            callback(false, QString::fromUtf8(response));
        }

        reply->deleteLater();
    });
}
