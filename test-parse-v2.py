import walk, path from os
import io, contract, nltk

org_fragments = ["Inc.", "INC.", "Incorp.", "INCORP.", "LLC", "N.A.", "L.L.C.", "LP", "L.P.", "B.V.", "BV", "N.V.", "NV", "Corp.", "CORP."]

month_names = ["January", "Jan", "Jan.", "JAN", "JAN.", "February", "Feb", "Feb.", "FEB", "FEB.", "March", "Mar", "Mar.", "MAR", "MAR.", "April", "Apr", "Apr.", "APR", "APR.", "May", "June", "Jun", "Jun.", "JUN", "JUN.", "July", "Jul", "Jul.", "JUL", "JUL.", "August", "Aug", "Aug.", "AUG", "AUG." "September", "Sep", "Sep.", "SEP", "SEP.", "October", "Oct", "Oct.", "OCT", "OCT.", "November", "Nov", "Nov.", "NOV", "NOV.", "December", "Dec", "Dec.", "DEC", "DEC."]

definition_terms = ["Company", "Buyer", "Seller", "Sellers", "Purchaser", "Parent", "Guarantor", "Lender", "Borrower", "Lessor", "Lessee", "Landlord", "Tenant", "Creditor", "Contractor", "Customer", "Indemnitee", "Employer", "Employee", "Bank", "Trustee", "Supplier", "Licensee", "Licensor", "Investor", "Debtor"]

incorp_phrases_3 = ["a Delaware corporation", "a Delaware limited liability company", "a Kansas corporation", "an Arizona corporation", "an Illinois corporation", "a New York corporation", "a California corporation", "a New Jersey corporation"]

name_punctuation = [","]

bad_first_names = ["Art.", "Art", "Article", "Sec.", "Sect.", "Section", "Sec", "Part"]

def parseSamples(path, limit):
    print "begin parse samples"
    num = 0
    for dirpath, subdirs, files in os.walk(path):
        for name in files:
            if name[0] != '.':
                num += 1
                name = os.path.join(dirpath, name)
                f = io.open(name, 'rU', encoding='utf-8', errors='ignore')
                text = f.read()
                if num < limit:
                    print "SAMP. #{}. {}".format(num,name)
                    cleaned_text = clean_text(text)
                    
                    parties = extract_parties(cleaned_text)
                    parties_str = '; '.join(parties)
                    print "Parties: " + parties_str.encode("utf-8")
                    
                    dates = extract_effective_dates(cleaned_text)
                    dates_str = '; '.join(dates)
                    print "Effective date: " + dates_str.encode("utf-8")

                    dates = extract_term_dates(cleaned_text)
                    dates_str = '; '.join(dates)
                    print "Termination date: " + dates_str.encode("utf-8")

                    print ".........................."
    print 'I am done - bite my shiny metal ass!'


def clean_text(text):
    # text = text.replace('“','"')
    return text


def extract_effective_dates(text):
    words = nltk.word_tokenize(text)
    word_total = len(words)
    dates = []
    for idx, val in enumerate(words):
        pct_depth = (float(idx + 1) / word_total) * float(100)

        if pct_depth < 10:
        
            if subsequent_phrase(words,idx,["Effective Date"], 5) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if subsequent_phrase(words,idx,["Effective Date"], 10) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)
        
        if pct_depth < 10 or pct_depth > 85:
            
            if preceding_phrase(words,idx,["dated :", "Dated :"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if preceding_phrase(words,idx,["Date :"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if preceding_phrase(words,idx,["effective as of", "Effective as of"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if preceding_phrase(words,idx,["effective"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if preceding_phrase(words,idx,["entered into as of", "Entered into as of"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if preceding_phrase(words,idx,["dated as of", "Dated as of"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)
        
            if preceding_phrase(words,idx,["as of"]) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

    return dates


def extract_term_dates(text):
    words = nltk.word_tokenize(text)
    word_total = len(words)
    dates = []
    for idx, val in enumerate(words):
        pct_depth = (float(idx + 1) / word_total) * float(100)
        
        if pct_depth < 80:

            if subsequent_phrase(words,idx,["Termination Date"], 5) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if subsequent_phrase(words,idx,["Termination Date"], 10) and looks_like_date(words,idx):
                date = words[idx] + " " + words[idx + 1] + words[idx + 2] + " " + words[idx + 3]
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

            if preceding_phrase(words,idx,["extended automatically for", "automatically extended for", "extend automatically for", "automatically extend for"]):
                date = "automatically extended"
                if not dates:
                    date.encode('utf-8')
                    dates.append(date)

    return dates


def extract_parties(text):
    words = nltk.word_tokenize(text)
    word_total = len(words)
    parties = []
    for idx, val in enumerate(words):
        pct_depth = (float(idx + 1) / word_total) * float(100)
        
        if pct_depth < 10:

            if looks_like_person_name(words,idx):
                party_name = words[idx] + " " + words[idx + 1] + " " + words[idx + 2]
                party_name = clean_party(party_name)
                party_name.encode('utf-8')
                parties.append(party_name)  

            if preceding_phrase(words,idx,["among", "between"]) and looks_like_party_name(words, idx):
                party_name = capture_party_name(words, idx, "right")
                party_name = clean_party(party_name)
                party_name.encode('utf-8')
                parties.append(party_name)  
            
            if preceding_phrase(words,idx,["( Exact name of"]) and words[idx] == "registrant" and looks_like_party_name(words, idx - 5):
                party_name = capture_party_name(words, idx - 5, "left")
                party_name = clean_party(party_name)
                party_name.encode('utf-8')
                if party_name.upper() not in (party.upper() for party in parties):
                    parties.append(party_name)
            
            if preceding_phrase(words,idx,['( The']) and words[idx] == "Company" and subsequent_phrase(words,idx,[')'],1) and looks_like_party_name(words, idx - 3):
                party_name = capture_party_name(words, idx - 3, "left")
                party_name = clean_party(party_name)
                party_name.encode('utf-8')
                if party_name.upper() not in (party.upper() for party in parties):
                    parties.append(party_name)

            if (preceding_phrase(words,idx,['( The']) or preceding_phrase(words,idx,['( the']) or preceding_phrase(words,idx,['('])) and words[idx] in definition_terms:
                if preceding_phrase(words,idx - 2,incorp_phrases_3):
                    party_name = capture_party_name(words, idx - 5, "left")
                    party_name = clean_party(party_name)
                    party_name.encode('utf-8')
                    if party_name.upper() not in (party.upper() for party in parties):
                        parties.append(party_name)
                elif looks_like_party_name(words,idx - 3):
                    party_name = capture_party_name(words, idx - 3, "left")
                    party_name = clean_party(party_name)
                    party_name.encode('utf-8')
                    if party_name.upper() not in (party.upper() for party in parties):
                        parties.append(party_name)
            
    return parties


def looks_like_date(words,idx):
    if words[idx] in month_names and words[idx + 2] == "," and words[idx + 3].isdigit():
        return True 
    else:
        return False

def looks_like_party_name(words,idx):
    cap = "none"
    if words[idx][0].isupper():
        cap = "initial"
    if words[idx].isupper():
        cap = "full"
    if cap == "initial" or cap == "full":
        return True
    else: 
        return False

def looks_like_person_name(words,idx):
    cap = "none"
    if words[idx][0].isupper():
        cap = "initial"
    if words[idx].isupper():
        cap = "full"
    if cap == "initial" or cap == "full":
        next_word_len = len(words[idx + 1])
        if next_word_len == 2 and words[idx + 1][1] == "." and words[idx + 2][0].isupper(): 
            if words[idx] in bad_first_names:
                return False
            else:
                return True
        else: 
            return False
    else: 
        return False

def capture_party_name(words,idx,direction):
    party_name = words[idx]
    cap = "none"
    if words[idx][0].isupper():
        cap = "initial"
    if words[idx].isupper():
        cap = "full"

    if direction == "right" and cap == "full":
        i = 1
        while words[idx + i].isupper():
            party_name += " " + words[idx + i]
            i += 1
        while words[idx + i] in name_punctuation:
            x = i + 1
            if words[idx + x] in org_fragments:
                party_name += words[idx + i] + " " + words[idx + x]
            i += 1  
        return party_name

    if direction == "right" and cap == "initial":
        i = 1
        while words[idx + i][0].isupper():
            party_name += " " + words[idx + i]
            i += 1
        while words[idx + i] in name_punctuation:
            x = i + 1
            if words[idx + x] in org_fragments:
                party_name += words[idx + i] + " " + words[idx + x]
            i += 1  
        return party_name
              
    if direction == "left":
        i = 1
        while words[idx - i].isupper() or words[idx - i] in org_fragments or words[idx - i] in name_punctuation:            
            if words[idx - i].isupper() or words[idx - i] in org_fragments:
                party_name = words[idx - i] + " " + party_name
                i += 1
            if words[idx - i] in name_punctuation:
                x = i + 1
                party_name = words[idx - x] + words[idx - i] + " " + party_name
                i += 2
        return party_name


def preceding_phrase(words,idx,phrases):
    for phrase in phrases:
        phrase_tokens = phrase.split()
        i = 1
        pre_words = []
        while i <= len(phrase_tokens):
            pre_words.insert(0, words[idx - i])
            i += 1
        if phrase_tokens == pre_words:
            return True
        else:
            return False      


def subsequent_phrase(words,idx,phrases,reach):
    for phrase in phrases:
        phrase_tokens = phrase.split()
        offset = 0
        while offset <= reach:
            i = 1
            post_words = []
            while i <= len(phrase_tokens):
                x = i + offset
                post_words.append(words[idx + x])
                i += 1
            if phrase_tokens == post_words:
                return True
            else:
                offset += 1         


def clean_party(party_name):
    party_name = party_name.replace("_", "")
    return party_name


parseSamples('samples/2014/QTR1', 170)
