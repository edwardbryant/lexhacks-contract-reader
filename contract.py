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


    def extract_parties(self):
        """ [comment]
        """
        self.parties = []
        for idx, val in enumerate(self.tokens):
            depth = (float(idx+1) / self.token_count) * float(100)
            # print "\r\t {}".format(depth),

            """
            ORIGINAL RULE #1
            within the first 10 pct of text, assume a 3-token string that looks 
            like a name with a middle initial is a party to the contract. 
            """
            if depth < 10:
                if self.like_person_name(idx):
                    name = " ".join(self.tokens[idx:idx+3])
                    self.add_party(name)

            """
            ORIGINAL RULE #2
            within first 10 pct of text, assume phrases with full or initial  
            capitalization immediately following the words "among" or "between"
            are parties to the contract.   
            """
            if depth < 10:
                triggers = ["among","between"]
                if self.prior_phrase(idx,triggers) and self.like_org_name(idx):
                    name = self.capture_org_name(idx,"right")
                    self.add_party(name)

            """
            ORIGINAL RULE #3
            within first 10 pct of text, assume phrases with full or initial 
            capitalization before the phrase "(Exact name of registrant ..."
            is a party to the contract. Designed for language on certain SEC 
            filings.  
            """
            if depth < 10:
                triggers = ["( Exact name of"]
                if self.prior_phrase(idx,triggers) and self.tokens[idx] == "registrant" and self.like_org_name(idx-5):
                    name = self.capture_org_name(idx-5,"left")
                    self.add_party(name)


    def clean_name(self,name):
        # add this
        return name


    def add_party(self,name):
        name = self.clean_name(name)
        if name.upper() not in (party.upper() for party in self.parties):       
            self.parties.append(name)


    def prior_phrase(self,idx,triggers):
        for phrase in triggers:
            phrase_tokens = nltk.word_tokenize(phrase)
            i = 1
            pre_words = []
            while i <= len(phrase_tokens):
                pre_words.insert(0,self.tokens[idx-i])
                i += 1
            if phrase_tokens == pre_words:
                return True
            else:
                return False      


    def like_org_name(self,idx):
        w = self.tokens[idx]
        if w.isupper() or w.istitle():
            return True
        else:
            return False


    def capture_org_name(self,idx,direction):
        punc = [","]
        frag = ["Inc.","INC.","Incorp.","INCORP.","LLC","N.A.","L.L.C.","LP","L.P.","B.V.","BV","N.V.","NV","Corp.","CORP."]
        name = self.tokens[idx]
        cap = "none"
        if self.tokens[idx].istitle():
            cap = "initial"
        if self.tokens[idx].isupper():
            cap = "full"
        if direction == "right" and cap == "full":
            i = 1
            while self.tokens[idx+i].isupper():
                name += " " + self.tokens[idx+i]
                i += 1
            while self.tokens[idx+i] in punc:
                x = i + 1
                if self.tokens[idx+x] in frag:
                    name += self.tokens[idx+i] + " " + self.tokens[idx+x]
                i += 1
            return name
        if direction == "right" and cap == "initial":
            i = 1
            while self.tokens[idx+i].istitle():
                name += " " + self.tokens[idx+i]
                i += 1
            while self.tokens[idx+i] in punc:
                x = i + 1
                if self.tokens[idx+x] in frag:
                    name += self.tokens[idx+i] + " " + self.tokens[idx+x]
                i += 1  
            return name
        if direction == "left":
            c = punc + frag
            i = 1
            while self.tokens[idx-i].isupper() or self.tokens[idx-i] in c:            
                if self.tokens[idx-i].isupper() or self.tokens[idx-i] in frag:
                    name = self.tokens[idx-i] + " " + name
                    i += 1
                if self.tokens[idx-i] in punc:
                    x = i + 1
                    name = self.tokens[idx-x] + self.tokens[idx-i] + " " + name
                    i += 2
            return name


    def like_person_name(self,idx):
        bad_names = ["Art.","Art","Article","Sec.","Sect.","Section","Sec","Part"]
        w = self.tokens[idx:idx+3]
        if w[0].istitle() or w[0].isupper():
            next_len = len(w[1])
            if next_len==2 and w[1][1]=="." and w[2][0].isupper(): 
                if w[0] in bad_names:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False


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
        print "\t FILE: {}".format(self.path + "/" + self.filename)

 
    def output_basic_stats(self):
        """ Outputs basic NLP document statistics to the command line by 
        calling output methods for char_count, page_est, token_count, and 
        unique_token_count.

        No Args
        """
        print "\t ------------------------------------- "
        self.output_char_count()
        self.output_page_est()
        self.output_token_count()
        self.output_unique_token_count()
        self.output_sent_count()
        self.output_avg_sent_length()
        print "\t ------------------------------------- "
    

    def output_char_count(self):
        """ Outputs character_count of text to the command line.

        No Args
        """
        print "\t CHARS: {0:,g}".format(self.char_count)


    def output_page_est(self):
        """ Outputs page estimate (based on 1800 chars per) of text to the 
        command line.

        No Args
        """
        print "\t PAGE EST: {0:.2f} @ 1800 chars per page".format(self.page_est)


    def output_token_count(self):
        """ Outputs token_count of text to the command line, or error.

        No Args
        """
        print "\t TOKENS: {0:,g}".format(self.token_count)


    def output_unique_token_count(self):
        """ Outputs unique_token_count of text to the command line, or error.

        No Args
        """
        print "\t UNIQUE TOKENS: {0:,g}".format(self.unique_token_count)


    def output_sent_count(self):
        """ Output sent_count of text to the command line.

        No Args 
        """
        print "\t SENT SEGMENTS: {0:,g}".format(self.sent_count)


    def output_avg_sent_length(self):
        """ Output the average length of a sentence in the text to the command 
        line.

        No Args
        """
        print "\t AVG SENT LENGTH: {0:.2f} chars".format(self.avg_sent_length)


    def output_parties(self):
        """ Output the parties extracted from the text.

        No Args
        """ 
        str_parties = '; '.join(self.parties)
        print "\t PARTIES: " + str_parties

    def test(self):
        x = nltk.FreqDist(self.tokens)
        return nltk.x.most_common(10)
        # print "X: " + str(x)

