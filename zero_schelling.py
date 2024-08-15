#!/usr/bin/env python

import os
import argparse
import sys
import json
from os.path import exists, dirname, basename, join, expanduser
from glob import glob
import pandas as pd
import numpy as np


HELP_PARAGRAPHS = {
    'main':'an example cli tool',
    'level1': {
        'main':'main level',
        'first-thing':'docs for first thing',
        'second-thing':'docs for second thing',
    }
}


def main():
    parser = argparse.ArgumentParser(description=HELP_PARAGRAPHS['main'])

    h = HELP_PARAGRAPHS['level1']
    parser.add_argument('--test', '-f', required=False, default='',
                        action='store_true', help=h['first-thing'])
    args = parser.parse_args()

    if args.test:
        from zero_schelling_demo import agent as a 
        ag = a.Agent(min_like_neighbors_happy=1, )
        print(ag)


if __name__ == '__main__':
    main()
