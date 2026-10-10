# AI-Animation

A small gallery of hand-drawn style cartoons made by AI models, part of the Distant Writing projects.

Every animation starts from the same long prompt, [`prompt.txt`](prompt.txt), which asks the model to work like a classical animation studio (key poses, in-betweens, multiplane depth, camera moves). The blanks at the end of the prompt are filled in with the subject of each cartoon. The animations are made ahead of time and uploaded, so visitors to the site only watch them: no API key or server is needed.

The site is served with GitHub Pages at https://jdbolter.github.io/AI-Animation/.

## Making a new animation

1. Create its folder and a copy of the prompt:

   ```
   ./new-animation.sh "Frog Buys Groceries"
   ```

   This makes `animations/frog-buys-groceries/prompt.txt`. The folder name is the name you give, lowercased, with hyphens for spaces and other characters dropped. It also appears in the page's web address.
2. Open that `prompt.txt` and fill in the blanks at the end: the subject (required), and references, length, aspect ratio and visual style (or write "infer").
3. Ask Claude Code, in this repo: "make the animation in frog-buys-groceries". It follows the steps in [`CLAUDE.md`](CLAUDE.md): it writes the animation as `index.html` in that folder, checks it frame by frame, and adds it to `animations.json` so it appears in the gallery.

## Adding an animation by hand

If an animation was made elsewhere:

1. Make a folder in `animations/` with a short name, for example `animations/frog-groceries/`.
2. Put the animation in it:
   - an HTML, SVG or canvas animation as `index.html`, or
   - a video file (MP4 or WebM, well under GitHub's 100 MB file limit).
3. Optionally add `prompt.txt` (the full prompt you used), `direction.txt` (just the subject) and a still image for the gallery card, such as `poster.png`.
4. Add an entry to [`animations.json`](animations.json):

   ```json
   {
     "slug": "frog-groceries",
     "title": "Frog Buys Groceries",
     "direction": "frog buys groceries",
     "type": "html",
     "aspect": "16 / 9",
     "model": "Claude Opus 5.5",
     "date": "2026-10-09",
     "prompt": "prompt.txt",
     "notes": "Anything worth saying about how it was made."
   }
   ```

   `slug` must match the folder name. For a video, use `"type": "video"` and `"file": "frog.mp4"`. `poster`, `model`, `date`, `prompt`, `notes`, `aspect` and `previewTime` are optional. Without a poster, the gallery card plays the animation itself; for an HTML animation that supports `?t=` (holding one frame), `previewTime` shows a still from that second instead. The gallery has two sections, Fiction and Essays/Technical documents: add `"section": "essay"` for the second; entries without it are fiction. Cards appear in the order of `animations.json` within each section.

## Previewing locally

The pages load `animations.json` and `prompt.txt`, which browsers block when a file is opened straight from disk. Run a local server from this folder instead:

```
python3 -m http.server
```

Then open http://localhost:8000.

## Publishing

Push to `main`. GitHub Pages is set to deploy from the `main` branch, root folder (Settings → Pages → Build and deployment → Deploy from a branch). The `.nojekyll` file stops GitHub's Jekyll step from touching the files, since Jekyll's template language uses the same `{{ }}` markers as the prompt's blanks.
