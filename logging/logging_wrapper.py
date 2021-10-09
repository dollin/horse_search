import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(lineno)d %(funcName)s %(message)s',
)


def wrap(pre, post):
    """ Wrapper """
    def decorate(func):
        """ Decorator """
        def call(*args, **kwargs):
            """ Actual wrapping """
            pre(func, *args)
            result = func(*args, **kwargs)
            post(func)
            return result
        return call
    return decorate


def head(func, *args):
    """ Pre function logging """
    logging.info("Entered %s", func.__name__)
    logging.info(func.__doc__)
    logging.info("Function at line %d in %s" %
                (func.__code__.co_firstlineno, func.__code__.co_filename))
    try:
        logging.warn("The argument %s is %s" % (func.__code__.co_varnames[0], *args))
    except IndexError:
        logging.warn("No arguments")


def tail(func):
    """ Post function logging """
    logging.info("Exited  %s", func.__name__)