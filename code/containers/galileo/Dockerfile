FROM perl:5-threaded

LABEL maintainer="Ernesto Serrano <erseco@correo.ugr.es>"

WORKDIR /projects/galileo

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.

# ENV SOURCE_BRANCH=devops-dockerfile

# Install requirements from main alpine repository
# RUN apk --no-cache add \

RUN cpanm Galileo