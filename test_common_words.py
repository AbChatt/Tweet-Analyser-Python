'''A3. Tester for the function common_words in tweets.
'''

import unittest
import tweets

class TestCommonWords(unittest.TestCase):
    '''Tester for the function common_words in tweets.
    '''

    def test_empty(self):
        '''Empty dictionary.'''

        arg1 = {}
        arg2 = 1
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_one_word_limit_one(self):
        '''Dictionary with one word.'''

        arg1 = {'hello': 2}
        arg2 = 1
        exp_arg1 = {'hello': 2}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
    
    def test_five_words_limit_two(self):
        '''Dictionary with five words'''
        
        arg1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        arg2 = 2
        exp_arg1 = {'d': 4, 'e': 5}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)
        
        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
    
    def test_keep_multiple_words_same_count(self):
        '''Dictionary contains multiple words with the same count'''
        
        arg1 = {'a': 1, 'b': 2, 'c': 4, 'd': 4, 'e': 5}
        arg2 = 3
        exp_arg1 = {'c': 4, 'd': 4, 'e': 5}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)
        
        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
    
    def test_remove_multiple_words_same_count(self):
        '''Dictionary contains multiple words with the same count'''
        
        arg1 = {'a': 1, 'b': 2, 'c': 4, 'd': 4, 'e': 5}
        arg2 = 2
        exp_arg1 = {'e': 5}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)
        
        msg = ("Expected dictionary to be {}\n" +
               "but it was \n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)

if __name__ == '__main__':
    unittest.main(exit=False)
