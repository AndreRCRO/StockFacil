---
name: StockFácil
description: Bento sobrio para mantener el inventario en orden.
colors:
  primary: "#234e43"
  primary-deep: "#183a31"
  canvas: "#f5f6f1"
  surface: "#ffffff"
  ink: "#26362f"
  muted: "#626e66"
  line: "#e3e7e0"
  field-line: "#cdd5cd"
  focus: "#527f69"
  nav-active: "#e9efe6"
  sage-alert: "#eef0df"
  sage-alert-ink: "#536246"
  success-bg: "#edf4e9"
  success-ink: "#365d37"
  warning-bg: "#fbf1d8"
  warning-ink: "#7c5a12"
  danger-bg: "#f9eae5"
  danger-ink: "#a34338"
  neutral-bg: "#ecefec"
  neutral-ink: "#566056"
typography:
  display:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "clamp(30px, 3.5vw, 49px)"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-.035em"
  headline:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "clamp(26px, 2.4vw, 34px)"
    fontWeight: 750
    lineHeight: 1.25
    letterSpacing: "-.035em"
  title:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "16px"
    fontWeight: 750
    lineHeight: 1.25
    letterSpacing: "-.02em"
  body:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "12px"
    fontWeight: 750
    lineHeight: 1.6
  button:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.6
  metric:
    fontFamily: "Manrope Variable, sans-serif"
    fontSize: "clamp(64px, 7vw, 86px)"
    fontWeight: 550
    lineHeight: 1.1
    letterSpacing: "-.04em"
rounded:
  badge: "5px"
  icon: "7px"
  control: "8px"
  choice: "9px"
  brand: "11px"
  panel: "14px"
spacing:
  compact: "8px"
  control: "12px"
  small: "16px"
  grid: "18px"
  filter: "20px"
  panel: "24px"
  form: "30px"
  page: "36px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
    height: "43px"
  button-primary-hover:
    backgroundColor: "{colors.primary-deep}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
    height: "43px"
  field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.control}"
    padding: "11px 12px"
  navigation:
    textColor: "{colors.muted}"
    rounded: "{rounded.control}"
    padding: "12px 14px"
  navigation-active:
    backgroundColor: "{colors.nav-active}"
    textColor: "{colors.primary}"
  status-warning:
    backgroundColor: "{colors.warning-bg}"
    textColor: "{colors.warning-ink}"
    rounded: "{rounded.badge}"
    padding: "4px 8px"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
    padding: "24px"
  inventory-card:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.panel}"
    padding: "24px"
  movement-choice:
    rounded: "{rounded.choice}"
    padding: "14px 16px 14px 40px"
---

# Design System: StockFácil

## Overview

**Creative North Star: "Bento sobrio"**

La dirección confirmada combina blanco roto, grafito y salvia/petróleo con una navegación lateral estable. Las superficies blancas y las tarjetas de proporciones diferentes organizan la información sin competir con las tareas de registrar, consultar y reponer existencias. El verde profundo concentra la identidad en la marca, las acciones principales y el resumen de inventario.

La densidad es práctica: tablas con separadores finos, formularios con etiquetas visibles y métricas que destacan mediante escala tipográfica. La profundidad procede de cambios de tono y bordes; la interfaz se adapta desde el escritorio a una navegación móvil desplegable. Esta documentación recoge los valores implementados en CSS, los componentes Blade y su comportamiento JavaScript; no supone una certificación de accesibilidad.

**Key Characteristics:**

- Bento sobrio con superficies blancas sobre un lienzo blanco roto.
- Verde petróleo para identidad y acción; tonos semánticos para existencias y mensajes.
- Una sola familia tipográfica local y cifras tabulares para comparar cantidades.
- Bordes finos, esquinas moderadas y profundidad sin sombras.
- Sidebar, tablas desplazables y formularios que se reorganizan en móvil.

## Colors

La paleta combina neutros de matiz vegetal con un verde profundo y estados de stock legibles por texto y color. Los valores normativos están en el frontmatter; los nombres siguientes explican su aplicación.

### Primary

- **Petróleo vegetal** (`primary`): símbolo de marca, acción principal, tarjeta de productos activos, enlaces y panel narrativo del acceso.
- **Petróleo profundo** (`primary-deep`): respuesta al pasar el puntero sobre la acción principal.
- **Salvia de foco** (`focus`): borde enfocado y contorno visible de teclado.
- **Salvia de navegación** (`nav-active`): fondo de la sección actual en el menú.

### Neutral

- **Blanco roto vegetal** (`canvas`): fondo general del área de trabajo.
- **Blanco de superficie** (`surface`): sidebar, tarjetas, campos y panel de acceso.
- **Grafito verde** (`ink`): texto principal y contenido introducido en formularios.
- **Gris vegetal** (`muted`): texto secundario, ayudas, fechas, cabeceras de tabla y placeholders.
- **Separador suave** (`line`): límites de paneles y divisiones de navegación, tablas y formularios.
- **Borde de campo** (`field-line`): contorno en reposo de controles editables.

### Estados semánticos

- **Salvia de atención** (`sage-alert`, `sage-alert-ink`): panel de productos que necesitan revisión.
- **Verde disponible** (`success-bg`, `success-ink`): distintivo de existencias disponibles.
- **Ámbar de mínimo** (`warning-bg`, `warning-ink`): distintivo de stock bajo.
- **Arcilla de agotado** (`danger-bg`, `danger-ink`): distintivo de existencias agotadas.
- **Gris inactivo** (`neutral-bg`, `neutral-ink`): distintivo de producto inactivo.

**The Estado legible Rule.** Acompañar el color de un estado con su texto; entradas y salidas incluyen además un icono y el signo de la cantidad en el historial.

## Typography

**Display Font:** Manrope Variable, con respaldo `sans-serif`.

**Body Font:** Manrope Variable, con respaldo `sans-serif`.

**Character:** Una sola familia de curvas suaves sostiene la identidad y la lectura operativa. Se importa desde `@fontsource-variable/manrope` y se sirve con los recursos locales de Vite; no requiere una solicitud a un proveedor externo de fuentes.

### Hierarchy

- **Display:** Mensaje narrativo del acceso; peso y tamaño fluido del token `display`. En pantallas de hasta 800 px se reduce a 28 px.
- **Headline:** Título de página del token `headline`; composición equilibrada mediante `text-wrap: balance`.
- **Title:** Encabezado de sección del token `title`. Los títulos de tarjetas varían entre 12 y 13 px; el formulario de acceso utiliza 27 px.
- **Body:** Texto base del token `body`. Tablas y buena parte de la interfaz operativa emplean 12 px; las ayudas y metadatos utilizan 10 u 11 px.
- **Label:** Etiquetas visibles del token `label`, con peso fuerte y caja natural. Los botones tienen su propio token `button`.
- **Metric:** Cifra protagonista de productos activos del token `metric`; las métricas secundarias utilizan 34 px y peso 650, y el contador de atención utiliza 48 px.

**The Cifras comparables Rule.** Usar cifras tabulares en cantidades, stock, contadores y paginación, y alinear a la derecha las columnas numéricas.

## Layout

El escritorio combina una sidebar fija de 236 px, una barra superior de 77 px y un área principal centrada con máximo de 1600 px. El contenido tiene un margen interior de 36 px arriba, 38 px a los lados y 28 px abajo. La retícula Bento utiliza tres columnas de proporción `1fr 1fr 1.12fr`, separadas por el paso `grid`; movimientos recientes ocupan dos columnas y reposición ocupa el ancho completo.

El ritmo combina separaciones compactas de 8 y 12 px, paneles con 24 px de relleno y formularios con 30 px. Las tablas conservan estructura y se desplazan horizontalmente dentro de su contenedor; las cabeceras usan 13 px de relleno vertical y las celdas 18 px, con 20 px a los lados. Los formularios principales usan una proporción `2fr / 1fr`, una separación de 36 px y un máximo de 1100 px; los campos interiores se organizan en dos columnas separadas por 24 px.

- **Desde 1600 px:** La separación Bento aumenta a 24 px.
- **Hasta 1200 px:** La sidebar pasa a 210 px, el contenido a 28 px por 24 px y Bento a dos columnas. Atención, historial y acciones rápidas ocupan el ancho completo.
- **Hasta 800 px:** La sidebar de 250 px se despliega sobre la página; la barra superior mide 65 px, el contenido usa todo el ancho y el formulario pierde su columna auxiliar. El acceso pasa de dos columnas a una.
- **Hasta 540 px:** Bento y los campos pasan a una columna; las dos métricas pequeñas siguen en una fila. El contenido usa 25 px por 16 px, los filtros se apilan, la lista de reposición pasa a una columna y los formularios reducen su relleno a 22 px por 18 px.

## Elevation & Depth

El sistema no utiliza sombras. La separación se obtiene con superficies blancas, bordes de un píxel y fondos tonales para selección, avisos y resumen de inventario. En móvil, un velo verde translúcido (`#20382a60`) separa la sidebar abierta del contenido; la sidebar ocupa el nivel 40 y el velo el 35.

**The Superficie tranquila Rule.** Conservar la profundidad por tono y borde que utiliza el código actual; las tarjetas en reposo permanecen planas.

## Shapes

Las tarjetas y paneles usan el radio `panel`; los botones, campos y enlaces de navegación comparten `control`. Los controles de movimiento emplean `choice`, los botones de icono `icon`, los distintivos `badge` y el símbolo de marca `brand`. El avatar es circular. Esta gradación conserva diferencias claras entre superficie, control y estado sin cambiar de lenguaje formal.

Los paneles con tablas recortan sus esquinas y contienen el desplazamiento horizontal. Los SVG usan una caja de 24 unidades, trazos de 1,7 unidades, extremos redondos y ausencia de relleno; su tamaño habitual es 20 px, con variantes de 16 a 28 px según el contexto.

## Components

### Buttons

Acciones compactas, firmes y legibles. La acción principal utiliza los tokens de `button-primary`; su altura es mínima, por lo que puede crecer si el contenido lo exige. La variante secundaria conserva la superficie blanca con borde (`#d3dbd1`) y cambia a un fondo salvia claro (`#edf2e8`) al pasar el puntero. Los botones de icono miden 36 px por 36 px.

Enlaces y botones transicionan fondo y texto durante 150 ms con `ease-out`. El foco de teclado utiliza un contorno de 3 px y una separación de 3 px. Al enviar un formulario, la acción se deshabilita, declara `aria-busy` y muestra el texto de progreso; el estado deshabilitado reduce la opacidad a 0,6 y cambia el cursor. Los extremos de la paginación se presentan como texto con `aria-disabled`, a opacidad 0,5.

### Chips

Distintivos informativos de stock, con punto de color, etiqueta visible, tamaño de letra de 10 px y peso 650. Los fondos y textos siguen las parejas semánticas del frontmatter. Son etiquetas, no filtros interactivos; la selección de un producto ocurre en el enlace o acción que las contiene.

### Cards / Containers

Contenedores blancos con borde `line` y radio `panel`, sin sombras. El relleno habitual usa el paso `panel`; los formularios emplean `form`. La tarjeta de inventario utiliza el acento como fondo, una cifra grande tabular y un enlace al pie. El aviso de reposición utiliza una superficie salvia de atención. Las métricas, tablas y acciones rápidas comparten el mismo contorno aunque tengan proporciones distintas.

### Inputs / Fields

Campos blancos, borde `field-line`, radio `control` y relleno de 11 px por 12 px. Etiquetas visibles encima del control; ayudas y errores debajo con identificadores asociados. Los placeholders utilizan `muted`, igual que el texto secundario. El foco cambia el borde a `focus` y mantiene el contorno visible cuando corresponde al teclado.

Los campos inválidos declaran `aria-invalid` y usan un borde de arcilla (`#b54b45`), acompañado de error textual (`#a43d34`). Los radios de entrada/salida conservan controles nativos visibles y una tarjeta seleccionada con borde de foco y fondo (`#edf3e9`).

### Navigation

Sidebar blanca con enlaces a Dashboard, Productos, Movimientos y Stock bajo. Cada enlace combina SVG, texto de peso 650 y, en la sección activa, fondo `nav-active`, color `primary`, punto final y `aria-current="page"`. El hover emplea fondo (`#f3f6f0`). Usuario y cierre de sesión se sitúan al pie.

En móvil, el menú se desplaza durante 180 ms con `ease-out`; cerrado, la sidebar queda `inert` y sus controles dejan de recibir interacción. El botón declara `aria-expanded`; abrir lleva el foco al cierre, Tab recorre los elementos del menú y Escape, el velo o el botón cierran y devuelven el foco. El enlace «Ir al contenido» aparece al recibir foco. La preferencia de movimiento reducido elimina las transiciones.

### Tables & Feedback

Tablas de 12 px con cabeceras pequeñas, fondo claro (`#fafbf7`) y separadores suaves. El hover de fila utiliza (`#fafbf8`); las cantidades mantienen cifras tabulares y alineación derecha. Nombre y SKU forman una jerarquía de dos líneas. La paginación se ubica bajo un borde superior y puede reorganizarse en pantallas pequeñas.

Los avisos de éxito usan `role="status"` y los errores `role="alert"`, con icono SVG y texto. Los estados vacíos combinan icono, título, explicación breve y una acción cuando corresponde. En movimientos, la vista previa muestra stock actual y resultante; una salida que excede las existencias cambia la cifra a arcilla y explica cómo corregirla.

## Do's and Don'ts

### Do:

- **Do** Mantener el Bento sobrio, la sidebar blanca y las superficies diferenciadas por tono y borde.
- **Do** Reutilizar Manrope Variable local y las jerarquías existentes para texto, etiquetas y métricas.
- **Do** Acompañar los estados de stock con texto y conservar las cifras tabulares alineadas en tablas.
- **Do** Conservar etiquetas visibles, ayudas asociadas, foco de teclado y sidebar móvil inerte cuando está cerrada.
- **Do** Contener las tablas en un área con desplazamiento horizontal y reorganizar los formularios según los breakpoints observados.

### Don't:

- **Don't** Introducir sombras decorativas que alteren la profundidad plana del sistema actual.
- **Don't** Convertir el color o un placeholder en la única explicación de un estado o campo.
- **Don't** Suprimir el contorno de foco ni permitir que el menú móvil cerrado reciba foco.
- **Don't** Presentar los snippets estáticos del catálogo como datos reales de inventario o resultados de pruebas.
