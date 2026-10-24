#!/usr/bin/env python3
"""Local author tools for the AI Animation site.

Run from the repo root:

    python3 tools/author_server.py

then open http://localhost:8001/tools/author.html

It serves the site like `python3 -m http.server` and adds a small API that the
author page uses to list every animation, create a new animation's folder and
prompt, open Claude Code in a Terminal window to make or revise an animation
(an ordinary interactive session that asks for permission as usual), and
delete animations. It only listens on this computer; on GitHub
Pages, which serves files only, the author page cannot do anything.
"""
import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANIM = ROOT / 'animations'
MANIFEST = ROOT / 'animations.json'
TEMPLATES = {'classic': ROOT / 'prompt.txt', 'scion': ROOT / 'prompt-scion.txt'}
PORT = int(os.environ.get('PORT', '8001'))
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')

BLANKS = {
    '{{USER_DIRECTION}}': 'direction',
    '{{REFERENCES}}': 'references',
    '{{DURATION_OR_INFER}}': 'duration',
    '{{ASPECT_RATIO_OR_INFER}}': 'aspect',
    '{{VISUAL_DIRECTION_OR_INFER}}': 'visual',
}
# The scion prompt has its blanks in one sentence near the top, in square brackets.
SCION_WORK = 'an animated film'
SCION_FORMAT = 'a single self-contained HTML page (canvas or SVG with inline JavaScript)'
SCION_RESOURCES = ('Claude Code on this computer, on the owner\'s subscription, with headless Chrome for checking frames; '
                   'no paid APIs or network services; at most a few subagents at a time, and ask before using more')


def find_claude():
    """The Claude Code command: $CLAUDE_BIN, the PATH, or the copy inside the VS Code extension."""
    if os.environ.get('CLAUDE_BIN'):
        return os.environ['CLAUDE_BIN']
    found = shutil.which('claude')
    if found:
        return found
    home = Path.home()
    for p in [home / '.local/bin/claude', home / '.claude/local/claude']:
        if p.exists():
            return str(p)
    copies = glob.glob(str(home / '.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude'))
    return max(copies, key=os.path.getmtime) if copies else None


def open_in_terminal(request):
    """Open a Terminal window in the repo running Claude Code with this request already sent."""
    claude = find_claude()
    if not claude:
        raise ValueError('Claude Code was not found. Start the server with CLAUDE_BIN set to its path.')
    # Unset any API key from the shell profile so Claude Code uses the subscription login.
    command = f'cd {shlex.quote(str(ROOT))} && env -u ANTHROPIC_API_KEY {shlex.quote(claude)} {shlex.quote(request)}'
    script = command.replace('\\', '\\\\').replace('"', '\\"')
    subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "{script}"',
                    '-e', 'tell application "Terminal" to activate'], check=True, capture_output=True)


def slugify(name):
    # The same rule as new-animation.sh.
    s = re.sub(r'[\s_]+', '-', name.lower())
    s = re.sub(r'[^a-z0-9-]', '', s)
    return re.sub(r'-+', '-', s).strip('-')


def fill_prompt(fields):
    kind = fields.get('template') or 'classic'
    if kind not in TEMPLATES:
        raise ValueError('Unknown prompt template.')
    text = TEMPLATES[kind].read_text(encoding='utf-8')
    v = lambda key: (fields.get(key) or '').strip()
    if kind == 'scion':
        source = f'the direction “{v("direction")}”'
        if v('references'):
            source += f', with these references: “{v("references")}”'
        if v('visual'):
            source += f', and these visual qualities: “{v("visual")}”'
        fmt = f'{SCION_FORMAT}, duration: {v("duration") or "infer"}, aspect ratio: {v("aspect") or "infer"}'
        for blank, value in [('[WORK]', SCION_WORK), ('[DIRECTION AND REFERENCES]', source),
                             ('[FORMAT, DURATION, ASPECT RATIO]', fmt), ('[AVAILABLE RESOURCES]', v('resources') or SCION_RESOURCES)]:
            text = text.replace(blank, value, 1)
        return text
    for blank, key in BLANKS.items():
        text = text.replace(blank, v(key) or 'infer')
    return text


def read_manifest():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


def write_manifest(data):
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def animations():
    """Every folder in animations/: those in the gallery in gallery order, then the rest, newest first."""
    entries = read_manifest()
    by_dir = {}
    for e in entries:
        by_dir.setdefault(e.get('dir') or e['slug'], []).append(e)
    order = list(dict.fromkeys(e.get('dir') or e['slug'] for e in entries))
    for p in sorted((p for p in ANIM.iterdir() if p.is_dir()), key=lambda p: -p.stat().st_mtime):
        if p.name not in order:
            order.append(p.name)
    out = []
    for d in order:
        p = ANIM / d
        if not p.is_dir():
            continue
        es = by_dir.get(d, [])
        out.append({
            'dir': d,
            'title': es[0]['title'] if es else d,
            'entries': [{'slug': e['slug'], 'title': e['title'], 'file': e.get('file', 'index.html'),
                         'section': e.get('section', 'fiction'), 'model': e.get('model'), 'date': e.get('date')}
                        for e in es],
            'hasIndex': (p / 'index.html').exists(),
            'poster': (es[0].get('poster') if es else None) or ('poster.png' if (p / 'poster.png').exists() else None),
            'previewTime': es[0].get('previewTime') if es else None,
            'hasPrompt': (p / 'prompt.txt').exists(),
        })
    return out


def folder(slug):
    if not slug or not SLUG_RE.match(slug) or not (ANIM / slug).is_dir():
        raise ValueError('There is no animation folder by that name.')
    return ANIM / slug


# ---------- API ----------

def api_list(_):
    return {'animations': animations(), 'scionResources': SCION_RESOURCES,
            'templates': [k for k, p in TEMPLATES.items() if p.exists()]}


def api_create(body):
    if not (body.get('direction') or '').strip():
        raise ValueError('Paste a text or direction first.')
    slug = slugify(body.get('name') or '')
    if not slug:
        raise ValueError('Give the animation a name with some letters or numbers in it.')
    if (ANIM / slug).exists():
        raise ValueError(f'animations/{slug} already exists. Pick another name.')
    (ANIM / slug).mkdir(parents=True)
    (ANIM / slug / 'prompt.txt').write_text(fill_prompt(body), encoding='utf-8')
    return {'slug': slug}


def api_claude(body):
    slug = folder(body.get('slug')).name
    notes = (body.get('notes') or '').strip()
    if body.get('revise'):
        if not notes:
            raise ValueError('Write the revision first.')
        request = f'Revise the animation in animations/{slug}: {notes}'
    else:
        request = f'make the animation in {slug}'
    open_in_terminal(request)
    return {'request': request}


def api_delete(body):
    p = folder(body.get('slug'))
    # Move to the Trash rather than erase, so a mistake can be undone.
    trash = Path.home() / '.Trash'
    target = trash / p.name
    if target.exists():
        target = trash / f"{p.name} {time.strftime('%Y-%m-%d %H.%M.%S')}"
    shutil.move(str(p), str(target))
    data = read_manifest()
    kept = [e for e in data if (e.get('dir') or e['slug']) != p.name]
    if len(kept) != len(data):
        write_manifest(kept)
    return {'trashed': str(target), 'entriesRemoved': len(data) - len(kept)}


ROUTES = {('GET', '/api/animations'): api_list, ('POST', '/api/create'): api_create,
          ('POST', '/api/claude'): api_claude, ('POST', '/api/delete'): api_delete}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def local_only(self):
        # Refuse requests that were not addressed to this computer (guards against DNS rebinding).
        host = (self.headers.get('Host') or '').split(':')[0]
        if host not in ('localhost', '127.0.0.1'):
            self.send_error(403)
            return False
        return True

    def send_json(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def route(self, method):
        fn = ROUTES.get((method, self.path.split('?')[0]))
        if not fn:
            return False
        body = {}
        if method == 'POST':
            # A custom header other websites cannot send without permission, so only the author page can act.
            if self.headers.get('X-Author') != '1':
                self.send_error(403)
                return True
            n = int(self.headers.get('Content-Length') or 0)
            body = json.loads(self.rfile.read(n) or b'{}')
        try:
            self.send_json(200, fn(body))
        except ValueError as e:
            self.send_json(400, {'error': str(e)})
        except Exception as e:  # report anything unexpected to the page
            self.send_json(500, {'error': f'{type(e).__name__}: {e}'})
        return True

    def do_GET(self):
        if self.local_only() and not self.route('GET'):
            super().do_GET()

    def do_POST(self):
        if self.local_only() and not self.route('POST'):
            self.send_error(404)


if __name__ == '__main__':
    print(f'Author page: http://localhost:{PORT}/tools/author.html  (Ctrl+C to stop)')
    try:
        ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
