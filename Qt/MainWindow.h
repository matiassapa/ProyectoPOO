#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    explicit MainWindow(const QString &token, QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void generarTareas();
    void exportarCSV();
    void exportarPDF();
    void cerrarSesion();

private:
    Ui::MainWindow *ui;
    QString authToken;  // ✅ El token sigue siendo necesario para la autorización
};

#endif // MAINWINDOW_H
