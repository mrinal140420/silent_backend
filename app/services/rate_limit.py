import time
from collections import defaultdict

WINDOW = 60  # seconds
MAX_REQUESTS_IP = 60
MAX_REQUESTS_TOKEN = 20

_ip_requests = defaultdict(list)
_token_requests = defaultdict(list)


def _clean_old(entries, now):
    return [t for t in entries if now - t < WINDOW]


def allow_ip(ip: str) -> bool:
    now = time.time()
    _ip_requests[ip] = _clean_old(_ip_requests[ip], now)

    if len(_ip_requests[ip]) >= MAX_REQUESTS_IP:
        return False

    _ip_requests[ip].append(now)
    return True


def allow_token(token: str) -> bool:
    now = time.time()
    _token_requests[token] = _clean_old(_token_requests[token], now)

    if len(_token_requests[token]) >= MAX_REQUESTS_TOKEN:
        return False

    _token_requests[token].append(now)
    return True
