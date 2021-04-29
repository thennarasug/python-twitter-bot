import datetime
import logging

def basicconfig(filename, filemode="a", fformat='%(asctime)s,%(msecs)d | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG):
    logfilename = './' + filename + "." + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.log'
    logging.basicConfig(filename=logfilename, filemode=filemode, format=fformat, datefmt=datefmt, level=level)


def loginfo(a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9=""):
    logging.info("{} | {} | {} | {}{}{}{}{}{}".format(a1, a2, a3, a4, a5, a6, a7, a8, a9))


def logerror(a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9=""):
    logging.error("{} | {} | {} | {}{}{}{}{}{}".format(a1, a2, a3, a4, a5, a6, a7, a8, a9))


def logwarn(a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9=""):
    logging.warning("{} | {} | {} | {}{}{}{}{}{}".format(a1, a2, a3, a4, a5, a6, a7, a8, a9))


def logdebug(a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9=""):
    logging.debug("{} | {} | {} | {}{}{}{}{}{}".format(a1, a2, a3, a4, a5, a6, a7, a8, a9))


def logcritical(a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9=""):
    logging.critical("{} | {} | {} | {}{}{}{}{}{}".format(a1, a2, a3, a4, a5, a6, a7, a8, a9))


def logexception(a1="", a2="", a3="", a4="", a5="", a6="", a7="", a8="", a9=""):
    logging.exception("{} | {} | {} | {}{}{}{}{}{}".format(a1, a2, a3, a4, a5, a6, a7, a8, a9))
