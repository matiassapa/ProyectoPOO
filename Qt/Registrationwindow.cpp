#include "RegistrationWindow.h"
#include "ui_RegistrationWindow.h"
#include "AuthWindow.h"
#include "DataManager.h"

#include <QMessageBox>
#include <QDebug>

RegistrationWindow::RegistrationWindow(QWidget *parent)
    : QWidget(parent),
    ui(new Ui::RegistrationWindow)
{
    ui->setupUi(this);
}

RegistrationWindow::~RegistrationWindow()
{
    delete ui;
}

void RegistrationWindow::on_registerButton_clicked()
{
    const QString nombre   = ui->firstNameLineEdit->text().trimmed();
    const QString apellido = ui->lastNameLineEdit->text().trimmed();
    const QString username = ui->usernameLineEdit->text().trimmed();
    const QString email    = ui->emailLineEdit->text().trimmed();
    const QString password = ui->passwordLineEdit->text();

    if (!validateInput(nombre, apellido, username, email, password))
        return;

    DataManager::getInstance().registro(nombre, apellido, username, email, password,
                                        [this](bool success, QString message) {
                                            if (success) {
                                                QMessageBox::information(this, "Éxito", message);
                                                auto login = new AuthWindow;
                                                login->showMaximized();
                                                this->close();
                                            } else {
                                                QMessageBox::critical(this, "Error", message);
                                            }
                                        });
}

void RegistrationWindow::on_backToLoginButton_clicked()
{
    auto login = new AuthWindow;
    login->showMaximized();
    this->close();
}

bool RegistrationWindow::validateInput(const QString &nombre,
                                       const QString &apellido,
                                       const QString &username,
                                       const QString &email,
                                       const QString &password)
{
    if (nombre.isEmpty() || apellido.isEmpty() || username.isEmpty() ||
        email.isEmpty() || password.isEmpty()) {
        QMessageBox::warning(this, "Campos incompletos", "Completá todos los campos.");
        return false;
    }

    if (!email.endsWith("@gmail.com")) {
        QMessageBox::warning(this, "Email inválido", "El email debe ser @gmail.com");
        return false;
    }

    if (password.length() < 4) {
        QMessageBox::warning(this, "Contraseña", "Debe tener al menos 4 caracteres.");
        return false;
    }

    return true;
}
