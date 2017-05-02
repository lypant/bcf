#!/usr/bin/env python2

from __future__ import print_function
import logging
import logging.config


class Logger():
    '''
    Provides console and file logging services.
    Each log entry is passed to both console and file handlers.
    Filtering based on log levels for each of the handlers is done.
    The console handler by default is configured to show higher level output
    with progress tracking purposes.
    The file handler by default is configured to show same contents as
    the console handler plus additional levels with exact bash command text and
    its output
    '''
    # Aliases to logging levels to match project context
    # Top to bottom - highest to lowest priority
    ERROR = logging.CRITICAL
    STATISTIC = logging.ERROR
    COMMAND = logging.WARNING
    OUTPUT = logging.INFO
    # <RESERVED> = logging.DEBUG # not used at the moment

    def __init__(self,
                 logFile,
                 fileLogLevel=OUTPUT,
                 fileMode='w',
                 consoleLogLevel=STATISTIC,
                 format='<%(asctime)s> %(message)s',
                 datefmt=''):
        '''
        @param logFile path and name of a log file to be created
        @param fileLogLevel lowest level of logs stored in the log file
        @param fileMode file log open mode - write (default) or append
        @param consoleLogLevel lowest level of logs printed to console
        @param format format of each log entry
        @param datefmt format of timestamp used for each log entry
        '''
        dictConf = dict(
            version=1,
            formatters={
                'myFormatter': {
                    'format': format,
                    'datefmt': datefmt}},
            handlers={
                'myConsoleHandler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'myFormatter',
                    'level': consoleLogLevel},
                'myFileHandler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'myFormatter',
                    'level': fileLogLevel,
                    'filename': logFile,
                    'mode': fileMode}},
            loggers={
                'myLogger': {
                    'handlers': ['myConsoleHandler', 'myFileHandler'],
                    'level': Logger.OUTPUT}})
        logging.config.dictConfig(dictConf)
        self.logger = logging.getLogger('myLogger')
        self.logFile = logFile

    def logError(self, msg, *args, **kwargs):
        '''
        Main log level - use to show currently executed command and progress
        @param msg text to be logged
        @param args additional parameters to pass to logging.logger
        @param kwargs additional parameters to pass to logging.logger
        '''
        self.logger.critical(msg, *args, **kwargs)

    def logStatistic(self, msg, *args, **kwargs):
        '''
        Main log level - use to show currently executed command and progress
        @param msg text to be logged
        @param args additional parameters to pass to logging.logger
        @param kwargs additional parameters to pass to logging.logger
        '''
        self.logger.error(msg, *args, **kwargs)

    def logCommand(self, msg, *args, **kwargs):
        '''
        Middle log level - use to show details of bash command to be executed
        @param msg text to be logged
        @param args additional parameters to pass to logging.logger
        @param kwargs additional parameters to pass to logging.logger
        '''
        self.logger.warning(msg, *args, **kwargs)

    def logOutput(self, msg, *args, **kwargs):
        '''
        Low log level - use to show output of the executed bash command
        @param msg text to be logged
        @param args additional parameters to pass to logging.logger
        @param kwargs additional parameters to pass to logging.logger
        '''
        self.logger.info(msg, *args, **kwargs)

    def logException(self, msg, *args, **kwargs):
        '''
        Use in exception handler to provide more data about bash command error
        @param msg text to be logged
        @param args additional parameters to pass to logging.logger
        @param kwargs additional parameters to pass to logging.logger

        '''
        self.logger.exception(msg, *args, **kwargs)


if __name__ == '__main__':
    log = '/tmp/bcf_logger.log'
    print('(check %s for file handler output)' % log)
    logger = Logger(log)
    logger.logStatistic('List root directory...')
    logger.logCommand('ls -l /')
    logger.logOutput('one\ntwo\nthree')
    logger.logStatistic('List root directory...done')
