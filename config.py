from configparser import ConfigParser


def get_INTERNAL_CONFIG(_key):
    config_object = ConfigParser()
    config_object.read("config.ini")
    # Get the INTERNAL_CONFIG section
    cObj = config_object["INTERNAL_CONFIG"]
    # Get the Key
    return cObj[_key]


def set_INTERNAL_CONFIG(_key, _value):
    # cObj = config_object["INTERNAL_CONFIG"]
    config_object = ConfigParser()
    config_object.read("config.ini")
    # Get the INTERNAL_CONFIG section
    cObj = config_object["INTERNAL_CONFIG"]
    # Update the Key's value
    cObj[_key] = _value
    # Write changes back to file
    with open("config.ini", "w") as conf:
        config_object.write(conf)


# __main__
