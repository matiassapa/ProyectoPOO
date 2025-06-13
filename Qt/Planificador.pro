QT       += core gui widgets sql network webenginewidgets webchannel
CONFIG   += c++17

TEMPLATE = app
TARGET   = Planificador

SOURCES += \
    main.cpp \
    AuthWindow.cpp \
    MainWindow.cpp \
    Registrationwindow.cpp \
    DataManager.cpp

HEADERS += \
    AuthWindow.h \
    MainWindow.h \
    Registrationwindow.h \
    DataManager.h

FORMS += \
    authwindow.ui \
    mainwindow.ui \
    registrationwindow.ui

# Si querés incluir archivos externos como HTML, JS, CSS:
DISTFILES += \
    interfaz_web/index.html \
    interfaz_web/script.js \
    styles/estilo.qss

RESOURCES += \
    resources.qrc
