# Moving Target Defense

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub](https://img.shields.io/github/license/erseco/moving_target_defense.svg)](https://github.com/erseco/moving_target_defense/blob/master/LICENSE)
[![GitHub](https://img.shields.io/github/forks/erseco/moving_target_defense.svg)](https://github.com/erseco/moving_target_defense/network)
[![Build Status](https://travis-ci.com/erseco/moving_target_defense.svg?branch=master)](https://travis-ci.com/erseco/moving_target_defense)

## Sistema de ciberdefensa dinámica basada en algoritmos evolutivos para la prevención de ataques informáticos

## Abstract

Además de realizar una labor determinada de forma eficiente, los servicios informáticos deben ser capaces de evitar los ataques y de detectar los que haya. Una técnica de defensa consiste en convertirse en un "objetivo móvil", que varíe el perfil de forma que los atacantes no lo reconozcan.

Mediante algoritmos evolutivos trataremos de configurar diferentes servicios de forma que se maximice la diversidad, a la vez que se optimice la seguridad y las prestaciones.

## Contenido

- Memoria: [thesis](../blob/master/doc/)
- Presentación: [https://gitpitch.com/erseco/moving_target_defense](https://gitpitch.com/erseco/moving_target_defense?t=night)
- Codigo: [code](../blob/master/code/)

### Autor: Ernesto Serrano Collado
### Tutor: Juan Julián Merelo Guervós

Memoria realizada con LaTeX, para generar el archivo PDF introducir las siguientes órdenes:

```
cd doc
sudo apt-get install texlive texlive-latex-extra texlive-lang-spanish xzdec
tlmgr init-usertree
tlmgr install xcolor
make
```

*Memoria y Presentación* liberada bajo la licencia **Creative Commons Attribution-ShareAlike 4.0 International**.

*Código* liberado bajo licencia **GNU GENERAL PUBLIC LICENSE Version 3**.
