# Cards against Users

Following the rules of the infamous "Cards against Humanity", this script
cracks lines by drawing black and white cards and combining them randomly.

The script `cards.py` is a full blown Flask web application and can be
integrated in any WSGI-capable web server using `cards.wsgi`. If `cards.py`
is executed on the command line, it returns a catchy saying. To start the
debugging/development web server, call it as `./cards.py -d`.

The two files `white.txt` and `black.txt` contain the content of the white
and black cards, respectively, one per line. Comments starting with `#` as
well as blank (empty) lines are ignored.

`black.txt` contains the phrases with one or more blank spots. Blank spots
are denoted by a number of placeholders:

* `____` is a standard replacement, i.e. a word is inserted here without any
  changes

* `__NOARTICLE__` removes the article (a, an or the) from the word inserted
  if present

* `__LOWERCASE__` removes the article as well as any special characters
  (blanks, slashes, dots) from the word inserted and renders it lowercase
  so it is suited for phrases that resemble commands etc.

`white.txt` contains the words which are inserted into the blank spots on
black cards. Articles should be written lowercase. If a word is always
written lowercase, even at the beginning of a sentence (i.e. a command),
a space can be added in front of the word to prevent capitalization.
