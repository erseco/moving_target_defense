import fitness


def test_generate_random_config_len():
    config = fitness.generate_random_config()
    assert(len(config) == 13)
