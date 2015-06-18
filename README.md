# LexHacks-Contract-Reader

The original version of this project was completed for [LexHacks 2015](http://www.lexhacks.com) and won the [LexPredict](http://www.lexpredict.com) challenge. The challenge was to create a tool to scan a corpus of unstructured contracts and extract the names of the parties, the effective date, and the termination date or clause. Due to the two-day time limit of the hackathon and our team's limited experience with natural language processing (NLP) we settled on an approach that demonstrated a mix of using NLTK 3 (an Stanford NLP library/framework) for some tasks, such as word tokenization, and a series of custom token parsing rules. Although we won the challenge, we realized the potential to adapt what we created to be part of a more "prop" NLP-based solution to the problem. The hope is to expand this project into a free publically-available resource for parsing contract data.   

## Table of contents

- [Download](#download)
- [Documentation](#documentation)
- [Contributors](#contributors)
- [Copyright and license](#copyright-and-license)

## Download

The files for the project, may be [downloaded here](https://github.com/edwardbryant/lexhacks-contract-reader/archive/master.zip).

### What's included

Within the download you'll find the following directories and files:

```
lexhacks-contract-reader.zip/
├── contract.py
├── test-parse.py
├── test-parse-v2.py
├── screenshot.png
└── README.md
```

## Next Steps

 - Adapt the original project code into an expandable Python class that can be used to perform basic NLP operations on contracts [partially complete].
 - integrate basic NLP steps that were not utilized in the original project into the Python class.

## Documentation

Documentation for using test-parse-v2 is coming soon.

If you can't wait, the class methods are already commented (see contracts.py file) that explain most of what you would need to use it. In addition, test-parse-v2.py is an example use of the class to parse some contract files.  


### Original Hackathon Submission Code

The original project code is located in test-parse.py. This code wasn't written with re-use in mind and includes numerous examples of bad some ugly coding practices. The newer code (see test-parse-v2.py and contract.py) uses nearly the same logic and parsing rules as the original hackathon submission but was rewritten as a Python class. This newer version is much easier to use and includes some extras, such as providing some basic NLP statistics about the text.

Using the original code requires you to have NLTK 3 already installed. After you have NLTK installed, it can be used as follows:

To test the code against some documents, edit the below call to parseSamples() function (which is located at the end of the test-parse.py file). The function takes two params (1) a string which is the path where your contract documents are located, and (2) a int which is the limit on the number of documents to scan. In the example below, the code will return results for the first 170 documents it encounters in any folder or subfolders it encounters at the path provided.         

```
parseSamples('samples/2014/QTR1', 170)
```

After editing the above function call, run test-parse.py from the command line:

```
python test-parse.py
```

## Contributors

The contributors to this project were: [Edward Bryant](http://www.edwardbryant.com), Chase Hertel, Tomek Rabczak, Tetyana Rabczak, Bharat Lavania, and Jon Riley 

## Copyright and License

The project code is offered under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

