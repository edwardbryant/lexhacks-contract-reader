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
                    k.tokenize()
                    k.output_basic_stats()

    print ".......................... END ..........................."
    print " "

parseSamples('../contract-data/2014/QTR1/20140102', 170)
