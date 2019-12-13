import sys
import argparse
from twisted.internet import reactor

from fixsim.client import create_initiator


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='Run FIX client simulator')

    parser.add_argument('-ic', '--initiator_config', type=str, required=True
                        , help='Path to FIX config file')
    parser.add_argument('-c', '--client_config', type=str, required=True
                        , help='Path to FIX client config file')

    result = parser.parse_args(arguments)
    return result


def main(params):
    options = parse_args(params)

    initiator = create_initiator(options.initiator_config, options.client_config)
    initiator.start()

    reactor.run()


if __name__ == "__main__":
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    main(args)
