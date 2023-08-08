import sys
import configparser

from GenerateInvoice import GenerateInvoice

def main():
    args = sys.argv[1:]

    config_file = 'config_test.ini'
    if len(args) > 0:
        config_file = args[0]

    config = configparser.ConfigParser()
    if len(config.read(config_file)) == 0:
        print("Unable to read config file " + config_file)
        return 1

    print("Starting execution with config file: " + config_file)

    GenerateInvoice(config).Generate()

    print("Completed")
    input("Press [ENTER] to finish")
    return 0

if __name__ == '__main__':
    sys.exit(main())