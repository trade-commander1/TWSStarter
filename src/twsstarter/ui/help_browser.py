from __future__ import annotations
import re
import tempfile
import webbrowser
from pathlib import Path
from twsstarter.i18n import tr, current as lang_current
from twsstarter.resources.help_images import DATA_URIS

_TEMPLATE = """\
<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TWSStarter — Help</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', sans-serif;
    max-width: 780px;
    margin: 40px auto;
    padding: 0 24px 60px;
    color: #1e293b;
    line-height: 1.7;
    font-size: 15px;
  }}
  h2 {{
    color: #1e40af;
    font-size: 22px;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 8px;
    margin-top: 0;
  }}
  h3 {{
    color: #1e3a8a;
    font-size: 16px;
    margin-top: 32px;
  }}
  p {{
    margin: 10px 0;
  }}
  code {{
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.88em;
    font-family: 'Cascadia Code', 'Consolas', monospace;
  }}
  span[style*="color:#334155"] {{
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #334155;
    vertical-align: middle;
    margin-right: 2px;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 28px 0;
  }}
  .callout {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 18px 0 8px;
    font-size: 14px;
  }}
  .callout b {{
    color: #1e40af;
  }}
  figure.shot {{
    margin: 18px 0;
    text-align: center;
  }}
  figure.shot img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12);
  }}
  .footer {{
    margin-top: 48px;
    font-size: 12px;
    color: #94a3b8;
    border-top: 1px solid #e2e8f0;
    padding-top: 12px;
  }}
</style>
</head>
<body>
{body}
<div class="footer">© 2024 trade-commander.de — TWSStarter</div>
</body>
</html>"""


def _embed_images(body: str) -> str:
    """Replace [[IMG:<key>]] placeholders with inline <img> (base64 data URIs).
    Unknown placeholders are dropped so no broken image or literal token shows."""
    for key, uri in DATA_URIS.items():
        body = body.replace(
            f"[[IMG:{key}]]",
            f'<figure class="shot"><img src="{uri}" alt=""></figure>',
        )
    return re.sub(r"\[\[IMG:[a-z0-9_]+\]\]", "", body)


def open_help_in_browser() -> None:
    lang = lang_current()
    html = _TEMPLATE.format(lang=lang, body=_embed_images(tr('help_text')))
    tmp = Path(tempfile.gettempdir()) / f"twsstarter_help_{lang}.html"
    tmp.write_text(html, encoding='utf-8')
    webbrowser.open(tmp.as_uri())
