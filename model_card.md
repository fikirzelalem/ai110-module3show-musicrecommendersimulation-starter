# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SoundMatch 1.0**

---

## 2. Intended Use  

VibeFinder suggests songs based on what genre, mood, and energy level you're in the mood for. It's not a real app, it's more of a classroom project to show how content-based recommendation works. You tell it what you want, it scores every song in the catalog, and gives you the top 5. It's not meant to replace Spotify or anything like that, just to show the logic behind how those systems think.

---

## 3. How the Model Works  

Imagine you're a friend helping someone pick a song. You'd probably ask what genre they're into, what kind of mood they're in, and whether they want something chill or high energy. That's basically what this system does, except it turns those answers into numbers.

Every song in the catalog gets a score. If the genre matches, it gets 2 points. If the mood matches, 1 more point. Then it checks how close the song's energy is to what you said you wanted and gives up to 1 point for that. If you said you like acoustic music and the song is acoustic, there's a small bonus too. Once all the songs are scored, they get sorted and the top 5 come back with a note explaining why each one ranked where it did.

---

## 4. Data  

There are 18 songs in the catalog. Each one has a genre, mood, energy level, tempo, and a few other audio features like acousticness and danceability. The genres cover a decent range including pop, lofi, rock, r&b, electronic, hip-hop, jazz, metal, country, folk, ambient, indie pop, and synthwave. Moods include happy, chill, intense, relaxed, moody, and focused.

The problem is most genres only show up once or twice. Lofi is the most represented with three songs. A few moods like "focused" only appear in one song total. I added more songs to the original starter dataset but 18 is still pretty thin. If your taste falls in an underrepresented genre, the results get weak fast.

---

## 5. Strengths  

It works really well when your preferences line up with what's in the catalog. The Chill Lofi and Moody Electronic profiles both gave results that felt genuinely accurate. Neon Jungle hit a perfect score for the electronic profile because genre, mood, and energy all matched at the same time. That felt satisfying.

The other thing I actually liked is that you can see exactly why each song was picked. It tells you which features matched and how many points each one added. Most real apps don't show you that, so it's nice to have the transparency even if the catalog is tiny.

---

## 6. Limitations and Bias 

The biggest issue I found is that genre carries too much weight. At +2.0 points it basically controls the whole ranking, so even if a song has the wrong energy or mood, it'll still end up near the top just for being in the right genre. I ran into this with the edge case profile. The system kept recommending "Slow Burn" to a user who wanted high energy just because it was r&b. That felt wrong.

Most genres in the dataset only have one song, which makes things awkward. If you're a rock fan, your first result is fine, but after that the system just grabs whatever has similar energy from totally different genres. At that point it's not really recommending music, it's just filling slots.

The genre matching is also exact. "indie pop" and "pop" are treated as completely different things. So a pop fan won't get matched to "Rooftop Lights" even though it would probably fit their taste. There's no fuzzy matching or genre similarity built in.

One more thing: there's only one song tagged as "focused" in the whole catalog. If someone just wants music to study to, they're almost guaranteed to get bad mood matches across the board. Some user types just aren't supported by this dataset at all.

---

## 7. Evaluation  

I tested five different user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Moody Electronic, and an edge case I called "High Energy but Relaxed." For each one I ran the full recommender and looked at whether the top 5 results actually made sense for that type of listener.

Most of them felt right. The Chill Lofi profile got lofi songs with acoustic vibes at the top, and the Moody Electronic profile landed on Neon Jungle as a perfect match. Genre, mood, and energy all lined up. Those felt like wins.

The one that surprised me most was the edge case. I set up a profile that wanted r&b but also wanted high energy (0.9), which is kind of contradictory since most r&b in the catalog is pretty mellow. The system still picked r&b songs at the top because the genre weight is so strong. "Slow Burn" scored 3.58 even though its energy is only 0.48, way off from what the user asked for. A person using a real app would probably be confused by that result.

I also ran a weight shift experiment where I cut the genre weight in half and doubled the energy weight. That changed a few rankings, especially for the edge case and the Moody Electronic profile, but most results stayed the same. That told me the system is mostly working as designed, just a little too locked in on genre.

I also wrote pytest tests for `score_song` and `recommend_songs` to make sure the math was correct before trusting the output.

---

## 8. Future Work  

The first thing I'd fix is the genre matching. Right now it's all or nothing, so "indie pop" and "pop" score completely differently even though they're close. I'd want it to give partial credit for similar genres instead of treating every mismatch the same way.

I'd also add more songs. 18 is just not enough. Most genres have one song so the recommendations fall apart quickly once the top match is taken. More data would fix a lot of the problems on its own.

The last thing I'd want is some kind of listening history. Right now if you run the same profile twice you get the exact same list. A real system would track what you've already heard and stop recommending it so you actually get variety.

---

## 9. Personal Reflection  

I went into this thinking a recommender system would be more complicated than it actually is. It's really just scoring and sorting. Once I saw that, it made me look at apps like Spotify differently. All that "we think you'll like this" stuff is just math under the hood, the hard part is choosing the right features and weights.

What got me was how fast bias crept in without me trying. I never planned to make a system that fails for high-energy r&b listeners, but that's exactly what happened because I gave genre too many points. Nobody told me to do that, it just seemed like the right call at the time. I think about that when I use recommendation apps now. The weirdness in their suggestions probably isn't random, it's the result of choices someone made early on that nobody went back to question.
