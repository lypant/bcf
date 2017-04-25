#!/usr/bin/env python2

from __future__ import print_function

import subprocess
import select
import os
import logger
import time


class BashCommand():
    READ_SIZE = 1024

    class ExecutionError(Exception):
        '''
        For more convenient analysis of bash command execution errors
        '''
        def __init__(self, command, exitCode, stdErr):
            '''
            @param command bash command which caused an execution error
            @param exitCode exit code of the command returned by bash
            @param stdErr output passed to stderr by the command
            '''
            Exception.__init__(self)
            self.command = command
            self.exitCode = exitCode
            self.stdErr = stdErr

        def __str__(self):
            return '\nBash command: %s\nExit code: %s\nStd err: %s' % \
                    (self.command, self.exitCode, self.stdErr)

    def __init__(self, command, description='', input=''):
        self.command = command
        self.description = description
        self.input = input

        self.startTime = 0
        self.endTime = 0
        self.duration = 0

        self._cleanupTemporaryData()

    def __str__(self):
        return '<BashCommand> "%s" "%s"' % (self.description, self.command)

    def _cleanupTemporaryData(self):
        self.logger = None
        self.inputLines = []
        self.process = None
        self.inputStreams = []
        self.outputStreams = []
        self.errMsg = ''

    def execute(self, logger=None):
        # Set logger
        self.logger = logger
        self.startTime = time.time()
        self._createSubprocess()
        self._prepareInputStreamsAndData()
        self._prepareOutputStreams()
        self._waitForIOCompletion()
        self.process.wait()
        self.endTime = time.time()
        self.duration = self.endTime - self.startTime
        self._checkReturnCode()

        self._cleanupTemporaryData()

    def _createSubprocess(self):
        self.process = subprocess.Popen(
            ['/usr/bin/bash', '-c', self.command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def _prepareInputStreamsAndData(self):
        if self.input:
            self.inputLines = [
                line + '\n' for line in input.rstrip().split('\n')]
            self.inputStreams = [self.process.stdin.fileno()]

    def _prepareOutputStreams(self):
        self.outputStreams = [
            self.process.stdout.fileno(),
            self.process.stderr.fileno()]

    def _passInputLinesToSubprocess(self):
        for line in self.inputLines:
            os.write(self.inputStreams[0], line)
            self.inputLines.remove(line)

    def _storeMessageWhenErrorStream(self, fileDescriptor, data):
        if fileDescriptor == self.process.stderr.fileno():
            self.errMsg += data

    def _logOutput(self, data):
        if self.logger:
            self.logger.logOutput(data)

    def _handleSubprocessOutput(self):
        for fileDescriptor in self.outputStreams:
            data = os.read(fileDescriptor, BashCommand.READ_SIZE)
            if data:
                self._storeMessageWhenErrorStream(fileDescriptor, data)
                self._logOutput(data.rstrip())
            else:
                self.outputStreams.remove(fileDescriptor)

    def _waitForIOCompletion(self):
        while self.outputStreams:
            r, w, x = select.select(self.outputStreams, self.inputStreams, [])
            self._passInputLinesToSubprocess()
            self._handleSubprocessOutput()

    def _checkReturnCode(self):
        if self.process.returncode:
            raise BashCommand.ExecutionError(
                self.command,
                self.process.returncode,
                self.errMsg.rstrip())


if __name__ == '__main__':
    lgr = logger.Logger('/tmp/bashcommand.log')
    # bc1 = BashCommand('ls /')
    # bc2 = BashCommand('ls /home')
    # bc1.execute(lgr)
    # bc2.execute(lgr)
    # bc1.execute()
    # bc1.execute(lgr)
    # bc1.execute(lgr)

    bc3 = BashCommand('ls /zonk')
    try:
        bc3.execute(lgr)
    except BashCommand.ExecutionError as e:
        lgr.logError(e)
