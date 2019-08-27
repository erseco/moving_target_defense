###############################################################################
#
# TFM - Trabajo de Fin de Máster
# Master Profesional en Ingeniería Informática
#
# 2018 - Ernesto Serrano <erseco@correo.ugr.es>
# ---------------------------------------------
#
# Fichero Makefile para generacion de documentacion
#
###############################################################################

# TODO (sin empaquetado)
all: doc

#Generación de PDF compilando el archivo LaTeX con pdflatex
.PHONY: doc
doc:
	pdflatex -shell-escape -synctex=1 -interaction=nonstopmode project.tex || true
	biber project
	pdflatex -shell-escape -synctex=1 -interaction=nonstopmode project.tex || true
	mv project.pdf ../../
	make clean

spell:
	aspell --lang=es --mode=tex check project.tex
	find chapters/ -name "*.tex" -exec aspell --lang=es --mode=tex check "{}" \;

# LIMPEZA
# Limpia los archivos compilados, así como los archivos objeto y los paquetes zip
.PHONY: clean
clean:
	@echo "Limpiando..."
	@rm -rf {*.aux,*.lof,*.log,*.lol,*.lot,*.out,*.synctex.gz,*toc,*.run.xml,*.bbl,*.bcf,*.blg}
