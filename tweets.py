"""Assignment 3: Tweet Analysis"""

from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'

# Order of data in the file
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4

# Helper functions.

def alnum_prefix(text: str) -> str:
    """Return the alphanumeric prefix of text, converted to
    lowercase. That is, return all characters in text from the
    beginning until the first non-alphanumeric character or until the
    end of text, if text does not contain any non-alphanumeric
    characters.

    >>> alnum_prefix('')
    ''
    >>> alnum_prefix('IamIamIam')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!andMore')
    'iamiamiam'
    >>> alnum_prefix('$$$money')
    ''

    """

    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[:index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.

    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'

    """

    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text, converted to lowercase, with
    duplicates included.

    >>> extract_mentions('Hi @UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many @cats$extra @meow?!')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @! here?')
    []

    """

    # uses alnum
    
    mentions_lst = []
    
    for word in text.split():
        if word[0] == MENTION_SYMBOL and alnum_prefix(word[1:]) != '':
                mentions_lst.append(alnum_prefix(word[1:]))
    return mentions_lst


def extract_hashtags(text: str) -> List[str]:
    """Return a list containing all hashtags in the text, in the order
    of first occurrence, converted to lowercase with duplicates removed. 
    Hashtags are case insensitive so COMPSCI and compsci are treated as the same
    and only included once
    
    >>> extract_hashtags('Hi #UofT do you like #cats #CATS @meowmeow')
    ['uoft', 'cats']
    >>> extract_hashtags('#cats are @cute #cats #cat meow #meow')
    ['cats', 'cat', 'meow']
    >>> extract_hashtags('#many #cats$extra #meow?!')
    ['many', 'cats', 'meow']
    >>> extract_hashtags('No valid mentions #! here?')
    []
    """
    # uses alnum
    
    hashtags_lst = []
    
    for word in text.split():
        if word[0] == HASH_SYMBOL and alnum_prefix(word[1:]) != '':
            if alnum_prefix(word[1:]) not in hashtags_lst:
                hashtags_lst.append(alnum_prefix(word[1:]))
    return hashtags_lst    

    
def count_words(text: str, words_to_num: Dict[str, int]) -> None:
    """Updates the counts of words in words_to_num. If a word is not in
    words_to_num, then it is added. Hashtags, mentions, URLS and empty strings 
    are not words and non-alphanumberic characters are removed from words before
    being added to dictionary
    
    >>> words_to_num = {}
    >>> count_words("@UTM: We have free icecream! #sunnydays", words_to_num)
    >>> words_to_num
    {'we': 1, 'have': 1, 'free': 1, 'icecream': 1}
    >>> words_to_num = {'tweet': 2}
    >>> count_words("Tweet @UTM or share your opinion at the link: https://feedback.com", words_to_num)
    >>> words_to_num
    {'tweet': 3, 'or': 1, 'share': 1, 'your': 1, 'opinion': 1, 'at': 1, 'the': 1, 'link': 1}
    >>> words_to_num = {}
    >>> count_words("", words_to_num)
    >>> words_to_num
    {}
    """
    # uses clean_word
    
    words_in_tweet = text.split()
    
    for word in words_in_tweet:
        if clean_word(word) in words_to_num:
            words_to_num[clean_word(word)] = words_to_num[clean_word(word)] + 1
        elif HASH_SYMBOL != word[0]:
            if MENTION_SYMBOL != word[0]:
                if URL_START != word[0:4]:
                    if clean_word(word) != '':
                        words_to_num[clean_word(word)] = 1
                        
    
def common_words(words_to_num: Dict[str, int], upper_bound: int) -> None:
    """Updates words_to_num so it only includes the most common words. At most, 
    upper_bound words should be kept in the dictionary. If the number of words 
    with a particular word count exceeds upper_bound, then none of these words
    should be included
    
    >>> words_to_num = {'we': 1, 'have': 1, 'free': 1, 'icecream': 1}
    >>> common_words(words_to_num, 3)
    >>> words_to_num
    {}
    >>> words_to_num = {'tweet': 3, 'or': 1, 'share': 1, 'your': 1, 'opinion': 1}
    >>> common_words(words_to_num, 1)
    >>> words_to_num
    {'tweet': 3}
    >>> words_to_num = {'we': 3, 'have': 2, 'free': 1, 'icecream': 1}
    >>> common_words(words_to_num, 2)
    >>> words_to_num
    {'we': 3, 'have': 2}
    """
    num_to_words = {}
    
    # invert dictionary so counts can be used to remove words from original dict
    
    for word in words_to_num:
        num = words_to_num[word]
        
        if not (num in num_to_words):
            num_to_words[num] = [word]
        else:
            num_to_words[num].append(word)
                
    # calculate the lowest count and remove all items with that count. Continue
    # till length of dictionary is lower than or equal to upper_bound
    
    while len(words_to_num) > upper_bound:
        min_key = min(num_to_words)
        for value in num_to_words[min_key]:
            words_to_num.pop(value)
        num_to_words.pop(min_key)
      
      
def read_tweets(file: TextIO) -> Dict[str, List[tuple]]:
    """Read all of the data from the file to the dictionary. The dictionary keys
    are lowercase Twitter usernames and the values are the tweets sent by the 
    user. Tweet tuple has the format (text, date, source, favourite count,
    retweet count)
    """
    file_contents = file.readlines()
    all_usernames = []
    all_tweet_data = []
    tweet_data_collector = []    
    primary = []
    secondary = []
    tup0 = ''
    tweets_dict = {}
    i = 0
    
    # collect usernames
    
    for word in file_contents:
        if word != '\n':
            if word[-2] == ':' and word[-1] == '\n':
                if word[:-2].isalnum():
                    all_usernames.append(word[:len(word) - 2])
            elif word[-1] == ':' and file_contents[-1] == word:
                all_usernames.append(word[:len(word) - 1])
    
    # collect all tweet headers and text
    
    for i in range(len(file_contents)):
        if (file_contents[i][:-2] in all_usernames):
            all_tweet_data.append(tweet_data_collector)
            tweet_data_collector = []
        else:
            tweet_data_collector.append(file_contents[i])
                       
    while file_contents.index(all_usernames[-1] + ':\n') < i \
                                                          < len(file_contents):
        tweet_data_collector.append(file_contents[i])
        i = i + 1
        
    all_tweet_data.append(tweet_data_collector)    
    all_tweet_data.pop(0)
    all_tweet_data[-1].pop(-1)        
     
    # create the list of tuples
          
    for i in range(len(all_tweet_data)):
        for j in range(len(all_tweet_data[i])):
            if all_tweet_data[i][j] == '<<<EOT\n':
                secondary.append(tup)
                tup0 = ''
            elif all_tweet_data[i][j - 1] == '<<<EOT\n' or j == 0:
                tup1 = int(all_tweet_data[i][j].split(',')[FILE_DATE_INDEX])
                tup2 = all_tweet_data[i][j].split(',')[FILE_SOURCE_INDEX]
                tup3 = int(all_tweet_data[i][j].split(',') \
                              [FILE_FAVOURITE_INDEX])
                tup4 = int(all_tweet_data[i][j].split(',') \
                              [FILE_RETWEET_INDEX])
            else:
                tup0 = tup0 + all_tweet_data[i][j]
            tup = (tup0, tup1, tup2, tup3, tup4)
        primary.append(secondary)
        secondary = []
    
    # convert usernames to lowercase so they can be added to final dictionary
    
    for i in range(len(all_usernames)):
        all_usernames[i] = all_usernames[i].lower()
    
    # create dictionary that maps usernames to the list of tuples
    
    for i in range(len(all_usernames)):
        tweets_dict[all_usernames[i]] = primary[i]
    return tweets_dict
       
        
def most_popular(username_to_tweet: Dict[str, List[tuple]], date1: int,
                 date2: int) -> str:
    """Return the username of the user who was most popular between the 2 dates
    inclusive. Popularity is the sum of the favourite counts and retweet counts
    for all tweets issued in the time period. Returns tie if no tweets in date
    range or a tie between 2 (or more) users
    
    >>> most_popular({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'IPhone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, 20180801120000, 20180802000000)
    'tie'
    
    >>> most_popular({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, 20180801120000, 20190802000000)
    'Coldplay'
    
    >>> most_popular({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    2, 9), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, 20180801120000, 20190802000000)
    'Bastille'
    """
    popularity_lst = []
    user_lst = []
    current_popularity = 0
    
    for username in username_to_tweet:
        user_lst.append(username)
        for tweet in username_to_tweet[username]:
            if date1 <= tweet[TWEET_DATE_INDEX] <= date2:
                current_popularity = current_popularity + \
                tweet[TWEET_FAVOURITE_INDEX] + tweet[TWEET_RETWEET_INDEX]
        popularity_lst.append(current_popularity)
        current_popularity = 0
    max_popularity_index = popularity_lst.index(max(popularity_lst))
    
    if max(popularity_lst) == 0 or popularity_lst.count(max(popularity_lst)) \
                                                                            > 1:
        return 'tie'
    
    return user_lst[max_popularity_index]

        
def find_hashtags(username_to_tweet: Dict[str, List[tuple]], user: str) \
-> List[str]:
    """Returns a list of unique hashtags used by this particular user
    
    >>> find_hashtags({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, 'Bastille')
    ['hell', 'some']
    
    >>> find_hashtags({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, 'Coldplay')
    ['yo', 'listen']
    
    >>> find_hashtags({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#yeah \
    Just realeased KOD. Give it a listen #yeah:)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #some \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, 'Coldplay')
    []
    """
    
    hashtags_lst = []
    unique_hashtags_lst = []
    
    # create a list of all hashtags used by this user

    for tweet in username_to_tweet[user]:
        hashtags_lst.extend(extract_hashtags(tweet[TWEET_TEXT_INDEX]))
    for hashtag in hashtags_lst:
        if hashtag not in unique_hashtags_lst:
            unique_hashtags_lst.append(hashtag)
    
    hashtags_lst = []
    
    # create a list of hashtags unique to this user
    
    for username in username_to_tweet:
        if username != user:
            for tweet in username_to_tweet[username]:
                hashtags_lst.extend(extract_hashtags(tweet[TWEET_TEXT_INDEX]))
                for hashtag in hashtags_lst:
                    if hashtag in unique_hashtags_lst:
                        unique_hashtags_lst.remove(hashtag)
    return unique_hashtags_lst
                
    
def detect_author(username_to_tweet: Dict[str, List[tuple]], text: str) -> str:
    """Return the username, converted to lowercase, of the most likely author
    of text, based on the number of hashtags used, if possible
    
    >>> detect_author({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, '#hell')
    'bastille'
    >>> detect_author({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, '#sup')
    'unknown'
    >>> detect_author({'Bastille':[('#Hell #yeah guys! Check out my \
    instagram:', 20180830094524, 'Android', 3, 5), ('Dropping #some new merch \
    today! Hell #yeah', 20180921094524, 'Android', 2, 9)], 'Coldplay':[('#YO \
    Just realeased KOD. Give it a #listen #YO :)', 20180830094525, 'I Phone', \
    50, 69), ('Hey guys its me! You can follow me on spotify to #listen \
    #yeah!!!!', 20180915094524, 'Rolie', 1, 1)]}, '#yeah')
    'unknown'
    """
    
    hashtags_in_text = []
    
    hashtags_in_text.extend(extract_hashtags(text))
    
    for hashtag in hashtags_in_text:
        for username in username_to_tweet:
            if hashtag in find_hashtags(username_to_tweet, username):
                return username.lower()
    return 'unknown' 

if __name__ == '__main__':
    pass

    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    # import doctest
    # doctest.testmod()
