# How to make a walking audio guide like "Siena Step by Step"

This covers what is specific to **walking tours**: structure, stops, directions, interactive challenges,
indoor tracks, and the GPS web page. For the voice itself (settings, pace, pauses, emphasis, tone,
background, code), see **[`VOICE_STYLE.md`](VOICE_STYLE.md)**. Every audio file in the guide uses that voice.

Live example: `siena.html` (audio in `audio/siena-v3/` and `audio/siena-v2/`).

---

## 1. Structure of a tour

| Part | Length | Plays |
|---|---|---|
| **Introduction** while walking from the station / car park to the first stop | 10–15 min | at the start point (GPS) |
| **Main stops**, 150–300 m apart (never more than ~4 min walk) | 1½–2½ min each | automatically on arrival (GPS geofence 20–40 m) |
| **🔎 Find-it** extras at the same spot as a main stop | ~45 s each | right after the main stop |
| **Indoor tracks** (cathedral, museum, library) | 1–1½ min each | tap to play (GPS is unreliable indoors) |
| **Final stop**: a view, a sunset, a goodbye | 1½ min | on arrival |

Siena had: a 14-minute intro, 21 main stops, 7 Find-it extras, and 7 indoor tracks (about 75 minutes of audio).

## 2. Writing a main stop (220–300 words)

1. **Arrival line**: name the place calmly. `[calm] Piazza Tolomei. [pauses] And here is the she-wolf…`
2. **What to look at**: "Look up…", "On your left…", "The long building opposite…"
3. **One or two stories**: a date, a person, a surprising detail. Mark legends as legends.
4. **One interactive moment** (see §3).
5. **Spoken directions to the next stop** at the very end, short and concrete:
   *"Now take Via di Salicotto, the street that leaves the Campo beside the town hall. After about ninety metres, turn right."*
6. Refer back and forward ("Remember the she-wolf from Piazza Tolomei?") so the tour feels like one story.
   If you reorder stops, update these references and the directions.

## 3. Interactivity (what listeners liked most)

- **Find it**: something small, real and visible. "Can you find an iron ring at shoulder height?",
  "Find the curved palace", "Find the five golden crescent moons on a blue cross."
- **Count**: "Count the arches as you walk down", "Count the she-wolves today: the winner chooses dessert."
- **Guess**: "How many of her letters survive? Ten? A hundred? [long pause] Almost four hundred."
- **Choose / tell each other**: "Which contrada would you join?", "Which moves you more, Donatello or Bernini?"
- **Act**: "Wave to the tiny people on top of the wall", "Close your eyes and name the spices."
- Only ask people to find things you are sure exist and are visible; hedge positions you are not sure of
  ("somewhere along the edge of the square…").

### Example: main stop
```text
[calm] The Logge del Papa. [pauses] The Pope's Loggia. [long pause] Look how different it is from everything around it. [pauses] Light, elegant, with round arches and slender columns. Pure Renaissance, in a Gothic city. [long pause] It was built in the fourteen-sixties for a pope: Pius the Second. [pauses] Before he became pope, he was a diplomat, a traveller, a poet, and... let's say, not a saint. He even wrote a rather daring love story, which became a bestseller in its time. [long pause] And now, find a coat of arms. [pauses] A white shield with a blue cross, [pauses] and on the cross, five golden crescent moons. [long pause] That is the Piccolomini family. Once you know it, you will see it everywhere. [long pause] Now walk back towards the Campo along Via del Porrione, and climb the narrow passage Chiasso del Bargello up to Via di Città. [pauses] Turn left, and look for a long, curved palace with a tower.
```

### Example: Find-it extra (~45 s)
```text
[calm] A little challenge for you two. [pauses] As you walk, look at the walls of the old palaces, at about the height of your shoulders. [long pause] Can you find an iron ring? [pauses] Sometimes there is a whole row of them. [long pause] They were for tying horses. [pauses] Imagine a merchant arriving from Rome, tying his horse right here, and walking into the bank. [long pause] Now look higher up. [pauses] Do you see iron brackets? [pauses] They held torches at night, and flags on feast days. [long pause] How many rings can you count before the next corner?
```

### Example: indoor track opening
```text
[calm] Welcome inside. [pauses] Stop for a moment, just inside the door, and let your eyes adjust. [long pause] Now look up. [pauses] The vaults are deep blue, with golden stars. [long pause] And now, a challenge. [pauses] Look at the cornice, high up along the nave. [pauses] Do you see faces? [long pause] Can you find the one who looks the most bored?
```

## 4. Places, coordinates and directions (use real map data)

Guessed coordinates were up to 100 m off, so use OpenStreetMap services:
- **Coordinates:** Nominatim, `https://nominatim.openstreetmap.org/search?q=Fonte+Gaia,+Siena&format=json&limit=1`
  (send a User-Agent; at most 1 request per second).
- **Walking routes with street names:** OSRM foot router,
  `https://routing.openstreetmap.de/routed-foot/route/v1/foot/{lon1},{lat1};{lon2},{lat2}?steps=true&overview=full&geometries=geojson`.
  Use `steps` (turn + street name + metres) to write the directions, and the geometry to draw the route line.
- Check the router's choices: inside big squares it walks around the edge (write "walk straight across"),
  and it sometimes prefers odd back lanes or underpasses (add waypoints or end the tour elsewhere).
- Write directions for each stop twice: **spoken** at the end of the previous stop, and **written**
  ("About 190 m, 3 min. Take Via di Salicotto… turn right into Piazza del Mercato.") on the page.

## 5. The web page (GPS player)

What `siena.html` does, and what testers asked for:
- Map (Leaflet + OpenStreetMap tiles) with the route line and numbered pins. **Stops at the same spot share one pin** ("13·14", or "19–25" for a run).
- Live GPS dot with accuracy, a follow-me button, and a heading arrow.
- **Each story starts automatically on arrival** (geofence radius 20–40 m + up to 20 m of GPS accuracy).
  If one is still playing, the next one waits in a queue. Indoor tracks have no geofence.
- A **▶ Start** tap first (browsers only allow sound after a tap); it plays a tiny silent clip to unlock audio.
- **Bottom player with ⏮ ▶ ⏭** (also from the lock screen), and a **"Next: name · distance · minutes"** line
  with a **"Way ▸"** button that opens the turn-by-turn directions and a Google Maps walking link. People should never need to scroll up while walking.
- Each stop card: what to look for, "How to get here", "Walk here ↗", and a Read-along transcript.
- Keep the screen awake (Wake Lock); remember progress per device (localStorage).
- Host on GitHub Pages (needs https for GPS). A public repo is needed on a free GitHub plan.
- Use a **new audio folder** when you re-record files, so phones don't play cached old versions.

## 6. Workflow and budget

1. Pick stops (15–25) close together; geocode them; route them; check the order on a map.
2. Write the introduction and stops (VOICE_STYLE.md rules + §2–3 here). Fact-check dates and names.
3. Generate a single test file and listen.
4. Generate everything **in walking order**, 3 requests in parallel, and publish as files finish.
   People may already be walking.
5. Transcribe every file to check no tags were spoken; spot-check one on the phone.
6. Budget: about **1 credit per character**. Siena: intro ~9,000; 21 stops ~40,000; extras ~4,700; indoor ~8,600.

## 7. Prompt for another AI (audio guide)

> Write a walking audio-guide stop for ElevenLabs v4 (voice Jessica), following VOICE_STYLE.md
> (calm lecturer, short phrases, `[pauses]` / `[long pause]`, one CAPITALISED stress near the start of
> a phrase, numbers as words, `[calm]` opening, no exclamation marks) and AUDIO_GUIDE.md: name the place,
> say what to look at, tell one or two stories (mark legends as legends), include one "can you find…?"
> challenge with a real visible detail, and end with spoken directions to the next stop: [street names,
> turns, metres]. 220–300 words, under 2,300 characters. Place: … Next stop: … Directions: …
