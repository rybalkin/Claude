# The "calm lecturer" voice: how to recreate it for any app

A warm, calm, thoughtful narrator, slow and spacious, with clear stresses and natural long pauses,
generated with ElevenLabs. Use it for audio guides, podcasts, explainers, lessons, app narration,
meditations on history: anything where one person talks to the listener.

Hand this file to any assistant (Claude, Gemini, …) or follow it yourself. Walking-tour specifics
(stops, directions, GPS) are in [`AUDIO_GUIDE.md`](AUDIO_GUIDE.md).

---

## 1. Settings

| Setting | Value | Why |
|---|---|---|
| Service | ElevenLabs Text to Speech API | `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` |
| Voice | **Jessica**, `voice_id = cgSgspJ2msm6clMCkdW9` | General American; rated the most neutral (9/10) and warm for non-native listeners |
| Model | **`eleven_v4`** | Best quality; follows audio tags such as `[pauses]` |
| Voice settings | `stability: 0.45`, `similarity_boost: 0.75` | Calm and steady, still expressive. v4 has **no** style or speed setting (ignored if sent) |
| Output format | **`mp3_44100_192`** | Highest quality on the Creator plan (`pcm_44100` needs Pro) |
| Post-processing | **None.** Use the file exactly as delivered | Every edit we tried added audible artifacts (see §7) |
| Text per request | ≤ about 2,300 characters (≈ 2–2.5 min of audio) | Longer requests sometimes fail with "upstream request failed" |
| Parallel requests | 3 at a time | The Creator plan allows 5; more gives `concurrent_limit_exceeded` |
| Cost | ≈ 1 credit per character | 1 minute of speech ≈ 750–900 characters ≈ 750–900 credits |

Required API key permission: **Text to Speech**. Optional: *Voices → Read* (list voices),
*User → Read* (check remaining credits).

Tested alternatives, for reference: Aria (warm, calm, female), Roger (warm, male, can sound flat
when calm), Eric (bright, dynamic, male), Matilda (calm, female), Lily (British; too accented for our
listeners). All are classic ElevenLabs voices.

---

## 2. Pace

- **Measured target:** about 110–125 words per minute, which is slower than typical narration (~150).
- v4 ignores the `speed` setting, so **pace comes from the writing**:
  - short phrases of **4–7 words**;
  - a pause tag after most phrases (see §3);
  - one idea per sentence; no long subordinate clauses.
- Spell numbers as words ("in thirteen forty-eight", "about four hundred") so they are read calmly.

## 3. Pauses

ElevenLabs documentation (Eleven v4): *"Eleven v4 and Eleven v3 do not support SSML break tags.
Use audio tags, punctuation (ellipses), and text structure to control pauses and pacing."*

Same text, raw v4 output, measured:

| Markup | Length | Pauses > 0.7 s | Average pause | Longest |
|---|---|---|---|---|
| None | 58 s | 0 | 0.42 s | 0.6 s |
| Ellipses `...` + line breaks | 59 s | 0 | 0.43 s | 0.6 s |
| **`[pauses]` / `[long pause]` tags** | **68 s** | **11** | **0.75 s** | **1.4 s** |
| Tags + ellipses | 67 s | 11 | 0.71 s | 1.2 s |

- ✅ `[pauses]` after a short phrase (~0.5 s); `[long pause]` after a key sentence, a list, a question, or a punchline (~1–1.4 s).
- ✅ About one tag every 6–10 words. The model performs them silently and does not read them aloud.
- ❌ `<break time="1.5s"/>`: **not supported** in v4/v3 (only Multilingual v2 / Flash models).
- ❌ Ellipses alone barely change anything in v4. They are fine for a hesitant tone, not for length.
- ❌ Inserting silence afterwards (editing): causes artifacts, see §7.

## 4. Emphasis

Measured on the reference lecturer: a stressed word is **~8 semitones higher and ~10 dB louder,
but short and crisp, not stretched**, and it usually comes **at the START of a phrase**.

- ✅ CAPITALISE **one** word to stress it, placed early in the phrase:
  *"ACTUALLY, that's an exaggeration."*, *"It was REALLY rich."*, *"NOT handsome at all."*
- ✅ Typical stressed words: intensifiers and turn words (ACTUALLY, REALLY, ESPECIALLY, PRECISELY,
  NOT, BECAUSE), evaluative adjectives (STUNNING), and the key noun of the sentence.
- ✅ Rarely, a syllable-by-syllable word for a punchline: "that's an ex-ag-ge-ra-tion".
- ❌ Several capitalised words in a row: shouty.
- ❌ Stretching words or slowing them down for emphasis: sounds unnatural.

## 5. Tone and rhetoric

- **Calm, warm, thoughtful, gently ironic.** Never cheerful or "salesy".
- Start with `[calm]`. Use at most one or two mood tags per file: `[calm]`, `[thoughtful]`.
  Avoid `[warmly]`, `[excited]`, `[amused]` and exclamation marks: they made it sound like an advert.
- Rhetorical habits that make it sound like a good lecturer:
  - **question → pause → answer**: "What IS Siena? [long pause] A museum? … ACTUALLY… neither."
  - **piled-up adjectives**: "Dazzling, brilliant, utterly astonishing Florence."
  - **asides and self-corrections**: "of course…", "let's say…", "by the way…"
  - **historian's caution with light irony**: "Is it true? ACTUALLY, no. But they love it, and so do I."
  - **talking to the listener**: "dear friends", "imagine…", "look…", "tell each other…"
  - **letting a key line sink in**: the punchline, then `[long pause]`.

## 6. Background sound

- **Default: no background.** The voice alone, raw from ElevenLabs, sounded best and cleanest.
- If an app really needs ambience or music, keep the voice file untouched and do **one** final mix:
  - background about 11–15 dB quieter than the voice (we used a bed at −27 LUFS under a voice at −16 LUFS);
  - duck the background under speech (sidechain compression), with fades in and out;
  - encode **once**, at 160–192 kbps or higher. Never decode/re-encode the voice several times.
- ElevenLabs Sound Effects (`/v1/sound-generation`) can make ambience beds (e.g. "quiet stone courtyard,
  soft footsteps, distant bell"); music generation needs the *Music* permission on the key.

## 7. Mistakes to avoid (all of these happened)

- **Lengthening pauses by inserting digital silence**: the faint background switches off and on (audible "gating").
- **Time-stretching** to slow the voice (ffmpeg `atempo`, or Rubber Band with looped room tone): warbly, judged "terrible".
- **Re-encoding MP3** (decode → edit → encode again): loses quality.
- **Cheerful openings** ("Good afternoon, dear friends!" with `[warmly]`): sounds like an advert.
- **British-sounding voice** (Lily) for an international audience: too accented.
- **Too many parallel requests** (> 5): `concurrent_limit_exceeded`. **Very long requests**: occasional failures.

## 8. Other languages

The same voice and settings work in other languages; add `"language_code"`. Tested:

```text
DE: [calm] Guten Tag, liebe Freunde. [pauses] Heute sprechen wir über Siena... [long pause] Was IST Siena eigentlich? [long pause] EHRLICH gesagt... [pauses] weder noch.
RU: [calm] Здравствуйте, дорогие друзья. [pauses] Что ТАКОЕ Сиена? [long pause] НА САМОМ ДЕЛЕ, [pauses] ни то, ни другое.
```
An audio-model check rated the Russian 9/10 for natural pronunciation; the German transcript matched word for word.

## 9. Examples

### Introduction / explainer
```text
[calm] Hello, dear friends. Today we're going to talk about Siena... and I want to begin with a question. [long pause] What IS Siena? [long pause] A museum? [pauses] A pretty little provincial town on a hill, with a famous horse race? [long pause] ACTUALLY... neither. [long pause] Siena is a city that once wanted to be the greatest city in Europe. [long pause] And in a strange way, it lost everything. [pauses] And it is precisely BECAUSE it lost, [pauses] that it is so beautiful today. [long pause] Let's try to understand how that happened.
```

### Story with irony and a punchline
```text
[calm] Lorenzo was formidably intelligent, [pauses] an accomplished poet, [pauses] a dazzling conversationalist... [long pause] and strikingly unhandsome. [pauses] A flattened nose, [pauses] a harsh voice, [pauses] and, curiously, NO sense of smell at all. [long pause] None of which, [pauses] let's say, [pauses] dimmed his charm.
```

### App or lesson narration (non-travel)
```text
[calm] Before we start, [pauses] take a moment. [long pause] Today's lesson has only one idea. [pauses] Just one. [long pause] And it is REALLY simple: [pauses] small steps, repeated every day, [pauses] beat big plans that never begin. [long pause] Let's see why.
```

## 10. Code

### curl
```bash
curl -sS "https://api.elevenlabs.io/v1/text-to-speech/cgSgspJ2msm6clMCkdW9?output_format=mp3_44100_192" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "[calm] Hello, dear friends. [pauses] Today we are going to talk about Siena... [long pause] What IS Siena?",
    "model_id": "eleven_v4",
    "voice_settings": {"stability": 0.45, "similarity_boost": 0.75}
  }' \
  -o out.mp3
```
Add `"language_code": "de"` (or `"ru"`, `"it"`, …) for other languages. Never commit the API key.

### Batch tool
[`tools/tts_lecture.py`](tools/tts_lecture.py) turns a JSON of texts into MP3s with these exact settings
(3 in parallel, retries, stops when credits run out):
```bash
export ELEVENLABS_API_KEY=...
python3 tools/tts_lecture.py scripts.json out_dir/ [--lang de]
# scripts.json: {"01-intro": "[calm] Hello, dear friends...", "02-chapter": "..."}
```

## 11. Quality checks
- Transcribe each file (e.g. OpenAI `gpt-4o-transcribe`): no tag words ("pause", "calm", "thoughtful")
  should be spoken. Beware false alarms when the script itself contains those words.
- 95–100% word match with the script is normal (differences: numbers as digits, foreign names).
- Listen to the first file before generating many.

## 12. Prompt for another AI (any app)

> Write a narration script for ElevenLabs v4 (voice Jessica) in the style of VOICE_STYLE.md:
> a calm, warm, slightly ironic lecturer speaking directly to the listener. Short phrases of
> 4–7 words; `[pauses]` after most phrases and `[long pause]` after key sentences, questions and
> punchlines (about one tag every 6–10 words); capitalise ONE stressed word near the start of an
> important phrase (ACTUALLY, REALLY, NOT…); spell numbers as words; open with `[calm]` and no
> exclamation marks; use question → pause → answer, asides ("of course…", "let's say…"), and
> mark legends as legends. Keep each file under 2,300 characters. Topic: …
