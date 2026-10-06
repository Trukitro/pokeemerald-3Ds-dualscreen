# Pokémon Esmeralda en español

Pokémon Emerald 3Ds Dual Screen puede compilarse con los textos y gráficos de
la ROM española limpia de **Pokémon Esmeralda (España, BPES)**. La traducción
no se distribuye: se extrae en tu ordenador de tu propia ROM al compilar el
juego desde el código fuente.

Es **experimental**. Una versión anterior se probó en una 3DS física; la
integración con las funciones actuales necesita su propia prueba en consola.
El builder de las releases sigue siendo inglés: el payload publicado necesita
la ROM inglesa (BPEE) y rechaza la española.

| Idioma | Código | SHA-1 de la ROM limpia |
|---|---|---|
| Español | BPES | `fe1558a3dcb0360ab558969e09b690888b846dd9` |
| Inglés | BPEE | `f3ae088181bf583e55daf962a92bb46f4f1d07b7` |

## Compilar la versión española

Con los requisitos de la [guía de desarrollo](DEVELOPMENT.md):

```sh
python tools/bootstrap.py --make --spanish-rom "/ruta/Pokemon Esmeralda.gba" -j8
```

El bootstrap aplica los parches, compila las herramientas y los includes
generados, ejecuta `tools/localize_spanish.py` con tu ROM y compila el 3DSX en
`build/upstream/3ds_port/emerald3ds.3dsx`. Cambiar de idioma (volver a
ejecutar sin `--spanish-rom`) reinicia el árbol y borra los objetos compilados
y los recursos localizados, para no reutilizar datos del otro idioma.

El motor comprueba el idioma con el que se compiló: un ejecutable español solo
acepta un paquete de datos generado desde BPES, y uno inglés solo desde BPEE.

## Cómo se obtiene la versión española

`tools/localize_spanish.py` comprueba el SHA-1 de la ROM y las huellas SHA-256
de los archivos fuente antes de escribir en el árbol generado. Los manifiestos
de `tools/locales/` contienen posiciones en el código, desplazamientos y
tamaños en la ROM, nombres de símbolos y direcciones. No contienen textos,
gráficos, sonidos ni secciones de la ROM.

El proceso sustituye los textos y campos del código por los de tu ROM, extrae
104 recursos gráficos y reconstruye las 55 páginas de créditos y los pisos de
la Colina Desafío. Incluye nombres, diálogos, menús, vocabulario, canciones
del bardo, frases de entrenadores, cartas y preguntas. La pantalla táctil usa
etiquetas españolas y la Pokédex muestra metros y kilos.

Los parches de idioma (`patches/pokeemerald/0030-…` a `0035-…`, todos bajo
`PORT_BRIDGE`) copian por nombre las tablas de la Colina Desafío y adaptan los
nombres de bayas, las descripciones de los rivales, los títulos de concursos,
la pantalla «FIN», el ancho de una tabla de textos de combate y las unidades
de la Pokédex. En la compilación inglesa no cambian nada salvo la copia de la
Colina Desafío, que ya no depende del orden en que el enlazador coloca las
tablas.

Si un cambio del port modifica alguno de los archivos fuente del manifiesto,
la localización se detiene («Source differs from the pinned patched tree»)
hasta que se actualicen sus posiciones y huellas.

Las funciones añadidas después de la traducción (ajustes y trucos nuevos de
la pantalla táctil, por ejemplo) pueden mostrar todavía textos en inglés.

## Autoría

Traducción y herramientas de localización de Jesus Oliva
([pull request #6](https://github.com/ZallaxDev/pokeemerald-3Ds-dualscreen/pull/6)).
