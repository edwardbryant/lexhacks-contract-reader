#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os, io
import contract


def parseSamples(path, limit):
    print " "
    print "......................... START .........................."
    num = 0
    for dirpath, subdirs, files in os.walk(path):
        for filename in files:
            if filename[0] != '.':
                num += 1
                name = os.path.join(dirpath, filename)
                f = io.open(name, 'rU', encoding='utf-8', errors='ignore')
                text = f.read()
                if num < limit:
                    k = contract.Contract(dirpath, filename, text)
                    k.output_filename_header(num)
                    k.output_basic_stats()

                    k.extract_parties()
                    k.output_parties()
                    # k.output_parties_rule_data()
                    print " \n "
                    
                    # output set of tokens which includes 5 tokens before 
                    # and after the first occurrence of the token "agreement" 
                    # print k.get_token_in_context(k.find_token('agreement'), 8)

                    # k.test()


    print ".......................... END ..........................."
    print " "

parseSamples('../contract-data/2014/QTR1', 20)
