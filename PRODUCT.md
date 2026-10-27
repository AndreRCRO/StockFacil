# StockFácil

<!-- impeccable:product-schema 1 -->

## Platform
web

## Stack
Laravel 13, PHP 8.3, Blade, Tailwind CSS, Vite, Eloquent y SQLite. Stack exigido por el usuario.

## Users
Administradores de pequeños negocios y emprendimientos en Bolivia. Estudiantes que evalúan el proyecto mediante actividades de SQA.

## Product Purpose
Registrar productos, controlar entradas y salidas y conocer las existencias con un historial verificable.

## Operating Context
Aplicación local; precios en bolivianos y fechas de Bolivia. Inventario compartido, sin separación por negocio ni gestión de roles. La actividad del 19 de octubre incorpora registro de cuentas. La evaluación académica previa de HU-01 y HU-02 conserva su alcance histórico.

## Capabilities and Constraints
Autenticación, dashboard, productos, movimientos, alertas y consulta de historial. SQLite local. Sin API, Flutter ni servicios externos. El stock solo cambia mediante movimientos transaccionales. No se borran productos ni movimientos desde la interfaz.

## Brand Commitments
Nombre StockFácil. Interfaz Bento sobria; blanco roto, grafito y verde salvia/petróleo. Navegación lateral, SVG consistentes, tarjetas de diferentes proporciones y diseño responsivo. Construcción directa en Blade confirmada por el usuario.

## Evidence on Hand
Requisitos completos aportados en el archivo del usuario. Seeder de 12 productos con datos de demostración; ninguna cifra simulada en las vistas. Resultados de pruebas deben provenir de ejecuciones reales.

## Product Principles
- Funcionamiento y persistencia antes que decoración.
- Reglas simples y centralizadas.
- Historial trazable.
- Instalación reproducible.

## Accessibility & Inclusion
Etiquetas visibles, foco de teclado, contraste adecuado y adaptación a pantallas pequeñas.
