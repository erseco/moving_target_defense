FROM alpine:3.8 as tester

WORKDIR /tester

LABEL maintainer "erseco@correo.ugr.es"
LABEL vendor="ugr"

# Adding just requirements.txt to  optimize docker layer cache build
COPY requirements.txt .

# Installing alpine base packages
RUN apk add --no-cache \
	python3 \
	curl \
	nginx \
	openrc \
	ifupdown

RUN rc-update add nginx default
RUN echo "auto lo" > /etc/network/interfaces
Run echo "iface lo inet loopback" >> /etc/network/interfaces

# Installing python requirements
RUN	pip3 install -r requirements.txt

# Show package versions
RUN pip3 freeze

# Copying rest of files
COPY . .

# Avoid exiting this script (PID 1)
# CMD tail -f /dev/null
CMD /sbin/init
# CMD python3 docker.py

# VOLUME [ “/sys/fs/cgroup” ]