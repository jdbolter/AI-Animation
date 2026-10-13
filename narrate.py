#!/usr/bin/env python3
"""Generate a reader's voice for a film's captions.

    python3 narrate.py the-sunday-bus --samples     # a few lines in several voices, to choose one
    python3 narrate.py the-sunday-bus               # one clip per caption, in the chosen VOICE
    python3 narrate.py der-sonntagsbus --lang de --samples   # the same for a German film
    python3 narrate.py o-autocarro-de-domingo --lang pt --samples   # European Portuguese

Writes animations/<slug>/audio/<id>.mp3 and audio/narration.js (the clip list with durations,
which the film's narrated.html reads). It reads every quoted line in the film's SHOTS list: the
captions, and `say` lines spoken without a caption. A line followed by a language code, as in
['end', 'To fit in.', 'en'], is read in that language (an English line in a Portuguese film gets
a light Portuguese accent). A clip is named after its text, voice and instructions, so
re-running after editing one line only regenerates that clip.

Needs OPENAI_API_KEY in the environment. The speech service is used only here, when the
film is made; visitors just play the mp3 files. To use another service (e.g. Speechify),
replace speak() below; nothing else depends on the provider.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, urllib.request, urllib.error

MODEL = 'gpt-4o-mini-tts'
VOICE = 'ballad'  # chosen after listening to --samples
SAMPLE_VOICES = ['fable', 'marin', 'cedar', 'ballad', 'sage', 'onyx']
# How the reader should sound, by language of the film (--lang). The voices are multilingual:
# the text's language decides what they speak; these instructions set accent and manner.
INSTRUCTIONS = {
    'en': (
        'Accent: an educated Southern English (Received Pronunciation) reader; non-rhotic, '
        'with British vowels throughout (e.g. "path", "half", "can\'t" with a long a). '
        'Tone: warm, quiet and literary, like a reader of a short story on BBC Radio 4. '
        'Dialogue is read lightly, without acting out voices. '
        'Pacing: measured and unhurried, with natural pauses at commas and full stops.'
    ),
    'de': (
        'Sprache: Deutsch. Akzent: reines, gepflegtes Hochdeutsch (Bühnenaussprache), wie ein '
        'Sprecher im Deutschlandfunk; keinerlei englischer oder regionaler Akzent, deutsches r, '
        'deutsche Vokale und Umlaute. '
        'Ton: warm, ruhig und literarisch, wie bei einer Lesung einer Kurzgeschichte im Radio. '
        'Dialoge werden leicht gelesen, ohne Stimmen zu spielen. '
        'Tempo: gemessen und ohne Eile, mit natürlichen Pausen an Kommas und Punkten.'
    ),
    # European Portuguese, spelled out feature by feature: models drift toward Brazilian.
    'pt': (
        'Language: European Portuguese (português europeu, pt-PT), as spoken in Lisbon. '
        'This must NOT sound Brazilian. Use European pronunciation throughout: strongly reduced, '
        'almost silent unstressed vowels (e.g. "de" and "que" with a reduced e, "pequeno" as "p\'queno"); '
        'final and preconsonantal s pronounced "sh" (e.g. "três", "mais", "gestos"); '
        't and d stay hard before i and e (never "tchi" or "dji"); '
        'final l stays a dark l (never "w"); European rhythm and intonation, consonant-heavy and fast-flowing. '
        'Voice: a calm, educated Lisbon reader, like a literary reading on RTP Antena 2. '
        'Dialogue is read lightly, without acting out voices. '
        'Pacing: measured and unhurried, with natural pauses at commas and full stops.'
    ),
    # English lines inside a Portuguese film: the same Lisbon reader, now speaking English.
    'en@pt': (
        'Language: English, read by a native speaker of European Portuguese from Lisbon who speaks '
        'English fluently and clearly, with a light, natural Portuguese accent (not exaggerated, '
        'not a caricature). Read each phrase as a short item in a list, with a small pause after each. '
        'Tone: warm and friendly, like a language teacher. Pacing: unhurried.'
    ),
}


def speak(text, voice, instructions):
    """Return mp3 bytes for one line of text."""
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        sys.exit('Set OPENAI_API_KEY first (export OPENAI_API_KEY=...).')
    body = json.dumps({'model': MODEL, 'voice': voice, 'input': text,
                       'instructions': instructions, 'response_format': 'mp3'}).encode()
    req = urllib.request.Request('https://api.openai.com/v1/audio/speech', data=body,
                                 headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f'Speech request failed ({e.code}): {e.read().decode(errors="replace")[:500]}')


def duration(path):
    """Length of an audio file in seconds (afinfo on macOS, else ffprobe)."""
    try:
        out = subprocess.run(['afinfo', path], capture_output=True, text=True).stdout
        m = re.search(r'estimated duration:\s*([\d.]+)', out)
        if m:
            return float(m.group(1))
    except FileNotFoundError:
        pass
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def captions(page):
    """Spoken lines in order, as (text, language or None), from the film's SHOTS list:
    every quoted string except arguments to card functions (e.g. wordCard(1, 'caber'))
    and the 'end' marker; a string followed by a two-letter code is in that language."""
    src = open(page, encoding='utf-8').read()
    shots = src[src.index('const SHOTS = ['):]
    shots = shots[:shots.index('\n];')]
    out = []
    for m in re.finditer(r"'((?:[^'\\]|\\.)*)'(?:\s*,\s*'([a-z]{2})')?", shots):
        text = re.sub(r"\\(.)", r'\1', m.group(1))
        if text == 'end' or re.search(r'\w+\(\d+,\s*$', shots[:m.start()][-40:]):
            continue
        out.append((text, m.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slug')
    ap.add_argument('--page', help='film file to read lines from (default narrated.html, else index.html)')
    ap.add_argument('--voice', default=VOICE)
    ap.add_argument('--lang', default='en', choices=sorted(k for k in INSTRUCTIONS if '@' not in k), help='language of the film (sets the reading instructions)')
    ap.add_argument('--samples', action='store_true', help='read a few lines in several voices')
    a = ap.parse_args()
    instr = INSTRUCTIONS[a.lang]
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'animations', a.slug)
    page = a.page or ('narrated.html' if os.path.exists(os.path.join(folder, 'narrated.html')) else 'index.html')
    caps = captions(os.path.join(folder, page))
    if not caps:
        sys.exit('No captions found.')

    if a.samples:
        out = os.path.join(tempfile.gettempdir(), 'narration-samples', a.slug + '-' + a.lang)
        os.makedirs(out, exist_ok=True)
        main_lines = [t for t, l in caps if not l]
        text = ' '.join(main_lines[1:4] + [c for c in main_lines if c[0] in '“„»«—"'][:1])
        for v in SAMPLE_VOICES:
            path = os.path.join(out, v + '.mp3')
            open(path, 'wb').write(speak(text, v, instr))
            print(f'{v}: {path} ({duration(path):.1f}s)')
        subprocess.run(['open', out]) if sys.platform == 'darwin' else None
        return

    audio = os.path.join(folder, 'audio')
    os.makedirs(audio, exist_ok=True)
    manifest = os.path.join(audio, 'narration.js')
    old = {}
    if os.path.exists(manifest):
        m = re.search(r'=\s*(\{.*\});?\s*$', open(manifest, encoding='utf-8').read(), re.S)
        if m:
            old = {c['tag']: c for c in json.loads(m.group(1))['clips']}
    clips = []
    for text, lang in caps:
        # a line in another language uses that language's instructions (with this film's accent if there is one)
        ins = instr if not lang or lang == a.lang else INSTRUCTIONS.get(f'{lang}@{a.lang}', INSTRUCTIONS.get(lang, instr))
        tag = hashlib.sha1('\n'.join([MODEL, a.voice, ins, text]).encode()).hexdigest()[:12]
        name = tag + '.mp3'
        path = os.path.join(audio, name)
        prev = old.get(tag)
        if prev and os.path.exists(os.path.join(audio, prev['file'])):
            if prev['file'] != name:
                os.rename(os.path.join(audio, prev['file']), path)
            clips.append({**prev, 'file': name}); continue
        print(f'{name}  {text[:70]}')
        open(path, 'wb').write(speak(text, a.voice, ins))
        clips.append({'file': name, 'dur': round(duration(path), 2), 'text': text, 'tag': tag})
    for f in os.listdir(audio):
        if f.endswith(('.mp3', '.m4a')) and f not in {c['file'] for c in clips}:
            os.remove(os.path.join(audio, f))
    data = {'model': MODEL, 'voice': a.voice, 'lang': a.lang, 'clips': clips}
    open(manifest, 'w', encoding='utf-8').write(
        '// Written by narrate.py: one clip per caption, with its length in seconds.\n'
        'window.NARRATION = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
    total = sum(c['dur'] for c in clips)
    print(f'{len(clips)} clips, {total / 60:.1f} minutes of speech, voice {a.voice}. Wrote {manifest}')


if __name__ == '__main__':
    main()
