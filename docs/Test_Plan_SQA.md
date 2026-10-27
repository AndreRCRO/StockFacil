# Test Plan SQA de StockFácil

Universidad del Valle Univalle. Materia Software Quality Assurance.
Docente Rolando Lara. Integrantes Andre Romero Caballero y Santiago Camacho Echalar.
Fecha 27 de octubre de 2026. Versión 1.0 ágil con Kanban.

## 1 Introducción

StockFácil administra productos, entradas, salidas, alertas e historial de inventario para pequeños negocios. Conserva Laravel 13, PHP 8.3, Blade, Tailwind CSS 4, Vite 7 y SQLite. Este plan integra la calidad al flujo Kanban de dos integrantes, con pruebas verificables y revisión cruzada. Se amplía la documentación previa conservando sus evidencias históricas.

## 2 Alcance

Se verifican autenticación, catálogo de productos y movimientos de inventario con alertas. La matriz incluirá ocho casos críticos y su relación con las pruebas existentes y las nuevas pruebas de navegador.

## 3 Estrategia de pruebas

Se reutiliza PHPUnit para unidad e integración y se incorporan Selenium y Cypress para pruebas funcionales por navegador. Las pruebas se ejecutan en SQLite aislado; nunca se reinicia la base habitual. Los escenarios BDD son especificaciones vinculadas a pruebas, sin afirmar TDD retrospectivo.

## 4 Roles y responsabilidades

Andre coordina el plan y métricas y desarrolla catálogo. Santiago coordina pruebas y desarrolla movimientos. Ambos revisan el trabajo del otro y comparten calidad. La asignación es propuesta y no acredita revisiones humanas realizadas.

## 5 Ciclo de vida de las pruebas

Preparar requisito y datos, diseñar caso, desarrollar, probar, registrar defectos, corregir, reejecutar y documentar el cierre. El tablero utiliza Pendiente, En desarrollo, En pruebas, En corrección y Terminado.

## 6 Criterios de entrada y salida

Entrada: requisito y criterio comprobables, datos aislados y entorno disponible. Salida técnica: pruebas aprobadas, evidencias y documentación sincronizadas. Cierre de equipo: revisión humana cruzada y aceptación registradas. Límite de dos tareas En desarrollo.

## 7 Métricas y control de calidad

Línea base ejecutada: 60 pruebas PHPUnit aprobadas y 419 aserciones. Las métricas finales se completan al terminar las nuevas ejecuciones, conservando los logs originales.

## 8 Riesgos y mitigación

Entrega al 28 de octubre, descargas de navegadores, accesos GitHub y revisión humana pendiente. Se priorizan funciones existentes, automatización mínima y evidencias reproducibles.

## Anexos

Se completan la matriz, resultados, guía Kanban, auditoría y relación con GitHub conforme avanza la implementación.
