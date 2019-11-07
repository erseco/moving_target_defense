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
import time

import signal


def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), signal.SIGKILL)


def calculate_fitness(config):

    # Force kill running NGINX processes
    # print("Stopping NGINX servicer...", file=sys.stderr)
    # Popen(["service", "nginx", "stop"])
    # time.sleep(1)

    nginx = generate(config)

    filename = '/etc/nginx/nginx.conf'

    with open(filename, 'w') as f:
        f.write(str(nginx))

    p = run(['nginx', '-t', '-c', filename], stdout=PIPE, encoding='ascii')

    # Print values (for debug purposes)
    # print(p.returncode)
    # print(p.stdout)

    # By default return a high value
    alerts = 999

    if p.returncode == 0:
        Popen(["service", "nginx", "start"], stdout=PIPE, encoding='ascii')

        alerts = zap_test()

        # Print alerts (for debug purposes)
        print("Alerts:")
        print(alerts)

        check_kill_process("nginx")

        Popen(["service", "nginx", "zap"])
        time.sleep(2)

        # os.unlink(filename)


    return alerts
