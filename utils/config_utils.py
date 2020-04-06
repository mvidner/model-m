import configparser


def string_to_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


class ConfigFile():

    def __init__(self, param_dict=None):

        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        if param_dict:
            for name, value in param_dict.items():
                self.config[name] = value

    def save(self, filename):
        with open(filename, 'w') as configfile:
            self.config.write(configfile)

    def load(self, filename):
        self.config.read(filename)

    def section_as_dict(self, section_name):
        sdict = self.config._sections.get(section_name, {})
        return {name: string_to_number(value) for name, value in sdict.items()}


if __name__ == "__main__":

    test_dict = {
        "TASK": {"num_nodes": 10000},
        "MODEL": {"beta": 0.155,
                  "gamma": 1/12.39,
                  "sigma": 1/5.2
                  }
    }

    test_config = ConfigFile(test_dict)
    test_config.save("test.ini")

    new_config = ConfigFile()
    new_config.load("test.ini")

    print(new_config.section_as_dict("TASK"))
    print(new_config.section_as_dict("MODEL"))
