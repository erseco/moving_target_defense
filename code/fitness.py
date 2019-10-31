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
from generate_nginx_config import *

from subprocess import run, Popen, PIPE

import tempfile
import os
import sys


def calculate_fitness(config):

    # Force kill running NGINX processes
    print("Killing existing NGINX processes...", file=sys.stderr)
    Popen(["pkill", "nginx"])

    nginx = generate(config)

    new_file, filename = tempfile.mkstemp()

    with open(filename, 'w') as f:
        f.write(str(nginx))

    p = run(['nginx', '-t', '-c', filename], stdout=PIPE, encoding='ascii')

    # Print values (for debug purposes)
    # print(p.returncode)
    # print(p.stdout)

    # By default return a high value
    alerts = 999

    if p.returncode == 0:
        p = Popen(['nginx', '-c', filename], stdout=PIPE, encoding='ascii')

        alerts = zap_test()

        # Print alerts (for debug purposes)
        # print("Alerts:")
        # print(alerts)

        p.terminate()

    os.unlink(filename)

    return alerts
