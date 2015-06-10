from __future__ import division

import locale

import nltk


class Contract():

    """ Class for representing a contract and performing NLP processing """

    def __init__(self, path, filename, text):
        """ Inits a Contract object. 
    
        Args:
        path = a string of the path to the contract
        filename = a string of the contract's filename
        """
        self.path = path
        self.filename = filename
        self.text = text
        self.char_count = len(self.text)


    def tokenize(self):
        """ Breaks a Contract object into a list of word tokens and takes 
        populates some class vars with some basic NLP statistics. 

        No Args
        
        Sets Class Vars:
        word_tokens = the obj as a list of tokens
        token_count = an int of number of tokens in contract
        unique_tokens = a list of distinct tokens in contract, sorted
        unique_token_count = an int of number of unique tokens 
        """
        self.word_tokens = nltk.word_tokenize(self.text)
        self.token_count = len(self.word_tokens)
        self.unique_tokens = sorted(set(self.word_tokens))
        self.unique_token_count = len(set(self.word_tokens))


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
        calling output methods for char_count, token_count, and 
        unique_token_count.

        No Args
        """
        self.output_char_count()
        self.output_token_count()       
        self.output_unique_token_count()       


    def output_char_count(self):
        """ Outputs doc character_count to the command line.

        No Args
        """
        # locale.format("%d", 1255000, grouping=True)
        count = "{0:,g}".format(self.char_count)
        print "\t CHARS: {}".format(count)


    def output_token_count(self):
        """ Outputs doc token_count to the command line, or error.

        No Args
        """
        if hasattr(self, 'token_count'):
            count = "{0:,g}".format(self.token_count)
            print "\t TOKENS: {}".format(count)
        else:
            print "\t ERROR: must tokenize method first."


    def output_unique_token_count(self):
        """ Outputs doc's unique_token_count to the command line, or error.

        No Args
        """
        if hasattr(self, 'unique_token_count'):
            count = "{0:,g}".format(self.unique_token_count)
            print "\t UNIQUE TOKENS: {}".format(count)
        else:
            print "\t ERROR: must tokenize method first."

