from typing import List

words_in_tweet = []
i = 0
j = 0

for i in range(len(text)):
    if text[i] == ' ':
        words_in_tweet.append(text[j:i].strip())
        j = i
    elif i == len(text) - 1:
        words_in_tweet.append(text[j:i].strip())
        j = i