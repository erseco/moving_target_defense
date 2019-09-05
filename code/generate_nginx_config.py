#!/usr/bin/env python3
"""
    This script generates a nginx config file based on the given parameters
"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"

from nginx.config.api import Config, Section, Location, EmptyBlock, KeyMultiValueOption
import fitness


def set_directive_on_off(chromosome):
    return 'on' if chromosome else 'off'


def set_directive_int(chromosome):
    return chromosome


def set_directive_list(chromosome, list):
    return list[chromosome]


def generate(config=fitness.generate_random_config()):
    """
        Generate a configuration based on the "config" variable, if this var
        is not setted we generate a random configuration with the function
        fitness.generate_random_config()
    """
    events = Section(
        'events',
        worker_connections=set_directive_int(config[0])
    )

    http = Section(
        'http',
        include='/etc/nginx/mime.types',
        default_type='application/octet-stream',
        access_log='/var/log/nginx/access.log',
        sendfile='on',
        keepalive_timeout=set_directive_int(config[1]),
        disable_symlinks=set_directive_on_off(config[2]),
        autoindex=set_directive_on_off(config[3]),
        send_timeout=set_directive_int(config[4]),
        large_client_header_buffers="%d %d" % (4, set_directive_int(config[5])),
        client_max_body_size=set_directive_int(config[6]) * 1024,
        server_tokens=set_directive_on_off(config[7]),
        gzip=set_directive_on_off(config[8]),

    )

    http.sections.add(
        Section(
            'server',
            Location(
                '/',
                EmptyBlock(add_header=['X-Frame-Options:', set_directive_list(config[9], ['SAMEORIGIN', 'ALLOW-FROM http://www.exampletfm.com/', 'DENY', 'WRONG VALUE'])]),
                EmptyBlock(add_header=['X-Powered-By:', set_directive_list(config[10], ['PHP/5.3.3', 'PHP/5.6.8', 'PHP/7.2.1', 'Django2.2', 'nginx/1.16.0', 'WRONG SERVER'])]),
                EmptyBlock(add_header=['X-Content-Type-Options:', set_directive_list(config[11], ['nosniff', '""'])]),
                EmptyBlock(add_header=['Server:', set_directive_list(config[12], ['apache', 'caddy', 'nginx/1.16.0'])]),
                root='/usr/share/nginx/html',
                index='index.html index.htm',
            ),
            server_name='www.exampletfm.com',
            listen=80,
            error_page='500 502 503 504  /50x.html'
        )
    )

    nginx = Config(
        events,
        http,
        user='nginx',
        pid='/var/run/nginx.pid',
        worker_processes=1,
        daemon='off',  # passed in Dockerfile CMD
        error_log='/var/log/nginx/error.log warn',
    )

    # Return the generated configuration
    return nginx
