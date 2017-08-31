#!/usr/bin/python3

import logging
import logging.handlers
import os
import argparse
import yaml

def get_argparser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-c', '--config', default='../conf/conf.yaml',
        help='config file path')
    args = parser.parse_args()
    return args


def log_config(config, multiprocessing=False):
    log_file = '.'.join(os.path.splitext(__file__)[:-1])
    log_level = config["logging"].get("level", "INFO")
    log_dir = config["logging"].get("dir", "/var/log/")
    os.makedirs(log_dir, exist_ok=True)

    log_format = '[%(levelname)s]'
    if multiprocessing:
        log_format += '<p%(process)d - %(processName)s>'
    log_format += '<%(module)s>-%(funcName)s: %(message)s --- %(asctime)s'
    log_formatter = logging.Formatter(log_format)

    # add rotate log
    log_file = os.path.join(log_dir, log_file)
    loghandler_file = logging.handlers.TimedRotatingFileHandler(
        log_file, when = 'midnight', interval = 1, backupCount = 7)
    loghandler_file.setFormatter(log_formatter)
    loghandler_file.setLevel(getattr(logging, log_level.upper(), None))

    # add stream log
    loghandler_stream = logging.StreamHandler()
    loghandler_stream.setFormatter(log_formatter)
    loghandler_stream.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.addHandler(loghandler_file)
    logger.addHandler(loghandler_stream)
    logger.setLevel(log_level)


def main():
    args = get_argparser()
    with open(args.config, 'r') as f:
        conf = yaml.load(f)
        log_config(conf)

if __name__ == "__main__":
    main()
