#!/usr/bin/env python2

from __future__ import print_function
from logger import Logger
import time
import datetime


class Plan():
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

    def __init__(self, name, commands=(), logger=None):
        self.name = name

        self.commands = {}
        if commands:
            self.add(commands)

        if logger:
            self.logger = logger
        else:
            self.logger = Logger('./' + name + '.log')

    def __str__(self):
        text = ''
        for index in self.commands:
            text += '{index:0{width}} "{description}" "{command}"\n'.format(
                index=index,
                width=len(str(len(self.commands))),
                description=self.commands[index].description,
                command=self.commands[index].command)
        return text.rstrip()

    def add(self, commands):
        for command in commands:
            self.commands[len(self.commands) + 1] = command

    def getAllCommands(self):
        return self.commands.values()

    def planForCommands(self, planName, indices):
        cmds = [self.commands[index] for
                index in self.commands if index in indices]
        return Plan(planName, cmds)

    def planForCommandsExcept(self, planName, indices):
        cmds = [self.commands[index] for
                index in self.commands if index not in indices]
        return Plan(planName, cmds)

    def planForCommandsBefore(self, planName, index):
        cmds = [self.commands[i] for i in self.commands if i < index]
        return Plan(planName, cmds)

    def planForCommandsAfter(self, planName, index):
        cmds = [self.commands[i] for i in self.commands if i > index]
        return Plan(planName, cmds)

    def execute(self):
        commandsCount = len(self.commands)
        width = len(str(commandsCount))
        finalResultMsg = ''
        startTime = time.time()
        for index in self.commands:
            command = self.commands[index]
            resultMsg = Plan.RESULT_MSG_OK
            self.logger.logStatistic(
                Plan.START_MSG.format(
                    command=index,
                    commands=commandsCount,
                    width=width,
                    description=command.description))
            self.logger.logCommand(
                Plan.CMD_MSG.format(command=command.command))
            try:
                command.execute(self.logger)
            except BashCommand.ExecutionError as exception:
                self.logger.logError(
                    Plan.EXCEPTION_MSG + str(exception))
                resultMsg = Plan.RESULT_MSG_FAILED
                finalResultMsg = resultMsg
                break
            finally:
                duration = str(datetime.timedelta(seconds=command.duration))
                self.logger.logStatistic(Plan.END_MSG.format(
                    command=index,
                    commands=commandsCount,
                    width=width,
                    description=command.description,
                    resultMsg=resultMsg,
                    duration=duration))
        else:
            finalResultMsg = Plan.RESULT_MSG_OK
        totalDuration = time.time() - startTime
        formattedDuration = str(datetime.timedelta(seconds=totalDuration))
        self.logger.logStatistic(Plan.TOTAL_DURATION_MSG.format(
            executionPlan=self.name,
            result=finalResultMsg,
            duration=formattedDuration))


if __name__ == '__main__':
    from bashcommand import BashCommand

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
        # BashCommand('ls /zonk', 'Zonk'),
        BashCommand('echo 10', 'Tenth echo')]

    p = Plan('Echos', commands)

    '''
    for cmd in p.getCommands([1, 3, 5]):
        print(cmd)
    for cmd in p.getCommandsExcept([1, 3, 5]):
        print(cmd)
    for cmd in p.getCommandsBefore(5):
        print(cmd)
    for cmd in p.getCommandsAfter(5):
        print(cmd)
    for cmd in p.getAllCommands():
        print(cmd)
    print(p)
    '''

    p.execute()
