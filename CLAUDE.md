# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this is

A static gallery site (served on GitHub Pages) of cartoons made by AI from one long animation prompt, [`prompt.txt`](prompt.txt), or from the alternative [`prompt-scion.txt`](prompt-scion.txt). Visitors only watch; there is no server and no API key. See [`README.md`](README.md) for the site structure and the `animations.json` fields.

## Making an animation

The owner creates a folder with `./new-animation.sh "name"`, which copies `prompt.txt` into `animations/<slug>/prompt.txt`, and fills in the blanks at the end of that copy (`{{USER_DIRECTION}}`, `{{REFERENCES}}`, `{{DURATION_OR_INFER}}`, `{{ASPECT_RATIO_OR_INFER}}`, `{{VISUAL_DIRECTION_OR_INFER}}`). They then ask you to "make the animation in <slug>".

There is a second, alternative template, [`prompt-scion.txt`](prompt-scion.txt) (`./new-animation.sh --scion "name"`, or "Scion" on the Author page). It is a production-management prompt rather than a craft manual: creative thesis, quality references, an early test passage, independent critics, recursive inquiry. Its blanks are the bracketed words in one sentence near the top (`[WORK]`, `[DIRECTION AND REFERENCES]`, `[FORMAT, DURATION, ASPECT RATIO]`, `[AVAILABLE RESOURCES]`). Either way the folder's copy is named `prompt.txt`. When following a Scion prompt here:

- The deliverable and everything in steps 2–6 below are unchanged: one self-contained `index.html`, the playback code, `?t=`, the gallery entry and poster.
- The "swarm" and "independent critics" are real subagents, kept within the `[AVAILABLE RESOURCES]` line (by default a few at a time; ask before using more). Give a critic only the brief, the quality bar and the film (or captured frames); do not give it the builder's reasoning or history. Report which checks were made from stills and which from playback.
- The progress page and other working state go in the scratch directory (or an Artifact), not the repo.
- Sound, if the film uses it, must be synthesized in the page (Web Audio), with no external files.

The owner may instead paste the filled-in prompt (or just the filled-in blanks) into the conversation. Then, before any animation work: create the folder with `./new-animation.sh "<name>"` (use the name they give, or a short one from the subject, and tell them), and save the pasted prompt exactly as `animations/<slug>/prompt.txt`. If only the blanks were pasted, fill them into the copied template rather than rewriting the file. Then continue as below.

When asked:

1. Read `animations/<slug>/prompt.txt` in full and follow it as the brief. Any blank still left as a `{{…}}` placeholder or "infer" is yours to decide.
2. Write the animation as a single self-contained `animations/<slug>/index.html` (canvas or SVG plus inline JavaScript, no external files or network requests). It must fill its window (it is shown in an iframe at the declared aspect ratio). It plays once, then holds its last frame with a "Watch again" prompt; click pauses, and click at the end restarts (copy the playback code at the end of an existing film). Support `?t=SECONDS` to hold a single frame, used for gallery previews.
3. The prompt's drawing tools do not exist here; translate them into code, as the prompt allows. Use the prompt's process for real: plan the dramatic action and keys before writing detail, then check your work by capturing frames with headless Chrome (`--headless=new --screenshot --virtual-time-budget=<ms>`) at several times and comparing them. Fix the largest visible weakness each pass, and keep a copy of the best version so you can restore it rather than polishing past the peak. Put screenshots and working copies in a scratch directory, not in the repo.
4. Do not modify the folder's `prompt.txt`; it is the record of what was asked.
5. Add an entry to [`animations.json`](animations.json): `slug` (the folder name), `title`, `direction` (the filled-in `{{USER_DIRECTION}}`), `type: "html"`, `aspect`, `model` (the model you are), `date` (today), `prompt: "prompt.txt"`, and `template: "scion"` if the folder's prompt came from `prompt-scion.txt` (leave it out for the classic prompt; the gallery and watch page show which prompt was used). Put any short note on approach in `notes`. If the film is an essay or technical document rather than fiction, add `section: "essay"` so it appears in the gallery's second section; place the entry next to any other versions of the same film. Save a still for the gallery card as `animations/<slug>/poster.png` (a headless-Chrome screenshot of `?t=<a telling moment>` at 960x540) and set `poster: "poster.png"`.
Caption pacing (the `READ` / `STRETCH` line near the end of each film): English films use `READ = text => 1.2 + words / 2.9, STRETCH = 1.5` (about 175 words a minute, action may slow slightly). Films in another language use the slower `READ = text => 2 + words / 2, STRETCH = 1` (about 120 words a minute; the action is never slowed, scenes hold instead).
6. Tell the owner it is ready at http://localhost:8000 (started with `python3 -m http.server` in the repo root).

Revisions ("more weight", "make it funnier") are direction on the same shot: edit that folder's `index.html`, keep its entry in `animations.json`, and don't create a new folder unless asked.

## Other conventions

- Keep the site plain HTML/CSS/JS with no build step; all paths relative (the site lives under `/AI-Animation/`).
