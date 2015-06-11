from __future__ import division

import locale

import nltk


class Contract():

    """ Class for representing a contract and performing NLP processing """

    def __init__(self, path, filename, text):
        """ Inits a Contract object, and triggers tokenize(). 
    
        Args:
        path = a string of the path to the contract
        filename = a string of the contract's filename
        """
        self.path = path
        self.filename = filename
        self.text = text
        self.char_count = len(self.text)
        self.page_est = self.char_count / 1800
        self.tokenize()
        self.segment()


    def tokenize(self):
        """ Breaks a Contract obj into a list of tokens and takes populates 
        some class vars with basic NLP statistics. 

        No Args
        
        Sets Class Vars:
        tokens = the obj as a list of tokens
        token_count = an int of number of tokens in contract
        unique_tokens = a list of distinct tokens in contract, sorted
        unique_token_count = an int of number of unique tokens 
        """
        self.tokens = nltk.word_tokenize(self.text)
        self.token_count = len(self.tokens)
        self.unique_tokens = sorted(set(self.tokens))
        self.unique_token_count = len(set(self.tokens))


    def segment(self):
        """ Breaks a Contract obj into a list of sentences and populates some 
        class vars with additional statistics.

        No Args

        Sets Class Vars:
        sent_count = number of sentences
        avg_sent_length = char count divided by num of sentences 
        """
        self.sentences = nltk.sent_tokenize(self.text)
        self.sent_count = len(self.sentences)
        self.avg_sent_length = self.char_count / self.sent_count


    def find_token(self,token):
        """ Returns an int of index where token first occurred, or -1 if not
        found in text. 

        Args:
        token = a string of the token to find
        """
        try: 
            idx = self.tokens.index(token)
        except:
            idx = -1
        return idx


    def find_words_by_length(self,word_length):
        """ Returns a set of words of a given length, sorted by frequency
        
        Args:
        word_length = an int of word length to target
        """
        word_set = set(self.tokens)
        return_set = []
        for word in word_set:
            if len(word) == word_length:
                return_set.append(word)
        return return_set


    def get_token_in_context(self, idx, reach = 1):
        """ Returns a list containing a token, with surrounding tokens.

        Arg:
        idx = an int of the target token
        reach = an int of the number of tokens on each side of token to return 
        """
        if idx >= 0:
            start = idx - reach
            if start < 0: 
                start = 0
            end = idx + reach
            if end > self.token_count - 1:
                end = self.token_count - 1 
            return self.tokens[start:end]
        else:
            return []


    def output_filename_header(self, num = -1):
        """ Outputs a basic header with path and filename to the command line.

        Args:
        num (optional) = assign a document number in header
        """
        if num > 0:
            print "DOC. #{}.".format(num)
        else:
            print "DOC."
        print "\t FILE: {}".format(self.path + self.filename)

 
    def output_basic_stats(self):
        """ Outputs basic NLP document statistics to the command line by 
        calling output methods for char_count, page_est, token_count, and 
        unique_token_count.

        No Args
        """
        self.output_char_count()
        self.output_page_est()
        self.output_token_count()
        self.output_unique_token_count()
        self.output_sent_count()
        self.output_avg_sent_length()


    def output_char_count(self):
        """ Outputs character_count of text to the command line.

        No Args
        """
        count = "{0:,g}".format(self.char_count)
        print "\t CHARS: {}".format(count)


    def output_page_est(self):
        """ Outputs page estimate, based on 1800 chars per page, of text to the 
        command line.

        No Args
        """
        count = "{0:.2f}".format(self.page_est)
        print "\t PAGES (EST): {}".format(count)


    def output_token_count(self):
        """ Outputs token_count of text to the command line, or error.

        No Args
        """
        if hasattr(self, 'token_count'):
            count = "{0:,g}".format(self.token_count)
            print "\t TOKENS: {}".format(count)
        else:
            print "\t ERROR: must tokenize method first."


    def output_unique_token_count(self):
        """ Outputs unique_token_count of text to the command line, or error.

        No Args
        """
        if hasattr(self, 'unique_token_count'):
            count = "{0:,g}".format(self.unique_token_count)
            print "\t UNIQUE TOKENS: {}".format(count)
        else:
            print "\t ERROR: must use tokenize method first."


    def output_sent_count(self):
        """ Output sent_count of text to the command line.

        No Args 
        """
        count = "{0:,g}".format(self.sent_count)
        print "\t SENTS: {}".format(count)


    def output_avg_sent_length(self):
        """ Outputs the average length of a sentence in the text to the 
        command line.

        No Args
        """
        count = "{0:.2f}".format(self.avg_sent_length)
        print "\t SENT LEN (AVG): {}".format(count)


    def test(self):
        x = nltk.FreqDist(self.tokens)
        return nltk.x.most_common(10)
        # print "X: " + str(x)

