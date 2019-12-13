import quickfix
import copy
import uuid
import random
import datetime
import yaml
from twisted.internet import task


class MarketDataError(quickfix.Exception):
    pass


class FixSimError(Exception):
    pass


def instance_safe_call(fn):
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except quickfix.Exception as e:
            raise e
        except Exception as e:
            self.logger.exception(str(e))

    return wrapper


class FixSimApplication(quickfix.Application):
    def __init__(self, fixVersion, logger):
        super(FixSimApplication, self).__init__()
        self.fixVersion = fixVersion
        self.logger = logger

    @instance_safe_call
    def sendToTarget(self, message, sessionID):
        if sessionID is None:
            raise FixSimError("Invalid Fix Session")

        self.logger.info("FixSimApplication:SEND TO TARGET %s", message)
        quickfix.Session.sendToTarget(message, sessionID)

    @instance_safe_call
    def fromApp(self, message, sessionID):
        print "FROM APP"
        fixMsgType = quickfix.MsgType()
        beginString = quickfix.BeginString()
        message.getHeader().getField(beginString)
        message.getHeader().getField(fixMsgType)
        msgType = fixMsgType.getValue()

        self.logger.info("FixSimApplication.fromApp: Message type %s", str(msgType))
        self.dispatchFromApp(msgType, message, beginString, sessionID)


class IncrementID(object):
    def __init__(self):
        self.__value = 0

    def generate(self):
        self.__value += 1
        return str(self.__value)


def float_range(first, last, step):
    if last < 0:
        raise ValueError("last float is negative")

    result = []
    while True:
        if first >= last:
            return result

        result.append(first)
        first += step


def create_logger(config):
    import logging
    import logging.handlers

    def syslog_logger():
        logger = logging.getLogger('FixClient')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler()
        logger.addHandler(handler)
        return logger

    def file_logger(fname):
        logger = logging.getLogger('FixClient')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(fname)
        logger.addHandler(handler)
        return logger

    logcfg = config.get('logging', None)
    if not logging:
        return syslog_logger()

    target = logcfg['target']
    if target == 'syslog':
        logger = syslog_logger()
    elif target == 'file':
        filename = logcfg['filename']
        logger = file_logger(filename)
    else:
        raise FixSimError("invalid logger " + str(target))

    logger.addHandler(logging.StreamHandler())
    return logger


def load_yaml(path):
    with open(path, 'r') as stream:
        cfg = yaml.load(stream)

    return cfg


def create_fix_version(config):
    # ONLY FIX44 FOR NOW
    fix_version = config.get('fix_version', 'FIX44')
    if fix_version != 'FIX44':
        raise FixSimError("Unsupported fix version %s" % str(fix_version))

    import quickfix44

    return quickfix44
