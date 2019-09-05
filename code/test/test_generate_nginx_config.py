from generate_nginx_config import *
"""Pytest TDD Test definition file"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"


def test_set_directive_on_off_bool():
    """Test directive change"""
    assert(set_directive_on_off(True) == 'on')


def test_set_directive_on_off_int():
    """Test directive change"""
    assert(set_directive_on_off(0) == 'off')


def test_set_directive_list_value_int():
    """Test directive change"""
    chromosome = 1
    value_list = [1, 2, 3]
    result = set_directive_list(chromosome, value_list)
    assert(result == value_list[chromosome])


def test_set_directive_list_value_string():
    """Test directive change"""
    chromosome = 2
    value_list = ["test1", "test2", "test3"]
    result = set_directive_list(chromosome, value_list)
    assert(not isinstance(result, list))
    assert(result == value_list[chromosome])


def test_generate_config_good():
    """Test nginx configuration"""
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


def test_generate_config_bad():
    """Test nginx configuration"""
    config = [1, 1, 1, 0, 0, 0, 1933, 1, 0, 2, 3, 0, 1]
    nginx_config = str(generate(config))

    assert("worker_connections 0;" not in nginx_config)
    assert("keepalive_timeout 0;" not in nginx_config)
    assert("disable_symlinks off;" not in nginx_config)
    assert("autoindex on;" not in nginx_config)
    assert("send_timeout 1;" not in nginx_config)
    assert("large_client_header_buffers 4 1;" not in nginx_config)
    assert("add_header Server: Apache;" not in nginx_config)
    assert("add_header X-Content-Type-Options: '';" not in nginx_config)
    assert("add_header X-Powered-By: PHP5.6;" not in nginx_config)
    assert("add_header X-Frame-Options: ALLOW;" not in nginx_config)
