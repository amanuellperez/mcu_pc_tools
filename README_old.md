# Herramientas necesarias en mcu++

## Advertencia

Esto no es más que una copia de seguridad de algunos programas que voy
haciendo, para tenerlos ordenados y no perderlos. Por ello casi mejor no
pierdas el tiempo en este repositorio. 

De momento no voy a suministrar ni reglas de compilación ni variables de
entorno ni demás.

Trabajo en linux con GCC (versión 11 mínima).


## ¿Qué hay aquí?
Los programas que vaya incluyendo aquí son programas que necesito en mcu++.

Por ejemplo: para conectar la cámara OV7670 al ordenador no me vale el
terminal `screen` que estaba usando ya que desconozco cómo grabar en
hexadecimal. Implementaré una versión mínima de terminal para que funcione con
la cámara.

En principio los programas que vaya metiendo aquí van a ser programas
auxiliares que necesito en mcu++. Como tal no pretendo dedicarle mucho tiempo,
así que no estarán demasiado pensados.


## Dependencias

Casi seguro que la mayoría de los programas dependerán de `alp` y aquellos en
los que manipule imágenes dependerán de `img`.

