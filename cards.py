#!/usr/bin/env python3

import os

from html import escape
from random import choice
from re import search, sub


class Cards:
    """
    The main class that contains all the logic. The files with the contents
    of white and black cards are loaded once, the rest is handled by class
    methods. Therefore, everything can be accessed statically and no instances
    are needed.

    When the files are loaded, lines starting with `#`, i.e. comments, and
    blank lines are ignored.
    """

    left = "_REPLACED_LEFT_"
    right = "_REPLACED_RIGHT_"

    directory = os.path.dirname(os.path.realpath(__file__))

    white = []
    with open(directory + "/white.txt", "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith("#") and len(line) > 1:
                white.append(line.rstrip())

    black = []
    with open(directory + "/black.txt", "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith("#") and len(line) > 1:
                black.append(line.rstrip())

    @classmethod
    def draw_white(cls):
        """
        Draw a white card and return the text written on it.
        """
        return choice(cls.white)

    @classmethod
    def draw_black(cls):
        """
        Draw a black card and return the text written on it.
        """
        return choice(cls.black)

    @classmethod
    def remove_article(cls, phrase):
        """
        Remove the article from a given phrase and return the result.
        """
        regex = "^(a|an|the) "
        return sub(regex, "", phrase)

    @classmethod
    def to_lowercase(cls, phrase):
        """
        Convert a phrase to lowercase, remove special characters etc.
        and return the result."
        """
        regex = "[ /.]"
        return sub(regex, "-", cls.remove_article(phrase).lstrip().lower())

    @classmethod
    def replace(cls, black, white):
        """
        Replace content on a black card with some white card.

        This function first looks for special replacements as `__NOARTICLE__`
        or `__LOWERCASE__` and replaces the first one it finds. In the end,
        it tries a standard replacement or returns the text unchanged, if no
        replacement string could be found.
        """
        left, right = cls.left, cls.right

        if "__NOARTICLE__" in black:
            return black.replace(
                "__NOARTICLE__", left + cls.remove_article(white) + right, 1
            )

        if "__LOWERCASE__" in black:
            return black.replace(
                "__LOWERCASE__", left + cls.to_lowercase(white) + right, 1
            )

        return sub("__[A-Z]*__", left + white + right, black, 1)

    @classmethod
    def get_phrase(cls, html: bool = False, left="", right=""):
        """
        Return a catchy phrase.

        This function draws a black card and then draws white cards until
        all replacement patterns have been filled with content. It then
        formats the return string a bit so it looks nicer.
        """
        phrase = cls.draw_black()
        while search("__[A-Z_]*__", phrase):
            phrase = cls.replace(phrase, cls.draw_white())

        # Capitalize the first letter of the phrase. If the phrase starts
        # with a white card, we operate at the offset after the replacement
        # indicator.
        pos = len(cls.left)
        if phrase.startswith(cls.left) and phrase[pos] != " ":
            phrase = phrase[0:pos] + phrase[pos].upper() + phrase[pos+1:]
        else:
            phrase = phrase[0].upper() + phrase[1:]

        # If a card starts with a space to prevent capitalization,
        # we strip that space at this point to not mess up the layout.
        phrase = phrase.replace(cls.left + " ", cls.left).lstrip()

        if html:
            phrase = escape(phrase)

        return phrase.replace(cls.left, left).replace(cls.right, right)


def init_flask():
    """
    Initialize the Flask object and create a route to the template.
    """
    from flask import Flask, render_template

    app = Flask(__name__)

    @app.route("/")
    def render():
        return render_template("cards.html", cards=Cards, markup=True)

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
        init_flask().run(debug=True)
    else:
        while True:
            try:
                print(Cards.get_phrase())
            except UnicodeEncodeError:
                continue
            else:
                break
else:
    application = init_flask()

# vim: set expandtab ts=4 sw=4:
