🧠 TP4 - Planificador de Tareas Técnicas (Frontend en Qt)

Este repositorio contiene la aplicación de escritorio desarrollada en Qt para el trabajo práctico 4 de la asignatura Programación Orientada a Objetos. La herramienta permite ingresar una descripción general de un proyecto de software, procesarla mediante una API basada en OpenAI y visualizar el plan técnico resultante clasificado por tipo de tarea y orden cronológico.

📌 Funcionalidades principales

📝 Ingreso libre de requerimientos técnicos o funcionales.

📡 Comunicación con una API REST construida en FastAPI.

🧠 Clasificación automática de tareas usando OpenAI:

Por tipo: frontend, backend, base de datos, testing, etc.

Por orden de ejecución basado en dependencias implícitas.

📋 Visualización de tareas en una interfaz Qt ordenada y clara.

🎨 Colores o etiquetas por tipo de tarea.

📤 Exportación del resultado como PDF o CSV.

🎨 Visualización Qt

Para ejecutar correctamente esta aplicación se requiere Qt versión 6.6.3 con el kit MSVC2019 64bit.

QLineEdit + QPushButton para entrada y análisis.

QTableView con QStandardItemModel para mostrar tareas.

Colores por tipo (por ejemplo: azul para frontend, rojo para backend).

Orden automático por campo orden.

Botones para exportar como .pdf o .csv.

🧱 Backend relacionado

Este frontend se conecta con una API FastAPI incluida en un stack de Docker Compose, que provee:

FastAPI + OpenAI

Autenticación JWT (si se requiere)

Base de datos MySQL

phpMyAdmin

A continuación se incluirán los enlaces principales del proyecto:

🌐 API FastAPI: [[enlace a las APIs](http://ec2-54-167-15-203.compute-1.amazonaws.com:8000/docs)]

🛢️ Base de datos MySQL/phpMyAdmin: [[(http://ec2-54-167-15-203.compute-1.amazonaws.com:8080/)]]

☁️ Instancia AWS: (https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances)

👨‍💻 Autores

Matías Sapa

Valentino Frache
