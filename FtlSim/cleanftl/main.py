# for executing FtlSim from command line
import argparse

import utils
import config
import recorder
import simulator

def main():
    parser = argparse.ArgumentParser(
            description="It takes event input file."
            )
    parser.add_argument('-c', '--configfile', action='store',
        help='config file path (REQUIRED)')
    parser.add_argument('-e', '--events', action='store',
        help='event file (REQUIRED)')
    parser.add_argument('-v', '--verbose', action='store',
        help='verbose level: 0-minimum, 1-more')
    args = parser.parse_args()

    if args.events == None:
        parser.print_help()
        exit(1)

    if args.configfile == None:
        parser.print_help()
        exit(1)

    # You need to load config before everything else happen
    # (but you have already imported the modules)
    dic = utils.load_json(args.configfile)

    if args.verbose != None:
        dic['verbose_level'] = int(args.verbose)

    # Go with the wind~~~~
    conf = config.Config()
    conf.load_from_json_file(args.configfile)

    sim = simulator.Simulator(conf)
    sim.run(open(args.events, 'r'))

if __name__ == '__main__':
    main()

