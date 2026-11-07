# Zürich → Firenze by train

An animated, single-file website (`index.html`) showing a rail journey from Zürich to Florence: EuroCity through the Gotthard and Ceneri base tunnels to Milano Centrale, then Frecciarossa via Bologna to Firenze S. M. Novella.

Open `index.html` in a browser. Press Play (or Space), drag the slider or the train on the map, click a stop in the timetable, or change the departure time.

Times and the map are approximate and for illustration only.

# Florence on Foot

`florence.html` is a walking map of Florence for a first visit. It has three half-day walks (the Renaissance core, Oltrarno to sunset, and markets, Michelangelo & Santa Croce) and 19 stops. Each stop explains why it's worth seeing and adds a tip for couples. With GPS on, the map shows a live "you are here" dot and the walking time to every stop, and it can sort stops by nearest. Every stop also has a "Walk here" link for turn-by-turn directions.

GPS only works when the page is served over https, for example with GitHub Pages turned on for this repo.

# Voice guide

`VOICE_GUIDE.md` explains how the Siena audio guide voice was made (ElevenLabs v4, voice "Jessica", calm lecture style, pauses with `[pauses]` / `[long pause]` tags, raw 192 kbps, no post-processing), with examples in English, German and Russian. `tools/tts_lecture.py` generates new files in the same voice from a JSON of scripts.
