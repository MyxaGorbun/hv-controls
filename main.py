import argparse

from hv.run import hv_controls_cmd, hv_controls_qt


def create_parser():
    parser = argparse.ArgumentParser("HV-controls")
    parser.add_argument("--gui", action="store_const", const="qt", default=None)
    return parser

def main():
    args = create_parser().parse_args()
    if args.gui is None:
        hv_controls_cmd()
    elif args.gui == "qt":
        hv_controls_qt()

    return 0

if __name__ == '__main__':
    main()