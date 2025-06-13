#ifndef REGISTRATIONWINDOW_H
#define REGISTRATIONWINDOW_H

#include <QWidget>

namespace Ui { class RegistrationWindow; }

class RegistrationWindow : public QWidget
{
    Q_OBJECT

public:
    explicit RegistrationWindow(QWidget *parent = nullptr);
    ~RegistrationWindow();

private slots:
    void on_registerButton_clicked();
    void on_backToLoginButton_clicked();

private:
    Ui::RegistrationWindow *ui;

    bool validateInput(const QString &firstName,
                       const QString &lastName,
                       const QString &email,
                       const QString &password,
                       const QString &confirmPassword);
};

#endif // REGISTRATIONWINDOW_H
