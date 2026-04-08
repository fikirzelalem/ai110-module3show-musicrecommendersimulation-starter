# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest issue I found is that genre carries too much weight. At +2.0 points it basically controls the whole ranking, so even if a song has the wrong energy or mood, it'll still end up near the top just for being in the right genre. I ran into this with the edge case profile — the system kept recommending "Slow Burn" to a user who wanted high energy, just because it was r&b. That felt wrong.

Most genres in the dataset only have one song, which makes things awkward. If you're a rock fan, your first result is fine, but after that the system just grabs whatever has similar energy from totally different genres. At that point it's not really recommending music, it's just filling slots.

The genre matching is also exact — "indie pop" and "pop" are treated as completely different things. So a pop fan won't get matched to "Rooftop Lights" even though it would probably fit their taste. There's no fuzzy matching or genre similarity built in.

One more thing: there's only one song tagged as "focused" in the whole catalog. If someone just wants music to study to, they're almost guaranteed to get bad mood matches across the board. Some user types just aren't supported by this dataset at all.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
