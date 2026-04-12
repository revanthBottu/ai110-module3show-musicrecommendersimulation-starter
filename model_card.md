# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---Recommendo

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---It is used for music recommendation. It assumes that a realistic user may not have only one preference in genre when looking for new songs, so it matches more closely on mood.

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---genre and mood are used to filter, with how closely a song matches mood having more weight than a song's genre. User preferences towards energy, danceability, and valence are considered for ranking. Those features are turned into scores based on similarity with the user profile.

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---The csv has about 10 songs with various genres. It might be beneficial to have more songs to provide a wider range of results for the user.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---This model accurately captures songs with similar mood and genre, and the ranking for minor features helps tune the search more towards what the user likes.

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---The system might not be able to guarantee a song is similar to other songs the user likes. Some songs may have all the same features as the ones in the taste profile, but differ in lyrics or prod value, which can change the song entirely.

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---I looked for good similarity among diverse profiles across differing genres and moods, and a good ranking system where the higher songs matched the other scores well.

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---I would probably add more features towards beat, lyrics, and tone to better tune the model.

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps 

Recommender systems generally do well when presented with more features, which they can weight well against other features to give specific songs closer to what the user wants.
