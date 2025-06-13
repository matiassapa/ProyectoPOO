#include <QApplication>
#include <QFile>
#include <QDebug>
#include "AuthWindow.h"
#include "DataManager.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // 🔽 Aplicar estilo global desde archivo .qss
    QFile styleFile("styles/estilo.qss");
    if (styleFile.open(QFile::ReadOnly | QFile::Text)) {
        QString style = styleFile.readAll();
        app.setStyleSheet(style);
        qDebug() << "✅ Estilo cargado correctamente.";
    } else {
        qDebug() << "❌ No se pudo cargar el archivo styles/estilo.qss";
    }

    // ✅ Inicializar conexión con la base de datos
    DataManager::getInstance();

    // 🔐 Mostrar pantalla de inicio de sesión maximizada
    AuthWindow w;
    w.setObjectName("AuthWindow");  // para aplicar QSS
    w.showMaximized();              // pantalla completa

    return app.exec();
}
