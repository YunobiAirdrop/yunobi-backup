#!/usr/bin/env python3
"""OAuth2 untuk yt-growth: 1 token per channel (brand account), disimpan 600.

Alur (per channel, sekali saja):
  1. python auth.py auth-url SLUG        -> buka URL di browser HP/laptop
  2. Di layar "Choose an account", PILIH CHANNEL yang sesuai (bukan akun utama)
  3. Setujui, lalu salin ?code=... dari address bar (abaikan "unable to connect")
  4. python auth.py exchange SLUG KODE   -> token tersimpan di ~/.hermes/yt-growth/tokens/
"""
import json
import os
import sys
from pathlib import Path

BASE = Path.home() / ".hermes" / "yt-growth"
CLIENT_SECRETS = BASE / "client_secret.json"
TOKENS_DIR = BASE / "tokens"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",  # butuh untuk videos.update
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
REDIRECT = "http://localhost:8080/"


def _need_client():
    if not CLIENT_SECRETS.exists():
        sys.exit(f"client_secret.json belum ada di {CLIENT_SECRETS}.\nIkuti SETUP.md langkah 1-4 dulu.")


def _pkce_store():
    return BASE / "pkce.json"


def make_auth_url(slug):
    """Buat URL otorisasi + simpan PKCE verifier untuk exchange nanti."""
    _need_client()
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
    flow.redirect_uri = REDIRECT
    url, _ = flow.authorization_url(access_type="offline", prompt="consent select_account")
    store = _pkce_store()
    data = json.loads(store.read_text()) if store.exists() else {}
    data[slug] = flow.code_verifier
    BASE.mkdir(parents=True, exist_ok=True)
    store.write_text(json.dumps(data))
    os.chmod(store, 0o600)
    return url


def auth_url(slug):
    url = make_auth_url(slug)
    print(f"Channel: {slug}\n")
    print("Buka URL ini di browser (pastikan login khususstokyunobi@gmail.com):\n")
    print(url)
    print("\nPENTING: di layar 'Choose an account', pilih CHANNEL yang sesuai daftar")
    print("(Lima Misteri / Strange Tales / dst), BUKAN akun Google utama.")
    print("\nSetelah 'unable to connect', salin kode dari address bar (?code=...) lalu:")
    print(f"  python auth.py exchange {slug} KODE_TADI")


def exchange(slug, code):
    _need_client()
    from urllib.parse import unquote
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
    flow.redirect_uri = REDIRECT
    # kembalikan PKCE verifier yang dipakai saat URL dibuat
    store = _pkce_store()
    if store.exists():
        data = json.loads(store.read_text())
        if slug in data:
            flow.code_verifier = data[slug]
    code = unquote(code.strip())
    flow.fetch_token(code=code)
    TOKENS_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(TOKENS_DIR, 0o700)
    p = TOKENS_DIR / f"{slug}.json"
    p.write_text(flow.credentials.to_json())
    os.chmod(p, 0o600)
    print(f"OK, token tersimpan: {p}")


def get_credentials(slug):
    from google.oauth2.credentials import Credentials
    p = TOKENS_DIR / f"{slug}.json"
    if not p.exists():
        sys.exit(f"Belum ada token untuk '{slug}'. Jalankan: python auth.py auth-url {slug}")
    creds = Credentials.from_authorized_user_file(str(p), SCOPES)
    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
        p.write_text(creds.to_json())
        os.chmod(p, 0o600)
    return creds


def _proxy_http():
    """httplib2.Http dengan proxy VM (termasuk auth) + CA bundle egress.

    google-api-python-client memakai httplib2 yang tidak menangani proxy
    berautentikasi dari env dengan benar (menyebabkan SSL WRONG_VERSION_NUMBER).
    """
    import os
    from urllib.parse import urlparse
    import httplib2

    ca = "/run/hatch/egress-tls/ca-bundle.pem"
    for var in ("https_proxy", "HTTPS_PROXY", "http_proxy", "HTTP_PROXY"):
        val = os.environ.get(var)
        if not val:
            continue
        u = urlparse(val)
        # httplib2.socks bisa None; PROXY_TYPE_HTTP = 3
        proxy_info = httplib2.ProxyInfo(
            3, u.hostname, u.port or 3128,
            proxy_user=u.username, proxy_pass=u.password,
        )
        return httplib2.Http(proxy_info=proxy_info, ca_certs=ca)
    import httplib2 as _h
    return _h.Http(ca_certs=ca)


YT_BASE = "https://www.googleapis.com/youtube/v3"
YA_BASE = "https://youtubeanalytics.googleapis.com/v2"
_CA = "/run/hatch/egress-tls/ca-bundle.pem"


def api_session(slug):
    """requests.Session terotentikasi (uthorized) via proxy VM.

    Dipakai sebagai pengganti googleapiclient/httplib2 yang gagal total
    menembus proxy berautentikasi VM (SSL WRONG_VERSION_NUMBER).
    """
    from google.auth.transport.requests import AuthorizedSession
    creds = get_credentials(slug)
    s = AuthorizedSession(creds)
    s.verify = _CA
    return s


def yt_get(slug, path, params):
    s = api_session(slug)
    r = s.get(YT_BASE + path, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def ya_get(slug, params):
    s = api_session(slug)
    r = s.get(YA_BASE + "/reports", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def yt_put(slug, path, params, body):
    s = api_session(slug)
    r = s.put(YT_BASE + path, params=params, json=body, timeout=30)
    r.raise_for_status()
    return r.json()


def get_service(slug, api="youtube", version="v3"):
    from googleapiclient.discovery import build
    from google_auth_httplib2 import AuthorizedHttp
    creds = get_credentials(slug)
    http = AuthorizedHttp(creds, http=_proxy_http())
    return build(api, version, http=http, cache_discovery=False)


def status():
    if not TOKENS_DIR.exists():
        print("Belum ada token sama sekali.")
        return
    done = sorted(p.stem for p in TOKENS_DIR.glob("*.json"))
    print(f"Token aktif ({len(done)}/17): {', '.join(done) if done else '-'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "auth-url" and len(sys.argv) == 3:
        auth_url(sys.argv[2])
    elif cmd == "exchange" and len(sys.argv) == 4:
        exchange(sys.argv[2], sys.argv[3])
    elif cmd == "status":
        status()
    else:
        print("Pakai: auth.py auth-url SLUG | auth.py exchange SLUG KODE | auth.py status")
