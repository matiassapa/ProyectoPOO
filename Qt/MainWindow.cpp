#include "MainWindow.h"
#include "ui_mainwindow.h"
#include "AuthWindow.h"
#include "DataManager.h"

#include <QMessageBox>
#include <QFileDialog>
#include <QTextStream>
#include <QPrinter>
#include <QTextDocument>
#include <QDebug>

MainWindow::MainWindow(const QString &token, QWidget *parent)
    : QWidget(parent),
    ui(new Ui::MainWindow),
    authToken(token)
{
    ui->setupUi(this);
    this->setWindowTitle("Panel Principal - VYMTIA");
    this->showMaximized();

    connect(ui->generateButton, &QPushButton::clicked, this, &MainWindow::generarTareas);
    connect(ui->logoutButton, &QPushButton::clicked, this, &MainWindow::cerrarSesion);
    connect(ui->exportCsvButton, &QPushButton::clicked, this, &MainWindow::exportarCSV);
    connect(ui->exportPdfButton, &QPushButton::clicked, this, &MainWindow::exportarPDF);

    qDebug() << "🟢 MainWindow cargado correctamente.";
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::generarTareas()
{
    QString prompt = ui->promptTextEdit->toPlainText().trimmed();

    if (prompt.isEmpty()) {
        QMessageBox::warning(this, "Campo vacío", "Por favor ingresá un prompt.");
        return;
    }

    ui->outputLabel->setText("⌛ Enviando prompt a la API...");
    ui->resultTextEdit->clear();

    DataManager::getInstance().analizarPrompt(prompt, authToken, [this](bool success, QString respuesta) {
        if (!success) {
            QMessageBox::critical(this, "Error en la API", respuesta);
            ui->outputLabel->setText("❌ Error al generar tareas.");
            return;
        }

        ui->resultTextEdit->setPlainText(respuesta);
        ui->outputLabel->setText("✅ Tareas generadas correctamente.");
    });
}

void MainWindow::cerrarSesion()
{
    AuthWindow *login = new AuthWindow;
    login->showMaximized();
    this->close();
}

void MainWindow::exportarCSV()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Guardar como CSV", "", "Archivos CSV (*.csv)");
    if (fileName.isEmpty()) return;

    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QMessageBox::warning(this, "Error", "No se pudo abrir el archivo para escribir.");
        return;
    }

    QTextStream out(&file);
    out << ui->resultTextEdit->toPlainText();
    file.close();
    QMessageBox::information(this, "Éxito", "Archivo CSV exportado correctamente.");
}

void MainWindow::exportarPDF()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Guardar como PDF", "", "Archivos PDF (*.pdf)");
    if (fileName.isEmpty()) return;

    QPrinter printer(QPrinter::HighResolution);
    printer.setOutputFormat(QPrinter::PdfFormat);
    printer.setOutputFileName(fileName);

    QTextDocument document;
    QString html = "<h2>🔱 VYMTIA - Tareas Generadas</h2><pre>" +
                   ui->resultTextEdit->toPlainText().toHtmlEscaped() + "</pre>";

    document.setHtml(html);
    document.print(&printer);

    QMessageBox::information(this, "Éxito", "Archivo PDF generado correctamente.");
}
