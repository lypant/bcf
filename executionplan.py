#!/usr/bin/env python2

from __future__ import print_function

import time
import datetime
import bashcommand

class ExecutionPlan():
    # Format of a message printed before executing a command
    START_MSG = 'Cmd [{command:0{width}}/{commands:0{width}}] {description}...'
    # Format of a message printed after execution of a command
    END_MSG = START_MSG + '{resultMsg} ({duration})'
    # Part of END_MSG appended when command execution succeeded
    RESULT_MSG_OK = 'OK'
    # Part of END_MSG appended when command execution failed
    RESULT_MSG_FAILED = 'FAILED'
    # Format of a message printing full bash command
    CMD_MSG = 'Cmd: {command}'
    # Message printed when bash command error is detected
    EXCEPTION_MSG = 'Bash command execution failed'
    # Format of a message printed after all commands are executed
    TOTAL_DURATION_MSG = '{executionPlan}: {result}, total time: {duration}'

    def __init__(self, name='ExecutionPlan', commands=[], logger=None):
        self.name = name
        self.commands = []
        self.logger = logger
        self.appendCommands(commands)

    def appendCommands(self, commands):
        for command in commands:
            command.index = len(self.commands) + 1
            self.commands.append(command)

    def execute(self):
        commandsCount = len(self.commands)
        width = len(str(commandsCount))
        finalResultMsg = ''
        startTime = time.time()
        for command in self.commands:
            resultMsg = ExecutionPlan.RESULT_MSG_OK
            self.logger.logStatistic(
                ExecutionPlan.START_MSG.format(
                    command=command.index,
                    commands=commandsCount,
                    width=width,
                    description=command.description))
            self.logger.logCommand(
                ExecutionPlan.CMD_MSG.format(command=command.command))
            try:
                command.execute(self.logger)
            except bashcommand.BashCommand.ExecutionError as exception:
                self.logger.logError(ExecutionPlan.EXCEPTION_MSG + str(exception))
                resultMsg = ExecutionPlan.RESULT_MSG_FAILED
                finalResultMsg = resultMsg
                break
            finally:
                duration = str(datetime.timedelta(seconds=command.duration))
                self.logger.logStatistic(ExecutionPlan.END_MSG.format(
                    command=command.index,
                    commands=commandsCount,
                    width=width,
                    description=command.description,
                    resultMsg=resultMsg,
                    duration=duration))
        else:
            finalResultMsg = ExecutionPlan.RESULT_MSG_OK
        totalDuration = time.time() - startTime
        formattedDuration = str(datetime.timedelta(seconds=totalDuration))
        self.logger.logStatistic(ExecutionPlan.TOTAL_DURATION_MSG.format(
            executionPlan=self.name,
            result=finalResultMsg,
            duration=formattedDuration))

if __name__ == '__main__':
    import logger

    lgr = logger.Logger('/tmp/executionplan.log')
    ep = ExecutionPlan(name='Directory listings', logger=lgr)
    ep.appendCommands([
        bashcommand.BashCommand('ls /', 'List root dir'),
        bashcommand.BashCommand('ls / | wc -l', 'Count root dirs'),
        bashcommand.BashCommand('ls /zonk', 'List nonexisting dir'),
        bashcommand.BashCommand('ls /', 'List root dir')])
    ep.execute()
