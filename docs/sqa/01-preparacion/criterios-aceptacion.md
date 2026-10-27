# Criterios de aceptación originales y alcance

Fecha: 13 de octubre de 2026. Se preserva el texto de la consigna; las reglas complementarias no reemplazan los CA.

## HU-01

| Código | Descripción original |
| --- | --- |
| CA-01 | El sistema debe exigir el nombre del producto. |
| CA-02 | El SKU o código del producto debe ser único. |
| CA-03 | El precio no puede ser negativo. |
| CA-04 | La cantidad inicial no puede ser negativa. |
| CA-05 | Cuando se registre correctamente un producto, este debe aparecer en el inventario. |
| CA-06 | Cuando se ingresen datos inválidos, el sistema debe mostrar mensajes de validación. |

## HU-02

| Código | Descripción original |
| --- | --- |
| CA-01 | Las entradas deben incrementar correctamente las existencias. |
| CA-02 | Las salidas deben disminuir correctamente las existencias. |
| CA-03 | No se debe permitir retirar más productos de los disponibles. |
| CA-04 | No se deben permitir movimientos con cantidades iguales o menores a cero. |
| CA-05 | Cada entrada y salida debe quedar registrada en el historial. |
| CA-06 | El sistema debe mostrar alertas cuando un producto alcance su stock mínimo. |

## Precisiones de implementación

HU-01 exige además categoría válida, precio con hasta dos decimales, mínimo entero no negativo y stock inicial entero. El SKU se normaliza a mayúsculas. El stock inicial cero se guarda sin crear un movimiento cero. Son reglas complementarias observadas, no modificaciones de los seis CA.

HU-02 agrega cantidad entera, límite superior de 2147483647, producto activo, responsable autenticado, protección transaccional y conservación del historial. La alerta usa stock <= mínimo, lo cual incluye el límite solicitado y los productos por debajo de él. No se encontró una discrepancia funcional con los doce CA originales en los casos ejecutados.

## Identificación de casos

SQA/CP-01 a SQA/CP-14 designan exclusivamente los casos de esta actividad. Los CP de docs/casos-prueba.md pertenecen al catálogo previo y conservan sus IDs. Esta distinción resuelve HR-01 sin alterar la planificación anterior.
