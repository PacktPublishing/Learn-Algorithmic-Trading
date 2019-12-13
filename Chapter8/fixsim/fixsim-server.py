import sys
import argparse
from twisted.internet import reactor

from fixsim.server import create_acceptor


def parse_options(arguments):
    parser = argparse.ArgumentParser(description='Run FIX server simulator')

    parser.add_argument('-ac', '--acceptor_config', type=str, required=True
                        , help='Path to FIX config file')
    parser.add_argument('-c', '--server_config', type=str, required=True
                        , help='Path to FIX server config file')

    result = parser.parse_args(arguments)
    return result


def main(params):
    options = parse_options(params)

    acceptor = create_acceptor(options.acceptor_config, options.server_config)
    acceptor.start()

    reactor.run()


if __name__ == "__main__":
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    main(args)
