#ifndef DATAMANAGER_H
#define DATAMANAGER_H

#include <QObject>
#include <QNetworkAccessManager>
#include <functional>

class DataManager : public QObject
{
    Q_OBJECT

public:
    static DataManager& getInstance();

    void login(const QString& usuario, const QString& clave,
               std::function<void(bool, QString)> callback);

    void registro(const QString& nombre, const QString& apellido,
                  const QString& usuario, const QString& mail,
                  const QString& clave,
                  std::function<void(bool, QString)> callback);

    void analizarPrompt(const QString& texto, const QString& token,
                        std::function<void(bool, QString)> callback);

private:
    explicit DataManager(QObject* parent = nullptr);
    QNetworkAccessManager* networkManager;
};

#endif // DATAMANAGER_H
