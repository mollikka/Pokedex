from datetime import datetime

from urllib.request import Request, urlopen
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from config import CACHE_DIR, LOCK_DIR, EXTERNAL_EXPIRE_TIME

cache_opts = {
    'cache.data_dir': 'cache/data',
    'cache.lock_dir': 'cache/lock',
    'cache.regions': 'external',
    'cache.external.type': 'file',
    'cache.external.expire': EXTERNAL_EXPIRE_TIME,
}
cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.region('external')
def get_external(url):
    http_request = urlopen(Request(url, headers={'User-Agent':'browser'}))
    response = http_request.read().decode("utf-8")
    return response
