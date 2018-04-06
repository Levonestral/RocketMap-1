#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import requests
import argparse

sys.path.append('.')

from pogom.proxy import load_proxies, check_proxies

logging.basicConfig(
    format='%(asctime)s [%(threadName)15.15s][%(levelname)8.8s] %(message)s',
    level=logging.INFO)

log = logging.getLogger()


def main():
    args = get_args()
    set_log_and_verbosity(log)

    # Processing proxies if set (load from file, check and overwrite old
    # args.proxy with new working list).
    args.proxy = load_proxies(args)

    if args.proxy and not args.proxy_skip_check:
        args.proxy = check_proxies(args, args.proxy)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        help='Run in the verbose mode.',
                        action='store_true')
    parser.add_argument('-pxsc', '--proxy-skip-check',
                        help='Disable checking of proxies before start.',
                        action='store_true', default=False)
    parser.add_argument('-pxt', '--proxy-test-timeout',
                        help='Timeout settings for proxy checker in seconds.',
                        type=int, default=5)
    parser.add_argument('-pxre', '--proxy-test-retries',
                        help=('Number of times to retry sending proxy ' +
                              'test requests on failure.'),
                        type=int, default=0)
    parser.add_argument('-pxbf', '--proxy-test-backoff-factor',
                        help=('Factor (in seconds) by which the delay ' +
                              'until next retry will increase.'),
                        type=float, default=0.25)
    parser.add_argument('-pxc', '--proxy-test-concurrency',
                        help=('Async requests pool size.'), type=int,
                        default=0)
    check = parser.add_mutually_exclusive_group()
    check.add_argument('-px', '--proxy',
                       help='Proxy url (e.g. socks5://127.0.0.1:9050)',
                       action='append')
    check.add_argument('-pxf', '--proxy-file',
                       help=('Load proxy list from text file (one proxy ' +
                             'per line), overrides -px/--proxy.'))
    check.add_argument('-pgpru', '--pgproxy-url', default=None,
                       help='URL of PGProxy proxy manager.')

    args = parser.parse_args()

    if not args.proxy_file and not args.proxy and not args.pgproxy_url:
        log.error('You must supply a proxy file, list or PGProxy URL.')
        exit(1)

    return args


def set_log_and_verbosity(log):
    args = get_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    # These are very noisy, let's shush them up a bit.
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    # This sneaky one calls log.warning() on every retry.
    urllib3_logger = logging.getLogger(requests.packages.urllib3.__package__)
    urllib3_logger.setLevel(logging.ERROR)


if __name__ == '__main__':
    main()
