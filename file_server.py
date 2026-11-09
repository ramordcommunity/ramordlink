# -*- coding: utf-8 -*-
"""
Ramord Link - Multilingual Web HTTP File Sharing Server
Supports Drag & Drop uploads, atomic storage, disk quota protection, and 6-language UI.
"""

from __future__ import annotations
import html
import mimetypes
import os
import shutil
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from i18n import t

FILE_PORT = 8080
DEFAULT_SHARE_DIR = Path.home() / "Genel"
MAX_UPLOAD_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB max upload limit
MIN_FREE_SPACE_BUFFER = 100 * 1024 * 1024  # 100 MB safety buffer


def human_size(num: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num < 1024 or unit == "TB":
            return f"{int(num)} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"


PAGE_TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{web_title}</title>
<style>
  :root {
    --bg: #F4F1EA;
    --card: #EFECE6;
    --text: #2B2A27;
    --dim: #6B6862;
    --accent: #1A3328;
    --accent-hover: #284e3e;
    --accent-text: #F4F1EA;
    --card-border: rgba(26, 51, 40, 0.15);
    --hover-bg: rgba(26, 51, 40, 0.08);
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #080C0A;
      --card: #101613;
      --text: #E8E4DA;
      --dim: #8A948E;
      --accent: #589E7B;
      --accent-hover: #6db893;
      --accent-text: #080C0A;
      --card-border: rgba(88, 158, 123, 0.20);
      --hover-bg: rgba(88, 158, 123, 0.12);
    }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; min-height: 100vh; }
  .wrap { max-width: 820px; margin: 0 auto; padding: 32px 20px 60px; }
  .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid var(--card-border); padding-bottom: 16px; }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-logo { width: 42px; height: 42px; border-radius: 10px; background: var(--card); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px var(--hover-bg); border: 1px solid var(--card-border); overflow: hidden; }
  .brand-logo img { width: 100%; height: 100%; object-fit: contain; }
  h1 { font-size: 20px; margin: 0; font-weight: 700; color: var(--text); }
  .lang-picker a { color: var(--dim); text-decoration: none; margin-left: 10px; font-size: 13px; font-weight: 600; padding: 4px 8px; border-radius: 6px; transition: all .2s ease; }
  .lang-picker a:hover { color: var(--accent); background: var(--hover-bg); }
  .lang-picker a.active { color: var(--accent-text); background: var(--accent); font-weight: 700; }
  .sub { color: var(--dim); font-size: 13px; margin: 0 0 20px; word-break: break-all; }
  .drop { border: 2px dashed var(--card-border); border-radius: 16px; padding: 32px; text-align: center; color: var(--dim); background: var(--card); transition: all .2s ease; cursor: pointer; }
  .drop:hover, .drop.over { border-color: var(--accent); background: var(--hover-bg); color: var(--text); box-shadow: 0 6px 20px var(--hover-bg); }
  .drop p { margin: 6px 0; }
  .drop strong { color: var(--accent); font-size: 16px; }
  input[type=file] { display: none; }
  .status { color: var(--accent); min-height: 20px; font-size: 13px; margin-top: 10px; font-weight: 600; }
  table { width: 100%; border-collapse: collapse; margin-top: 28px; background: var(--card); border: 1px solid var(--card-border); border-radius: 14px; overflow: hidden; }
  th { text-align: left; color: var(--dim); font-size: 12px; font-weight: 700; padding: 13px 16px; border-bottom: 1px solid var(--card-border); background: var(--card); }
  td { padding: 13px 16px; border-bottom: 1px solid var(--card-border); font-size: 14px; }
  td:nth-child(2), td:nth-child(3) { color: var(--dim); white-space: nowrap; font-size: 13px; }
  a.file-link { color: var(--accent); text-decoration: none; font-weight: 600; }
  a.file-link:hover { text-decoration: underline; color: var(--accent-hover); }
  .empty { text-align: center; color: var(--dim); padding: 36px; font-size: 14px; }
  .footer { margin-top: 40px; text-align: center; color: var(--dim); font-size: 12px; }
  .footer a { color: var(--accent); text-decoration: none; }
</style>
</head>
<body>
<div class="wrap">
  <div class="top-bar">
    <div class="brand">
      <div class="brand-logo"><img src="/logo.svg" alt="Ramord Link Logo"></div>
      <h1>{web_title}</h1>
    </div>
    <div class="lang-picker">
      <a href="?lang=tr" class="{tr_active}">TR</a>
      <a href="?lang=en" class="{en_active}">EN</a>
      <a href="?lang=de" class="{de_active}">DE</a>
      <a href="?lang=es" class="{es_active}">ES</a>
      <a href="?lang=fr" class="{fr_active}">FR</a>
      <a href="?lang=it" class="{it_active}">IT</a>
    </div>
  </div>

  <p class="sub">{folder_path}</p>

  <div id="drop" class="drop" onclick="document.getElementById('file').click()">
    <p><strong>{web_drop}</strong></p>
    <input id="file" type="file" multiple>
    <p id="status" class="status"></p>
  </div>

  <table>
    <thead><tr><th>{web_file}</th><th>{web_size}</th><th>{web_date}</th></tr></thead>
    <tbody>{file_rows}</tbody>
  </table>

  <div class="footer">
    Ramord Link &middot; <a href="mailto:ramordhelp@gmail.com">ramordhelp@gmail.com</a>
  </div>
</div>

<script>
  const drop = document.getElementById('drop');
  const fileInput = document.getElementById('file');
  const status = document.getElementById('status');

  ['dragenter', 'dragover'].forEach(e => {{
    drop.addEventListener(e, ev => {{ ev.preventDefault(); ev.stopPropagation(); drop.classList.add('over'); }}, false);
  }});
  ['dragleave', 'drop'].forEach(e => {{
    drop.addEventListener(e, ev => {{ ev.preventDefault(); ev.stopPropagation(); drop.classList.remove('over'); }}, false);
  }});
  drop.addEventListener('drop', ev => {{
    const dt = ev.dataTransfer;
    if (dt && dt.files && dt.files.length) uploadFiles(dt.files);
  }}, false);
  fileInput.addEventListener('change', ev => {{
    if (fileInput.files && fileInput.files.length) uploadFiles(fileInput.files);
  }});

  function uploadFiles(files) {{
    let done = 0;
    const total = files.length;
    status.innerText = '{web_uploading}... (0/' + total + ')';
    Array.from(files).forEach(f => {{
      const xhr = new XMLHttpRequest();
      xhr.open('PUT', '/upload/' + encodeURIComponent(f.name), true);
      xhr.onload = () => {{
        done++;
        status.innerText = '{web_uploading}... (' + done + '/' + total + ')';
        if (done === total) {{
          status.innerText = '{web_uploaded}';
          setTimeout(() => location.reload(), 800);
        }}
      }};
      xhr.onerror = () => {{
        status.innerText = '{web_failed}: ' + f.name;
      }};
      xhr.send(f);
    }});
  }}
</script>
</body>
</html>
"""


class FileShareHandler(BaseHTTPRequestHandler):
    server_version = "RamordLink/1.0"
    directory = str(DEFAULT_SHARE_DIR)

    def log_message(self, *args) -> None:
        pass

    def _get_lang(self) -> str:
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "lang" in params and params["lang"][0] in ("tr", "en", "de", "es", "fr", "it"):
            return params["lang"][0]
        # Check Accept-Language
        accept = self.headers.get("Accept-Language", "").lower()
        for l in ("tr", "de", "es", "fr", "it"):
            if accept.startswith(l):
                return l
        return "en"

    def _send(self, code: int, body: bytes = b"", ctype: str = "text/plain; charset=utf-8") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _listing(self) -> None:
        base = Path(self.directory)
        cur_lang = self._get_lang()
        try:
            items = sorted(base.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError:
            items = []
        rows = []
        for item in items:
            if item.name.endswith(".part"):
                continue
            try:
                stat = item.stat()
            except OSError:
                continue
            name = html.escape(item.name)
            qname = urllib.parse.quote(item.name, safe="")
            size = "—" if item.is_dir() else human_size(stat.st_size)
            when = datetime.fromtimestamp(stat.st_mtime).strftime("%d.%m.%Y %H:%M")
            rows.append(
                f'<tr><td><a class="file-link" href="/files/{qname}">{name}</a></td>'
                f"<td>{size}</td><td>{when}</td></tr>"
            )
        file_rows = "\n".join(rows) or f'<tr><td colspan="3" class="empty">{t("web_empty", cur_lang)}</td></tr>'
        
        body = PAGE_TEMPLATE.format(
            lang=cur_lang,
            web_title=t("web_title", cur_lang),
            folder_path=html.escape(str(base)),
            web_drop=t("web_drop", cur_lang),
            web_file=t("web_file", cur_lang),
            web_size=t("web_size", cur_lang),
            web_date=t("web_date", cur_lang),
            web_uploading=t("web_uploading", cur_lang),
            web_done=t("web_done", cur_lang),
            file_rows=file_rows,
            tr_active="active" if cur_lang == "tr" else "",
            en_active="active" if cur_lang == "en" else "",
            de_active="active" if cur_lang == "de" else "",
            es_active="active" if cur_lang == "es" else "",
            fr_active="active" if cur_lang == "fr" else "",
            it_active="active" if cur_lang == "it" else "",
        )
        self._send(200, body.encode("utf-8"), "text/html; charset=utf-8")

    def _download(self, name: str) -> None:
        target = Path(self.directory) / Path(name).name
        if not target.is_file():
            self._send(404, b"Not Found")
            return
        ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        try:
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(target.stat().st_size))
            self.send_header(
                "Content-Disposition",
                "attachment; filename*=UTF-8''" + urllib.parse.quote(target.name),
            )
            self.end_headers()
            with target.open("rb") as fh:
                shutil.copyfileobj(fh, self.wfile)
        except OSError:
            pass

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)
        if path in ("/", "/index.html"):
            self._listing()
        elif path == "/logo.svg":
            logo_path = Path(__file__).resolve().parent / "assets/ramord-link.svg"
            if not logo_path.exists():
                logo_path = Path.home() / ".local/share/icons/hicolor/scalable/apps/ramord-link.svg"
            if logo_path.exists():
                self._send(200, logo_path.read_bytes(), "image/svg+xml")
            else:
                self._send(404, b"Not Found")
        elif path.startswith("/files/"):
            self._download(path[len("/files/"):])
        else:
            self._send(404, b"Not Found")

    def do_PUT(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)
        if not path.startswith("/upload/"):
            self._send(404, b"Not Found")
            return
        name = os.path.basename(path[len("/upload/"):])
        if not name or name in (".", ".."):
            self._send(400, b"Invalid filename")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            self._send(411, b"Length Required")
            return
        if length > MAX_UPLOAD_SIZE:
            self._send(413, b"Payload Too Large (Max 4 GB)")
            return

        # Check free disk space
        try:
            usage = shutil.disk_usage(self.directory)
            if usage.free < (length + MIN_FREE_SPACE_BUFFER):
                self._send(507, b"Insufficient Storage on host")
                return
        except OSError:
            pass

        target = Path(self.directory) / name
        temp = target.with_name(f"{target.name}.{os.getpid()}.part")
        try:
            remaining = length
            with temp.open("wb") as fh:
                while remaining > 0:
                    chunk = self.rfile.read(min(1 << 16, remaining))
                    if not chunk:
                        break
                    fh.write(chunk)
                    remaining -= len(chunk)
            if remaining:
                temp.unlink(missing_ok=True)
                self._send(400, b"Incomplete data")
                return
            os.replace(temp, target)
            self._send(200, b"OK")
        except OSError as exc:
            temp.unlink(missing_ok=True)
            self._send(500, str(exc).encode())
