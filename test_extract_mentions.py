'''A3. Tester for the function extract_mentions in tweets.
'''

import unittest
import tweets

class TestExtractMentions(unittest.TestCase):
    '''Tester for the function extract_mentions in tweets.
    '''

    def test_empty(self):
        '''Empty tweet.'''

        arg = ''
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_no_mention(self):
        '''Non-empty tweet with no mentions.'''

        arg = 'tweet test case'
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
    
    def test_nonempty_mentions(self):
        ''' Non-empty tweet with mentions'''
        
        arg = '@U_of_T: Congrats to all our @5tud3nts on @graduating!'
        actual = tweets.extract_mentions(arg)
        expected = ['u', '5tud3nts', 'graduating']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
        
    def test_nonempty_fake_mention(self):
        ''' Non-empty tweet with mention symbol embedded in word and hashtags'''
        
        arg = '#UTM #activate your id@mail.utoronto.ca addresses #today!'
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


if __name__ == '__main__':
    unittest.main(exit=False)
