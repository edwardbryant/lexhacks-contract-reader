from __future__ import division

import locale

import nltk


class Contract():

    """ Class for representing a contract and performing NLP processing """

    def __init__(self, path, filename, text):
        """ Inits a Contract object, and triggers tokenize(). 
    
        2 Args:
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
        
        Sets 4 Class Vars:
        tokens = the text as a list of tokens
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

        Sets 3 Class Vars:
        setences = the text as a list of setence segments
        sent_count = number of sentences
        avg_sent_length = char count divided by num of sentences 
        """
        self.sentences = nltk.sent_tokenize(self.text)
        self.sent_count = len(self.sentences)
        self.avg_sent_length = self.char_count / self.sent_count


    def extract_parties(self):
        """ Parses text and extracts specific strings which appear to be names 
        of parties to the contract, according to a set of predefined rules.

        No Args

        Sets 6 Class Vars:
        parties = a list of extracted parties.
        parties_rule[x]_count = a int count of the number of instances in which 
        a particular rule was used to id a party.

        """
        self.parties = []
        self.parties_rule1_count = 0
        self.parties_rule2_count = 0
        self.parties_rule3_count = 0
        self.parties_rule4_count = 0
        self.parties_rule5_count = 0
        for idx, val in enumerate(self.tokens):
            depth = (float(idx+1) / self.token_count) * float(100)
            # ORIGINAL RULE #1
            if depth < 10:
                if self.like_person_name(idx):
                    name = " ".join(self.tokens[idx:idx+3])
                    self.parties_rule1_count += 1
                    self.add_party(name)
            # ORIGINAL RULE #2
            if depth < 10:
                triggers = ["among","between"]
                if self.prior(idx,triggers) and self.like_org_name(idx):
                    name = self.capture_org_name(idx,"right")
                    self.parties_rule2_count += 1
                    self.add_party(name)
            # ORIGINAL RULE #3
            if depth < 10:
                triggers = ["( Exact name of"]
                if self.prior(idx,triggers) and self.tokens[idx] == "registrant" and self.like_org_name(idx-5):
                    name = self.capture_org_name(idx-5,"left")
                    self.parties_rule3_count += 1
                    self.add_party(name)
            # ORIGINAL RULE #4
            if depth < 10:
                triggers = ["( The"]
                if self.prior(idx,triggers) and self.tokens[idx] == "Company" and self.subsequent(idx,[')'],1) and self.like_org_name(idx-3):
                    name = self.capture_org_name(idx-3,"left")
                    self.parties_rule4_count += 1                    
                    self.add_party(name)
            # ORIGINAL RULE #5
            if depth < 10:
                triggers = ["( The","( the","("]
                defined_terms = ["Company","Buyer","Seller","Sellers","Purchaser","Parent","Guarantor","Lender","Borrower","Lessor","Lessee","Landlord","Tenant","Creditor","Contractor","Customer","Indemnitee","Employer","Employee","Bank","Trustee","Supplier","Licensee","Licensor","Investor","Debtor"]
                incorp_3 = ["a Delaware corporation","a Kansas corporation","an Arizona corporation","an Illinois corporation","a California corporation"]
                if self.prior(idx,triggers) and self.tokens[idx] in defined_terms:
                    if self.prior(idx-2,incorp_3):
                        name = self.capture_org_name(idx-5,"left")
                        self.parties_rule5_count += 1                    
                        self.add_party(name)
                    elif self.like_org_name(idx-3):
                        name = self.capture_org_name(idx-3,"left")
                        self.parties_rule5_count += 1                    
                        self.add_party(name)


    def capture_org_name(self,idx,direction):
        """ Assemble a string which represents an organization's name. After an 
        a rule in extract_parties is triggered, capture_org_name trys to gather 
        all the words in the name together as a single string which it returns.   

        2 Args:
        idx = an int of the index location where to start parsing for the name.
        direction = a string (right/left) indicating the direction in which 
        to parse for a name. 
        """
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


    def like_org_name(self,idx):
        """ Checks a word token and returns boolean value on whether the token 
        appears to be the proper name of an organization.

        1 Arg:
        idx = an int of the index location of the token to check. 
        """
        w = self.tokens[idx]
        if w.isupper() or w.istitle():
            return True
        else:
            return False


    def like_person_name(self,idx):
        """ Checks a word token and returns boolean value on whether the token 
        (and its subsequent 2 tokens) appear to be a person's name fitting the 
        pattern of "Firstname M. Lastname" making it likely to be a person's 
        name.

        1 Arg:
        idx = an int of the index location of the token to check.
        """
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


    def prior(self,idx,triggers):
        """ Checks the tokens preceding a token for whether a string occurs 
        prior to it and returns a boolean.

        2 Args:
        idx = an int of the index location of the token to look before.
        triggers = a list of strings with any words or phrases to look for. 
        """
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


    def subsequent(self,idx,triggers,reach):
        """ Checks the tokens after a token for whether a string occurs 
        within a given range of tokens and returns a boolean.

        3 Args:
        idx = an int of the index location of the token to look after.
        triggers = a list of strings with any words or phrases to look for. 
        reach = an int representing how many tokens forward to look.
        """        
        for phrase in triggers:
            phrase_tokens = nltk.word_tokenize(phrase)
            offset = 0
            while offset <= reach:
                i = 1
                post_words = []
                while i <= len(phrase_tokens):
                    x = i + offset
                    post_words.append(self.tokens[idx+x])
                    i += 1
                if phrase_tokens == post_words:
                    return True
                else:
                    offset += 1         


    def add_party(self,name):
        name = self.get_cleaned_name(name)
        if name.upper() not in (party.upper() for party in self.parties):       
            self.parties.append(name)


    def get_token(self,token):
        """ Returns an int of index where token first occurred, or -1 if not
        found in text. 

        1 Arg:
        token = a string of the token to find
        """
        try: 
            idx = self.tokens.index(token)
        except:
            idx = -1
        return idx


    def get_words_by_length(self,word_length):
        """ Returns a set of words of a given length, sorted by frequency
        
        1 Arg:
        word_length = an int of word length to target
        """
        word_set = set(self.tokens)
        return_set = []
        for word in word_set:
            if len(word) == word_length:
                return_set.append(word)
        return return_set


    def get_cleaned_name(self,name):
        """ Returns a string with certain special characters removed which may 
        have been extracted with a name.

        1 Arg:
        name = a string representing a contract party (either a person or an 
        organization).
        """
        # add this
        return name


    def get_token_in_context(self,idx,reach = 1):
        """ Returns a list containing a token, with surrounding tokens.

        2 Args:
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


    def get_parties_rule_counts(self):
        return [parties_rule1_count, parties_rule2_count, parties_rule3_count, parties_rule4_count, parties_rule5_count]

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


    def output_parties_rule_data(self):
        """ Output data on individual parsing rule hits

        No Args
        """
        print "\t R1: {0:,g}".format(self.parties_rule1_count)
        print "\t R2: {0:,g}".format(self.parties_rule2_count)
        print "\t R3: {0:,g}".format(self.parties_rule3_count)
        print "\t R4: {0:,g}".format(self.parties_rule4_count)
        print "\t R5: {0:,g}".format(self.parties_rule5_count)


    def test(self):
        x = nltk.FreqDist(self.tokens)
        return nltk.x.most_common(10)
        # print "X: " + str(x)

