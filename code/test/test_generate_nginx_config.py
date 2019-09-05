from generate_nginx_config import *


def test_set_directive_on_off_bool():
    assert(set_directive_on_off(True) == 'on')


def test_set_directive_on_off_int():
    assert(set_directive_on_off(0) == 'off')


def test_set_directive_list_value_int():
    chromosome = 1
    value_list = [1, 2, 3]
    result = set_directive_list(chromosome, value_list)
    assert(result == value_list[chromosome])


def test_set_directive_list_value_string():
    chromosome = 2
    value_list = ["test1", "test2", "test3"]
    result = set_directive_list(chromosome, value_list)
    assert(result == value_list[chromosome])


def test_generate_good_config():
    config = [200, 39, 0, 1, 0, 1033, 1933, 1, 0, 2, 3, 0, 1]
    nginx_config = str(generate(config))

    assert("worker_connections 200;" in nginx_config)
    assert("keepalive_timeout 39;" in nginx_config)
    assert("disable_symlinks off;" in nginx_config)
    assert("autoindex on;" in nginx_config)
    assert("send_timeout 0;" in nginx_config)
    assert("large_client_header_buffers 4 1033;" in nginx_config)
    assert("add_header Server: caddy;" in nginx_config)
    assert("add_header X-Content-Type-Options: nosniff;" in nginx_config)
    assert("add_header X-Powered-By: Django2.2;" in nginx_config)
    assert("add_header X-Frame-Options: DENY;" in nginx_config)
