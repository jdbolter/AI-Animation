# Revision 4 — aligned desk hands and the original narrator

2026-10-31 · reiniger-r4 · 344.784 seconds (about 5:45), sixteen scenes at 12 fps.

The user requested straight hand/wrist junctions in the desk inserts, removal of splash-screen subtext, and the original Sunday Bus soundtrack adapted to this version. This supersedes the initial synthesized-sound-only constraint. The original read-aloud version contains narration, so its existing recordings are reused rather than generating a new voice.

## Changes and source boundary

- The insert hand contour has a centered, continuous wrist and cuff. The desk gestures use straight forearms, with a mirrored left hand for the elastic. All title subtext and its decorative rule have been removed.
- All 44 original MP3 recordings listed in `../the-sunday-bus/audio/narration.js` are embedded byte-for-byte in `index.html`. The original voice is documented there as OpenAI `gpt-4o-mini-tts`, voice `fable`. No new speech service was called. The original films and their source audio remain unchanged. The user explicitly authorized reuse for this adaptation; no new license or ownership claim is made.
- Narration is matched to the story text. Several merged captions use consecutive original recordings, separated by a short breath. Caption duration is the greater of reading time or the full spoken duration plus a short tail; recorded speech and walking speed are not stretched.
- The added sentences “She turned the map over.” and “The back was blank.” remain captioned, quiet visual beats. The original final-sentence recording starts after the blank reverse has been shown. No voice is falsely presented as having spoken newly generated text.
- The previous synthesized effects are replaced by the recorded narration. Volume is normal media playback, with mute, pause, seeking and replay. The media clock drives the picture during each spoken clip. A visible loading/failure message and Retry sound action replace silent playback failure.
- Original audio was initially linked as shared MP3s. Browser tests found seeking could restart a recording under the local server; embedding the bytes makes the film self-contained and seekable, including in the gallery’s opaque-origin sandboxed iframe. A seek waits for metadata and the seeked event before resuming.

## Verification

Chrome scanned all **4,138** retimed picture frames: maximum fixed-limb error **4.98×10⁻¹⁴** local units, no geometry failures, no caption overflow, no overlapping voice cues and no caption cut off before its recording ends. Every original clip is scheduled exactly once; only the two new visual sentences are unvoiced.

A native mouse click in the real gallery iframe started decoded narration (readyState 4, media time advancing, unmuted). Pause held both film and media clocks; seek/resume stayed aligned within 0.011 seconds at the sample; mute changed the media element; a seek near one recording’s end progressed into the next file; the original final sentence played after the quiet turn. A deliberately missing test resource produced a visible error and Retry sound restored playback. There were no uncaught exceptions. The decoded original narration sample has duration 7.752 seconds and RMS 0.0552, establishing a nonzero foreground speech signal rather than the earlier quiet synthetic signal. These are browser/decoded-signal checks, not a claim of a human listening session.

Independent shadow_reader verdict: **pass for focused r4 visual changes**, based on four desk inserts, title and ending stills. It found aligned wrists without the previous sideways kink, distinct fingers/thumbs, title without subtext, and the marked front → turn → blank reverse → final sentence order preserved. It did not assess audible narration or continuous film rhythm.

Working captures, schedule and playback evidence: `/tmp/reiniger-r4/`. A recoverable copy of this revision is stored there. The HTML is about 4.95 MB, including audio, and has no external runtime assets or service dependency.

---

## Earlier production record (revision 3)

# Revision 3 — more life, natural arms, blank reverse

2026-10-31 · reiniger-r3 · 316.517 seconds (5:17), sixteen scenes at 12 fps.

The user approved the aesthetic and requested natural resting arms, more acting, faster walking, the original `../the-sunday-bus/index.html` as a blocking guide, and a map turned over to a blank reverse before the final sentence. The original film was read as reference; its instructions were not treated as a new assignment. The original film and original prompt copy are unchanged. `story.txt` contains the revised adaptation text; the inline exposure sheet uses that version.

## Changes

- Both profile arms now flex in the same anatomical direction. Hands follow the forearm direction when relaxed. Reach limits apply before drawing the hand and forearm. The far arm is behind the torso.
- Breathing, small weight transfers, attention changes and head motion continue in standing holds, with fixed feet. Acting overrides the rest pose during an invitation, refusal, reach, bite or sip.
- The library cuts to a drawer insert: a rubber band stretches and breaks, an empty spectacle case opens, photographs move aside, and the map is revealed. Martin walks into the memory, offers repeated invitations, then stops. The calendar settles when invitations end. Separate handbag, alarm and packing shots follow the reference’s progression.
- Coastal root speeds are 116 stage pixels/second before the knee-pain pause, then 57; the previous version used 28 and 12. A tracking camera preserves a readable composition. Gait phase derives from root distance, keeping stance feet planted. Paired walkers pass in the opposite direction, with sticks and a dog; children cross the sand and stop to inspect it.
- The ending establishes Helen holding down the wind-lifted corner, cuts to the paper, rotates the whole sheet through an edge-on pose and holds its blank reverse. The turn completes 15.21 seconds into the shot. The final sentence begins at 19.41 seconds, after the blank reveal. The reverse has only its physical fold, with no map, words or symbolic marks.

## Evidence

Chrome scanned all 3,799 picture frames: maximum limb-length error 4.27×10⁻¹⁴ local units, zero backwards arm flexion in the shared profile rig, zero clamped arm targets, zero caption overflow (at most three lines). Captured real-time playback advanced normally through library, memory, walk and map-turn segments with AudioContext running and no runtime exceptions. The final line is structurally scheduled after the reverse is revealed.

A separate shadow_reader agent inspected sixteen overview stills, action sequences, and six frames captured about 0.4 seconds apart during actual playback for each of the library, memory, path and end passages. It judged the elastic stretch/break and real map turn readable, the resting elbows improved, and the blank reverse held before the reaction. It requested that the final memory invitation be removed and the calendar stop cycling at that moment; those repairs were applied. Final review confirmed lowered arms and Monday 24 at memory offsets 39, 45 and 48 seconds, with no further invitation. The final sleeve capture shows both forearms continuing out of frame. The critic’s final verdict was **pass for the inspected revision sequences**. Continuous full-film motion quality and audible sound remain unreviewed perceptually. Numerical checks are not a substitute for that judgment.

Working captures and recoverable project: `/tmp/reiniger-r3/`. The HTML still contains the original layered paths, profiles, analytic hinges, authored poses, procedural audio and canonical exposure sheet. `window.shadowFilm.actors()` exposes arm and foot evidence alongside the earlier inspection API.

---

## Earlier production record (revision 2)

# The Sunday Bus · Shadow Theatre

Revision: reiniger-r2, 2026-10-31. Full story, 296.517 seconds, fourteen scenes at 12 fps. The user replaced the prompt’s gate proof with The Sunday Bus. No gate scene was made.

## Creative thesis

A remembered invitation becomes a walk made too late. The open space at the chapel and the hand stopping a map corner carry the emotional action; a reunion or a sentimental resolution would weaken it.

Protected conditions: connected fixed-length limbs; no texture inside silhouettes; stable feet during holds and stance phases; readable profiles and hands; full source text in English captions. The artistic achievement is the felt absence when Martin disappears, judged from viewing rather than a proxy score.

## Editable project and source

`index.html` is the self-contained layered project and player, requiring no libraries, API, build, network requests or separate audio. Original paths and layer functions, PARTS profiles, joint geometry, pose parameters, procedural sound and exposure sheet remain inline. `window.shadowFilm` exposes revision, shots, geometry, deterministic frame rendering and per-frame hinge evidence. Coordinates: 1280×720, top-left origin, positive y down; stage ends at y594, caption band below it; actor-local coordinates have feet at y0. Time is seconds, picture quantized to 12 fps. `?t=SECONDS` gives a reproducible still.

Every rendered limb uses shared shoulder/elbow/wrist or hip/knee/ankle endpoints with an analytic two-link solver. Pose/view state is a typed JSDoc Pose plus scene-local staging. The film is an acting sequence that plays once, holds, and can be replayed. Browser controls provide pause, seek, keyboard operation and mute.

`story.txt` is the user-directed English text extracted from `../the-sunday-bus/prompt.txt`. Every story paragraph is retained verbatim in the inline RAW shot data. This is authorization to make the requested adaptation, not a claim of copyright ownership or a new license for the text. All figure paths, scenery and sound are original procedural work for this version; no archival imagery, old film artwork, recorded narration, fonts or music were imported.

Technical reading inspected: Lotte Reiniger’s own account, “Scissors make films”, BFI / Sight and Sound, https://www.bfi.org.uk/sight-and-sound/features/scissors-make-films-lotte-reiniger-creating-her-magical-animations/ . Her separate hinged shapes and transparent background layers inform the representation. No reference film was watched, and no comparison with its normal-speed acting is claimed.

## Independent critique log

A real separate shadow_reader agent inspected all fourteen first-assembly stills, then the repaired end, chapel and bus image sequences. It received the desired experience and output, not a builder assessment.

First verdict: **reference stronger** (stills). At approximately 283.5s, the reaching arm began in space. Stationary knees formed a diamond, the bus obscured the waiting figure, and children looked like small adult duplicates. Repair condition: a continuous fixed-length shoulder–elbow–hand chain before/during/after corner contact; steady feet; visible contact.

Repairs: replaced the extra end arm with the puppet’s own attached chain and a shared paper/contact layout; straightened resting legs; restaged waiting and boarding; gave children separate proportions and bending poses. The title gained a ground ledge.

Final verdict: **pass for the reviewed still sequences; full playback and sound remain inconclusive**. End frames 272.52, 274.52, 276.02, 277.02, 278.02, 282.52 and 296.47 seconds show connected arm, lifted corner, lowered palm, held contact and stable feet. Chapel frames 207.14, 214.14, 221.14, 228.14 and 232.14 seconds show empty space → faint companion → empty space. Bus frames 149.55, 151.75, 153.05 and 154.05 seconds establish waiting, approach and boarding. Strengths to preserve: uncluttered ending, readable caption band, warm monochrome layers and the remembered figure’s disappearance. Remaining artistic limit: schematic gestures. The title ledge contrast was increased after this review.

## Verification and limits

Headless Chrome rendered all **3,559** scheduled frames. The greatest measured limb-length error was **4.27×10⁻¹⁴** actor-local units; no failures. All captions fit in at most three lines. An initial walking-pose overextension was found and repaired before this result. Grounded stance follows root distance/stride phase; resting map-scene feet are constant.

Actual requestAnimationFrame playback advanced after a gesture; pause held time; replay restarted at zero; mute changed state; AudioContext ran and generated nonzero waveform evidence (RMS 0.00240 over 2,048 samples). This establishes execution and signal, not a listening judgment. Mobile player framing was captured at 390×220. The independent critic inspected stills and sampled sequences, not continuous normal-speed movement or audible sound. Full perceptual acceptance of rhythm and sound remains unclaimed.

A recoverable revision and working review captures are in `/tmp/reiniger-review/` on the production machine. No publishing or git commit was performed.

## Method library

- Hinged profile + analytic two-link limbs → quiet human acting → ending → excessive reach changes segment lengths → adjust root/hand placement before adding parts. Rejected: unattached overlay arm.
- Separate pale memory layer → uncertain recall → chapel → a persistent figure reads as a companion → fade back to empty space. Preserve the empty hold.
- Root-distance gait phase → planted stance → coastal path → hip too high overextends a swinging leg → lower walking hip, then scan every frame. Rejected: hiding joints with blur.
