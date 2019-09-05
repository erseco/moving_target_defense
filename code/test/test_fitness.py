import fitness
import genetic
"""Pytest TDD Test definition file"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"


def test_generate_random_config_len():
    """Test generation of random config"""
    config = fitness.generate_random_config()
    assert(isinstance(config, list))
    assert(len(config) == genetic.genes)
