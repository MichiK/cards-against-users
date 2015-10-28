#!/usr/bin/env python2.7

import os

from cgi import escape
from random import choice
from re import search, sub

class Cards():
    """
    The main class that contains all the logic. The files with the contents
    of white and black cards are loaded once, the rest is handled by class
    methods. Therefore, everything can be accessed statically and no instances
    are needed.

    When the files are loaded, lines starting with `#`, i.e. comments, and
    blank lines are ignored.
    """

    s = "_REPLACED_S_"
    e = "_REPLACED_E_"

    d = os.path.dirname(os.path.realpath(__file__))

    white = []
    with open(d + "/white.txt", "r") as f:
        for l in f:
            if not l.startswith("#") and len(l) > 1:
                white.append(l.decode("utf-8").rstrip())

    black = []
    with open(d + "/black.txt", "r") as f:
        for l in f:
            if not l.startswith("#") and len(l) > 1:
                black.append(l.decode("utf-8").rstrip())

    @classmethod
    def draw_white(cls, html=False):
        """
        Draw a white card and return the text written on it.
        """
        if html:
            return escape(choice(cls.white))
        else:
            return choice(cls.white)
    
    @classmethod
    def draw_black(cls, html=False):
        """
        Draw a black card and return the text written on it.
        """
        if html:
            return escape(choice(cls.black))
        else:
            return choice(cls.black)

    @classmethod
    def remove_article(cls, str):
        """
        Remove the article from a string given and return the result.
        """
        regex = "^(a|an|the) "
        return sub(regex, "", str)

    @classmethod
    def to_lowercase(cls, str):
        """
        Convert a string to lowercase, remove special characters etc.
        and return the result."
        """
        regex = "[ \/\.]"
        return sub(regex, "-", cls.remove_article(str).lstrip().lower())

    @classmethod
    def replace(cls, black, white):
        """
        Replace content on a black card with some white card.
        
        This function first looks for special replacements as `__NOARTICLE__`
        or `__LOWERCASE__` and replaces the first one it finds. In the end,
        it tries a standard replacement or returns the text unchanged, if no
        replacement string could be found.
        """
        s = cls.s
        e = cls.e
        if "__NOARTICLE__" in black:
            return black.replace(
                "__NOARTICLE__", s + cls.remove_article(white) + e, 1
            )
        elif "__LOWERCASE__" in black:
            return black.replace(
                "__LOWERCASE__", s + cls.to_lowercase(white) + e, 1
            )
        else:
            return sub("__[A-Z]*__", s + white + e, black, 1)
    
    @classmethod
    def get_phrase(cls, html=False):
        """
        Return a catchy phrase.

        This function draws a black card and then draws white cards until
        all replacement pattterns have been filled with content. It then
        formats the return string a bit so it looks nicer.
        """
        str = cls.draw_black(html=html)
        while search("__[A-Z_]*__", str):
            str = cls.replace(str, cls.draw_white(html=html))

        l = len(cls.s)
        if str.startswith(cls.s) and str[l] != " ":
            str = str[0:l] + str[l].upper() + str[l+1:]
        else:
            str = str[0].upper() + str[1:]

        str = str.replace(cls.s + " ", cls.s).lstrip()

        if not html:
            str = str.replace(cls.s, "").replace(cls.e, "")

        return str


def init_flask():
    """
    Initialize the Flask object and create a route to the template.
    """
    from flask import Flask, render_template
    app = Flask(__name__)
    @app.route("/")
    def render():
        return render_template(
            "cards.html",
            phrase=Cards.get_phrase(html=True),
            s=Cards.s, e=Cards.e,
            markup=True
        )
    return app

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Return a catchy phrase.")
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="start Flask's debugging web server"
    )
    args = parser.parse_args()
    if args.debug:
        app = init_flask()
        app.run(debug=True)
    else:
        print Cards.get_phrase()

# vim: set expandtab ts=4 sw=4:
