# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this is

A static gallery site (served on GitHub Pages) of cartoons made by AI from one long animation prompt, [`prompt.txt`](prompt.txt). Visitors only watch; there is no server and no API key. See [`README.md`](README.md) for the site structure and the `animations.json` fields.

## Making an animation

The owner creates a folder with `./new-animation.sh "name"`, which copies `prompt.txt` into `animations/<slug>/prompt.txt`, and fills in the blanks at the end of that copy (`{{USER_DIRECTION}}`, `{{REFERENCES}}`, `{{DURATION_OR_INFER}}`, `{{ASPECT_RATIO_OR_INFER}}`, `{{VISUAL_DIRECTION_OR_INFER}}`). They then ask you to "make the animation in <slug>".

The owner may instead paste the filled-in prompt (or just the filled-in blanks) into the conversation. Then, before any animation work: create the folder with `./new-animation.sh "<name>"` (use the name they give, or a short one from the subject, and tell them), and save the pasted prompt exactly as `animations/<slug>/prompt.txt`. If only the blanks were pasted, fill them into the copied template rather than rewriting the file. Then continue as below.

When asked:

1. Read `animations/<slug>/prompt.txt` in full and follow it as the brief. Any blank still left as a `{{…}}` placeholder or "infer" is yours to decide.
2. Write the animation as a single self-contained `animations/<slug>/index.html` (canvas or SVG plus inline JavaScript, no external files or network requests). It must fill its window (it is shown in an iframe at the declared aspect ratio). It plays once, then holds its last frame with a "Watch again" prompt; click pauses, and click at the end restarts (copy the playback code at the end of an existing film). Support `?t=SECONDS` to hold a single frame, used for gallery previews.
3. The prompt's drawing tools do not exist here; translate them into code, as the prompt allows. Use the prompt's process for real: plan the dramatic action and keys before writing detail, then check your work by capturing frames with headless Chrome (`--headless=new --screenshot --virtual-time-budget=<ms>`) at several times and comparing them. Fix the largest visible weakness each pass, and keep a copy of the best version so you can restore it rather than polishing past the peak. Put screenshots and working copies in a scratch directory, not in the repo.
4. Do not modify the folder's `prompt.txt`; it is the record of what was asked.
5. Add an entry to [`animations.json`](animations.json): `slug` (the folder name), `title`, `direction` (the filled-in `{{USER_DIRECTION}}`), `type: "html"`, `aspect`, `model` (the model you are), `date` (today), `prompt: "prompt.txt"`. Put any short note on approach in `notes`. Save a still for the gallery card as `animations/<slug>/poster.png` (a headless-Chrome screenshot of `?t=<a telling moment>` at 960x540) and set `poster: "poster.png"`.
6. Tell the owner it is ready at http://localhost:8000 (started with `python3 -m http.server` in the repo root).

Revisions ("more weight", "make it funnier") are direction on the same shot: edit that folder's `index.html`, keep its entry in `animations.json`, and don't create a new folder unless asked.

## Other conventions

- Keep the site plain HTML/CSS/JS with no build step; all paths relative (the site lives under `/AI-Animation/`).
