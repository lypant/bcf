#!/usr/bin/env python2

from __future__ import print_function
from bashcommand import BashCommand
from plan import Plan


def getPlan():
    commands = [
        BashCommand('echo 1', 'First echo'),
        BashCommand('echo 2', 'Second echo'),
        BashCommand('echo 3', 'Third echo'),
        BashCommand('echo 4', 'Fourth echo'),
        BashCommand('echo 5', 'Fifth echo'),
        BashCommand('echo 6', 'Sixth echo'),
        BashCommand('echo 7', 'Seventh echo'),
        BashCommand('echo 8', 'Eight echo'),
        BashCommand('echo 9', 'Ninth echo'),
        BashCommand('echo 10', 'Tenth echo')
    ]

    return Plan('Test echos', commands)


if __name__ == '__main__':
    getPlan().execute()
