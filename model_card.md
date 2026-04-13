# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch is designed for classroom exploration, and it is not a production app. It suggests songs from a small catalog based on a user's stated genre preference, mood, energy target, and acoustic texture preference. It assumes the user can describe what they want in advance and that those four fields are enough to find a good match. It is meant to demonstrate how a simple scoring system turns user preferences into ranked recommendations, and to expose where that approach succeeds and where it breaks down.

It should not be used to make real music recommendations for real users, as the catalog is too small, the user profile is too limited, and the scoring logic has known biases that would produce unfair or misleading results at scale.

---

## 3. How the Model Works

Each song in the catalog gets a score based on how closely it matches what the user said they want. The score is built from five ingredients added together.

First, if the song's genre matches the user's preferred genre, it earns bonus points. Same for mood. These are all-or-nothing, meaning either it matches exactly or it gets nothing. Then the system looks at energy. Instead of requiring an exact match, it rewards songs that are close to the user's target energy. A song that's slightly off gets nearly full points; a song that's way off gets almost none. The formula squares the gap so that small differences barely matter but large ones really hurt. Finally, two small bonuses: one for acoustic texture (the system rewards songs that feel more organic or more electronic depending on what the user prefers), and one that gives a tiny edge to songs that sound more upbeat, used only as a tiebreaker. The song with the highest total score ranks first. The top five are returned.

---

## 4. Data

The catalog has 18 songs in a CSV file. The original dataset had 10 songs; 8 more were added to improve variety. Songs span 15 genres including lofi, pop, rock, jazz, classical, hip-hop, metal, folk, reggae, edm, and more. Moods include happy, chill, intense, focused, melancholic, peaceful, romantic, angry, and others.

Each song stores five numeric features; energy, tempo, valence, danceability, and acousticness; all on a 0 to 1 scale except tempo. Despite the additions, the catalog is still very small. Most genres have only one song, which means the data doesn't represent the full range of musical taste. Listeners who prefer genres outside the main cluster (lofi, pop) will get much weaker recommendations.

---

## 5. Strengths

The system works well for users whose preferences align with the core of the catalog. A lofi listener asking for chill, low-energy, acoustic music gets a well-differentiated top-5 with a clear winner and meaningful gaps between the rankings. A pop listener asking for happy, high-energy songs also gets a clean result with sensible ordering.

The scoring is fully transparent. Every recommendation comes with a breakdown of exactly which sub-scores fired, genre match, mood match, energy proximity, acoustic fit, and valence, so there's no mystery about why a song ranked where it did. That explainability is the biggest strength of this approach compared to a learned model that can't tell you why it recommended something.

---

## 6. Limitations and Bias

The most significant weakness discovered during testing is that the catalog is too small and unevenly distributed to treat all users fairly. With 18 songs spread across 15 genres, most genres have exactly one song, meaning a genre match is a lottery that only a handful of users can win, and everyone else is ranked almost entirely on numeric features like energy and acousticness. This creates a structural advantage for lofi listeners, who have three songs in the catalog, compared to a metal or reggae fan who has only one. In practice, a lofi user received a rich, differentiated top-5 list with scores spread across a wide range, while a metal fan's recommendations was a narrower spread, where the ordering felt arbitrary. This is not a flaw in the scoring logic itself, but is a data representation problem, as it produces unfair outcomes just the same, and a real system would need a much larger and more balanced catalog before the scoring weights could be trusted to work equally well for all listener types.

Two additional biases worth naming: the valence tiebreaker silently favors brighter-sounding songs regardless of what the user asked for, which means melancholic profiles are quietly nudged toward cheerful ones. And the system never warns the user when their genre request couldn't be matched, but instead returns a confident-looking list even when the genre was completely ignored.

---

## 7. Evaluation

Six user profiles were tested: three standard profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial ones designed to expose edge cases (a conflicting profile pairing high energy with a melancholic mood, a ghost genre profile using "bossa nova" which doesn't exist in the catalog, and an extreme profile targeting near-zero energy with electronic texture preference). For each profile, the top 5 results were examined and compared against what felt musically intuitive.

The standard profiles all behaved as expected, where the correct song topped each list and the rankings felt reasonable. The most surprising result came from the conflicting profile, as even though the user wanted high energy (0.90) and the only matching song had energy of only 0.62, it still ranked first by a wide margin because the genre and mood matched simultaneously. This revealed that two binary matches together (+2.5 points) can outweigh a significant numeric mismatch, which feels wrong, as a song that misses the energy target by nearly 0.3 should not be the top pick for someone who prioritized energy.

The ghost genre profile was also instructive. When "bossa nova" produced no genre matches at all, the system silently fell back to mood and numeric scoring and still returned a confident-looking top-5 list. Coffee Shop Stories (jazz) rose to first place, which was actually a reasonable substitution — but nothing in the output told the user that their genre preference was completely ignored. A real system would surface that gap rather than hide it.

---

## 8. Future Work

Replace the likes_acoustic boolean with a continuous target_acousticness float so that users can express a specific texture preference rather than a binary choice. This would close the biggest gap between how energy and acousticness are handled, as energy already works this way, and so acousticness should too.

Add a fallback warning when no songs match the user's genre. Something like printing "No songs found for genre X: showing closest matches" would make the system more honest without changing the scoring logic.

Expand the catalog, as most of the current biases trace back to having only one song per genre. A minimum of five songs per genre would give the scoring weights a fair chance to work as intended across different listener types.

---

## 9. Personal Reflection

The biggest learning moment came from the adversarial profiles, as the scoring logic felt solid on paper, but running the conflicting profile showed that two categorical matches together can completely override a numeric mismatch, making the system more confident than it should be. AI tools helped with drafting the formula, thinking through weights, and generating test profiles, but every suggested weight still needed to be verified by actually running the output and checking whether it felt right. The most surprising thing was how quickly 40 lines of arithmetic started to feel like a real recommender, as the gap between "a ranked list" and "a system with taste" is smaller than expected, which is both impressive and worth being skeptical of. Next steps would be replacing the boolean likes_acoustic with a continuous value, adding a warning when a genre has no catalog matches, and eventually incorporating listening history so the system can learn from behavior rather than relying entirely on what the user said upfront.

---
