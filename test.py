import configparser
config = configparser.ConfigParser()
config.read("config")
print(config.sections())
