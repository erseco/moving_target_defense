#!/usr/bin/env python3
"""
    This script calculate the fitnes of a configuration via this steps:
     1. Generate a NGINX configuration file based on the given config
     2. Test the configuration throught the `nginx -t` tool
     3. Run NGINX with the generated configuration
     4. Uses ZAP to know the security score of the configuration
"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"
from zap import *

from subprocess import run, Popen, PIPE

import tempfile
import os

import random


def generate_random_config():
    """
        Generate a random configuration, the positions are the selected NGINX
        directives to test, we have binary, integer and list directives
    """
    return [
        random.randint(512, 2048),   # worker_connections
        random.randint(10, 120),     # keepalive_timeout
        random.randint(0, 1),        # disable_symlinks
        random.randint(0, 1),        # autoindex
        random.randint(0, 1),        # send_timeout
        random.randint(512, 2048),   # large_client_header_buffers
        random.randint(512, 2048),   # client_max_body_size
        random.randint(0, 1),        # server_tokens
        random.randint(0, 1),        # gzip
        random.randint(0, 3),        # X-Frame-Options
        random.randint(0, 5),        # X-Powered-By
        random.randint(0, 1),        # X-Content-Type-Options
        random.randint(0, 2),        # server
    ]


def fitness(config):

    # Force kill running NGINX processes
    os.popen("kill -9 $(ps aux | grep  " + 'nginx' + " | awk '{print $2}') 2> /dev/null")

    nginx = generate(config)

    filename = tempfile.mkstemp()

    with open(filename, 'w') as f:
        f.write(str(nginx))

    p = run(['nginx', '-t', '-c', filename], stdout=PIPE, encoding='ascii')

    # Print values (for debug purposes)
    # print(p.returncode)
    # print(p.stdout)

    # By default return a high valu
    alerts = 999

    if p.returncode == 0:
        p = Popen(['nginx', '-c', filename], stdout=PIPE, encoding='ascii')

        alerts = test()

        # Print alerts (for debug purposes)
        # print("Alerts:")
        # print(alerts)

        p.terminate()

    os.unlink(filename)

    return alerts
