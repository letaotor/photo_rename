#! /bin/python

import argparse


def args_proc():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src', default='./',
            type=str, dest='src')
    parser.add_argument('-d', '--dst', default='./',
            type=str, dest='dst')
    args = vars(parser.parse_args())
    return args
