import logging
import requests

log = logging.getLogger(__name__)


def pgproxy_request_proxies(args):

    # By default, this request will return only working/validated proxies.
    r = requests.get("{}/proxy/request".format(args.pgproxy_url))
    result = r.json()
    proxy_list = result if isinstance(result, list) else [result]

    # Go through the JSON object list and pull out only the URL.
    proxies = []
    for proxy in proxy_list:
        proxies.append(proxy['url'])

    return proxies
