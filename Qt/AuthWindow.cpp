#include "AuthWindow.h"
#include "ui_AuthWindow.h"
#include "MainWindow.h"
#include "RegistrationWindow.h"
#include "DataManager.h"

#include <QMessageBox>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>

AuthWindow::AuthWindow(QWidget *parent)
    : QWidget(parent),
    ui(new Ui::AuthWindow)
{
    ui->setupUi(this);
    this->setObjectName("AuthWindow");

    connect(ui->authButton, &QPushButton::clicked, this, &AuthWindow::on_authButton_clicked);
    connect(ui->toggleButton, &QPushButton::clicked, this, &AuthWindow::abrirRegistro);
}

AuthWindow::~AuthWindow()
{
    delete ui;
}

void AuthWindow::on_authButton_clicked()
{
    const QString user = ui->usernameLineEdit->text().trimmed();
    const QString pass = ui->passwordLineEdit->text();

    if (user.isEmpty() || pass.isEmpty()) {
        QMessageBox::warning(this, "Atención", "Completá usuario y contraseña.");
        return;
    }


    DataManager::getInstance().login(user, pass, [this](bool success, QString respuesta) {
        if (!success) {
            QMessageBox::critical(this, "Error de inicio de sesión", respuesta);
            return;
        }

        QJsonDocument jsonDoc = QJsonDocument::fromJson(respuesta.toUtf8());
        if (!jsonDoc.isObject()) {
            QMessageBox::critical(this, "Error", "Respuesta inesperada del servidor.");
            return;
        }

        QString token = jsonDoc.object().value("access_token").toString();
        if (token.isEmpty()) {
            QMessageBox::critical(this, "Error", "No se recibió un token válido.");
            return;
        }

        MainWindow *main = new MainWindow(token);
        main->setAttribute(Qt::WA_DeleteOnClose);
        main->showMaximized();
        this->close();
    });
}

void AuthWindow::abrirRegistro()
{
    RegistrationWindow *regWin = new RegistrationWindow;
    regWin->setAttribute(Qt::WA_DeleteOnClose);
    regWin->showMaximized();
    this->close();
}
