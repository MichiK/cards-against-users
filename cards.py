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
        Draw a black card and return the text written on it."
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
        return sub(regex, "-", cls.remove_article(str)) 

    @classmethod
    def replace(cls, black, white, markup=False):
        """
        Replace content on a black card with some white card.
        
        This function first looks for special replacements as `__NOARTICLE__`
        or `__LOWERCASE__` and replaces the first one it finds. In the end,
        it tries a standard replacement or returns the text unchanged, if no
        replacement string could be found.
        """
        if markup:
            s = "<span class=\"insert\">"
            e = "</span>"
        else:
            s = ""
            e = ""
        if "__NOARTICLE__" in black:
            return black.replace(
                "__NOARTICLE__", s + cls.remove_article(white) + e, 1
            )
        elif "__LOWERCASE__" in black:
            return black.replace(
                "__LOWERCASE__", s + cls.to_lowercase(white) + e, 1
            )
        else:
            return black.replace(
                "____", s + white + e, 1
            )
    
    @classmethod
    def get_phrase(cls, html=False, markup=False):
        """
        Return a catchy phrase.

        This function draws a black card and then draws white cards until
        all replacement pattterns have been filled with content. It then
        formats the return string a bit so it looks nicer.
        """
        if markup:
            html = True
        str = cls.draw_black(html=html)
        while search("__[A-Z_]*__", str):
            str = cls.replace(str, cls.draw_white(html=html), markup=markup)
        if str.startswith(" "):
            str = str.lstrip()
        else:
            str = str[0].upper() + str[1:]

        return str.replace("  ", " ")


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
            phrase=Cards.get_phrase(html=True)
        )
    return app

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Return a catchy phrase.")
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="Start Flask's debugging web server"
    )
    args = parser.parse_args()
    if args.debug:
        app = init_flask()
        app.run(debug=True)
    else:
        print Cards.get_phrase()
else:
    application = init_flask()

# vim: set expandtab ts=4 sw=4:
