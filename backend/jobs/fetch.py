"""SSRF-safe job page reader: http(s) only, public IPs only, <=3 manual redirects, timeout, size cap."""
import html, ipaddress, re, socket, urllib.error, urllib.request
from urllib.parse import urlparse, urljoin


class FetchError(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _check_host(url):
    p = urlparse(url)
    if p.scheme not in ('http', 'https') or not p.hostname:
        raise FetchError('Only http(s) links are allowed.')
    try:
        infos = socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80))
    except socket.gaierror:
        raise FetchError('That address could not be found.')
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise FetchError('Private or local addresses are blocked.')


def fetch_job_text(url):
    opener = urllib.request.build_opener(_NoRedirect)
    for _ in range(4):
        _check_host(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'SkillPathBot/1.0 (student project)'})
        try:
            with opener.open(req, timeout=8) as r:
                if 'html' not in r.headers.get('Content-Type', 'html') and 'text' not in r.headers.get('Content-Type', ''):
                    raise FetchError('That link is not a readable web page.')
                raw = r.read(1_000_000).decode('utf-8', 'ignore')
                break
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get('Location'):
                url = urljoin(url, e.headers['Location'])
                continue
            raise FetchError(f'The site refused access (HTTP {e.code}).')
        except (urllib.error.URLError, socket.timeout, TimeoutError):
            raise FetchError('The page could not be reached in time.')
    else:
        raise FetchError('Too many redirects.')
    m = re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I)
    title = html.unescape(m.group(1)).strip()[:200] if m else ''
    raw = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    return title, re.sub(r'\s+', ' ', text).strip()
