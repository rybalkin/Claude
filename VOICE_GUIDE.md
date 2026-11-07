# How to recreate the "calm lecturer" audio-guide voice

This is the recipe behind the Siena audio guide (`siena.html`, audio in `audio/siena-v3/`).
Hand this file to any assistant (Claude, Gemini, …) or follow it yourself. It contains
everything needed: the exact ElevenLabs settings, how to write scripts in this style,
copy-paste examples, a working script (`tools/tts_lecture.py`), and the mistakes to avoid.

---

## 1. The recipe at a glance

| Setting | Value | Why |
|---|---|---|
| Service | ElevenLabs Text to Speech API | `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` |
| Voice | **Jessica**, `voice_id = cgSgspJ2msm6clMCkdW9` | General American, rated most neutral (9/10) and warm for non-native listeners |
| Model | **`eleven_v4`** | Best quality; follows audio tags such as `[pauses]` |
| Voice settings | `stability: 0.45`, `similarity_boost: 0.75` | Calm and steady but still expressive. v4 has **no** style or speed setting (ignored if sent) |
| Output format | **`mp3_44100_192`** | Highest quality on the Creator plan (`pcm_44100` needs Pro) |
| Post-processing | **None.** Use the file exactly as delivered | Every edit we tried (stretching, inserted silence, re-encoding) added audible artifacts |
| Pauses | `[pauses]` and `[long pause]` tags written in the text | The only reliable way to get long pauses in v4 (see §4) |
| Emphasis | CAPITALS on one word, usually at the **start** of a phrase | v4 stresses capitalised words |
| Language | Optional `language_code` (`"en"`, `"de"`, `"ru"`…) | The same voice speaks German and Russian naturally |
| Text per request | ≤ about 2,300 characters (≈ 2–2.5 min of audio) | Longer requests sometimes time out |
| Cost | ≈ 1 credit per character | A 2-minute stop ≈ 1,600 credits |

Required API key permission: **Text to Speech**. (Optional: *Voices → Read* to list voices,
*User → Read* to check remaining credits.)

---

## 2. The speaking style (what makes it sound like a good lecturer)

The style was modelled on a Russian history lecture, measured with speech analysis:

- **Calm, warm, thoughtful.** Never cheerful or "salesy". No exclamation marks in greetings.
- **Short phrases of 4–7 words**, each followed by a pause.
- **Longer pauses** after a list, before a key point, and after a punchline ("let it sink in").
- **Stress = a quick, higher, louder word at the START of a phrase**, not a stretched word
  at the end: *ACTUALLY, REALLY, ESPECIALLY, PRECISELY, NOT…*
- **Piled-up adjectives**: "Dazzling, brilliant, utterly astonishing Florence."
- **Asides and self-corrections**: "of course…", "let's say…", "by the way…".
- **A historian's gentle irony**: "Is it true? ACTUALLY, no. But the Sienese love it, and so do I."
- **Rhetorical question, pause, answer**: "What IS Siena? [long pause] A museum? … ACTUALLY… neither."
- **Talking to the listener**: "dear friends", "the two of you", "look up", "can you find…?"
- **Interactive challenges** (the part people liked most): "Can you find the iron rings?",
  "Count the she-wolves today. The winner chooses dessert."

### Rules for writing a script
1. Open calmly, with a tag and no exclamation: `[calm] Hello, dear friends.`
2. After almost every short phrase put `[pauses]`; after a key sentence put `[long pause]`.
   About one tag every 6–10 words is right.
3. Put ONE capitalised word at the start of an important phrase. Don't capitalise several words in a row.
4. Spell numbers as words: "in thirteen forty-eight", "about four hundred steps".
5. Use at most one or two mood tags per stop: `[calm]`, `[thoughtful]`. Avoid `[excited]`, `[warmly]`
   and exclamation marks, which make it sound like an advert.
6. For walking tours, end each stop with spoken directions to the next one
   ("Now take Via di Salicotto… after about ninety metres, turn right.").
7. Add one "find it" challenge per stop: something small and real that people can look for.
8. Say clearly when something is a legend ("The legend says…", "Is it true? Probably not.").
9. Target 220–300 words per stop (1½–2½ minutes).

---

## 3. Examples (copy and adapt)

### Example A: opening of an introduction
```text
[calm] Hello, dear friends. Today we're going to talk about Siena... and I want to begin with a question. [long pause] What IS Siena? [long pause] A museum? [pauses] A pretty little provincial town on a hill, with a famous horse race? [long pause] ACTUALLY... neither. [long pause] Siena is a city that once wanted to be the greatest city in Europe. [long pause] And in a strange way, it lost everything. [pauses] And it is precisely BECAUSE it lost, [pauses] that it is so beautiful today. [long pause] Let's try to understand how that happened.
```

### Example B: a walking-tour stop with a challenge and directions
```text
[calm] The Logge del Papa. [pauses] The Pope's Loggia. [long pause] Look how different it is from everything around it. [pauses] Light, elegant, with round arches and slender columns. Pure Renaissance, in a Gothic city. [long pause] It was built in the fourteen-sixties for a pope: Pius the Second. [pauses] Before he became pope, he was a diplomat, a traveller, a poet, and... let's say, not a saint. He even wrote a rather daring love story, which became a bestseller in its time. [long pause] And now, find a coat of arms. [pauses] A white shield with a blue cross, [pauses] and on the cross, five golden crescent moons. [long pause] That is the Piccolomini family. Once you know it, you will see it everywhere. [long pause] Now walk back towards the Campo along Via del Porrione, and climb the narrow passage Chiasso del Bargello up to Via di Città. [pauses] Turn left, and look for a long, curved palace with a tower.
```

### Example C: a short "Find it" challenge (≈ 45 seconds)
```text
[calm] A little challenge for you two. [pauses] As you walk, look at the walls of the old palaces, at about the height of your shoulders. [long pause] Can you find an iron ring? [pauses] Sometimes there is a whole row of them. [long pause] They were for tying horses. [pauses] Imagine a merchant arriving from Rome, tying his horse right here, and walking into the bank. [long pause] Now look higher up. [pauses] Do you see iron brackets? [pauses] They held torches at night, and flags on feast days. [long pause] How many rings can you count before the next corner?
```

### Example D: the same voice in German (works with `language_code: "de"`)
```text
[calm] Guten Tag, liebe Freunde. [pauses] Heute sprechen wir über Siena... [pauses] und ich möchte mit einer Frage beginnen. [long pause] Was IST Siena eigentlich? [long pause] Ein Museum? [pauses] EHRLICH gesagt... [pauses] weder noch. [long pause] Und GERADE weil sie verloren hat, [pauses] ist sie heute so schön.
```

### Example E: the same voice in Russian (works with `language_code: "ru"`)
```text
[calm] Здравствуйте, дорогие друзья. [pauses] Что ТАКОЕ Сиена? [long pause] Музей? [pauses] НА САМОМ ДЕЛЕ, [pauses] ни то, ни другое. [long pause] И именно ПОТОМУ, что потерял, [pauses] он так прекрасен сегодня.
```

---

## 4. Pauses: what works and what doesn't (tested and measured)

ElevenLabs documentation (Eleven v4): *"Eleven v4 and Eleven v3 do not support SSML break tags.
Use audio tags, punctuation (ellipses), and text structure to control pauses and pacing."*

Same Russian text, raw v4 output, measured pauses:

| Markup | Length | Pauses > 0.7 s | Average pause | Longest |
|---|---|---|---|---|
| None | 58 s | 0 | 0.42 s | 0.6 s |
| Ellipses `...` + line breaks | 59 s | 0 | 0.43 s | 0.6 s |
| **`[pauses]` / `[long pause]` tags** | **68 s** | **11** | **0.75 s** | **1.4 s** |
| Tags + ellipses | 67 s | 11 | 0.71 s | 1.2 s |

- ✅ Use `[pauses]` (short) and `[long pause]` (long). The model performs them and does not read them aloud.
- ❌ `<break time="1.5s"/>` is **not supported** by v4 or v3 (only Multilingual v2 / Flash).
- ❌ Ellipses alone barely change anything in v4.
- ❌ The `speed` setting is ignored by v4. Control pace through the writing (short phrases + tags).

---

## 5. Working code

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
  -o stop.mp3
```
Add `"language_code": "de"` (or `"ru"`, `"it"`, …) for other languages.

### Python (batch, with retries)
See **`tools/tts_lecture.py`** in this repository. Usage:
```bash
export ELEVENLABS_API_KEY=...        # never commit the key
python3 tools/tts_lecture.py scripts.json out_dir/
```
where `scripts.json` maps file names to texts: `{"01-intro": "[calm] Hello, dear friends...", "02-campo": "..."}`.
The tool runs 3 requests at a time (the Creator plan allows 5), retries failures, and stops if credits run out.

---

## 6. Quality checks we used
- **Transcribe each file** (e.g. OpenAI `gpt-4o-transcribe`) and make sure no tag words
  ("pause", "calm", "thoughtful") were spoken. Beware of false alarms when the script itself
  contains those words ("calm and serene").
- Compare the transcript with the script: 95–100% word match is normal; differences are mostly
  numbers written as digits and foreign names.
- Listen to the first file before generating the rest.

---

## 7. Mistakes to avoid (all of these happened)
- **Post-processing pauses** by inserting digital silence: the faint background switches off and on
  (audible "gating"). Looping room tone plus a Rubber Band time-stretch sounded even worse.
  → Keep the raw file.
- **Re-encoding MP3** (decode → edit → encode again) loses quality. → Use the delivered file.
- **Cheerful openings** ("Good afternoon, dear friends!" with `[warmly]`) sound like an advert.
  → `[calm]`, full stop, no exclamation.
- **British-sounding voices** (e.g. "Lily") were too accented for the listeners. → Jessica.
- **Stretching words for emphasis** sounds unnatural. → A capitalised word at the start of the phrase.
- **Too many parallel requests**: more than 5 at once gives `concurrent_limit_exceeded`. → 3 at a time.
- **Very long requests** sometimes fail with "upstream request failed". → Keep each request ≤ ~2,300 characters.

---

## 8. Prompt you can give another AI to write new scripts

> Write an audio-guide script for ElevenLabs v4 (voice Jessica) in the style described in
> VOICE_GUIDE.md: a calm, warm, slightly ironic history lecturer talking to two people
> ("dear friends", "the two of you"). Use short phrases of 4–7 words; put `[pauses]` after
> most phrases and `[long pause]` after key sentences; capitalise ONE stressed word at the
> start of an important phrase (ACTUALLY, REALLY, NOT…); spell numbers as words; open with
> `[calm]` and no exclamation marks; include one "can you find…?" challenge with a real,
> visible detail; mark legends as legends; end with directions to the next stop.
> 220–300 words per stop. Topic: …
