# proyecto-compiladores

#Avance 6

* Se agregó el operador GOTO para detectar la función “main”, también se agregaron los operadores de funciones y se agregó la funcionalidad para guardar el objeto función.
* Se agregó el campo de los parámetros al objeto de la función, también se agregó el cuádruplo ERA y se arregló un bug de floats.
* Se agregó el campo de la dirección al objeto de la función, también se agregó el cuádruplo ENDFUNC y se agregaron nuevos casos de ejemplo.
* Se agregó la funcionalidad para regresar los parámetros en la llamada a función, también se agregaron cuadrupulos PARAMETER y GOSUB al llamar la función.
* Se agregó la funcionalidad para validar el tipo y la cantidad de argumentos en la llamada a función, también se agregó el cuádruplo RETURN y la validación del retorno de la función.
* Se crearon las clases para el manejo de la memoria virtual, tomando en cuenta la estructura de memoria que se utilizará para su uso. 
* Se dividió la manera de guardar los operandos, haciendo la diferenciación si son constantes o variables.
* Se agregó la dirección de memoria a las variables constantes y se modificaron los cuádruplos para guardar dicha memoria. Dichas direcciones también se agregaron a la tabla de constantes.
* Se mejoró la impresión de los cuádruplos para mejorar la manera de trabajar en el proyecto.
* Se implementó una función para imprimir las variables constantes.
* Se agregó la dirección de memoria a las variables globales y se modificaron los cuádruplos para guardar dicha memoria.
* Se agregó la dirección de memoria a las variables locales y los temporales.
* Se agregaron campos en el objeto de la función para contabilizar el número de temporales y variables locales.
* Se contabilizó el número de temporales utilizados en una función.
* Se creó una clase para leer el archivo de compilación
* Se creó la tabla de constantes en el parseo de la máquina virtual.
* Se creó una clase especial de cuádruplos para la máquina virtual y se parsearon los cuádruplos.
* Se parsearon las funciones para la máquina virtual.
* Se creó la clase para la máquina virtual
* Se contabilizó los tamaños de las variables locales
* Se agregó la dirección de memoria a los parámetros de una función
* Se implementó la funcionalidad para realizar el reset de la memoria local y temporal al terminar la funció
* Se crearon archivos para el manejo de la máquina virtual.

