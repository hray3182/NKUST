# Homework

## Q1: Find a dataset you want to use to find associations

After watching the video, my first thought was we can apply to a song recommendation system.

I found a [spotify_million](https://www.kaggle.com/datasets/himanshuwagh/spotify-million), which contains 1 million playlists created by users on Spotify.

## Q2: Describe how to generate transaction dataset

Each playlist represents a transaction, and the songs in the playlist are the items in the transaction. We can apply Apriori algorithm to calculate the frequent itemsets and generate association rules.

## Q3: Give an example to show the importance of the discovered rules

We can recommend songs based on the discovered association rules. For example, if a user likes song A and song B, we can recommend song C to them if we find a rule that says "If a user likes song A and song B, they are likely to like song C".
