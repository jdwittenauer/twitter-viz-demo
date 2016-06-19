# The code below was adapted from Chris Potts' implementation at
# http://sentiment.christopherpotts.net/code-data/happyfuntokenizing.py

import re
import htmlentitydefs


def get_regex_strings():
    return (
        # Phone numbers:
        r"""
        (?:
          (?:            # (international)
            \+?[01]
            [\-\s.]*
          )?
          (?:            # (area code)
            [\(]?
            \d{3}
            [\-\s.\)]*
          )?
          \d{3}          # exchange
          [\-\s.]*
          \d{4}          # base
        )"""
        ,
        # Emoticons:
        r"""
        (?:
          [<>]?
          [:;=8]                     # eyes
          [\-o\*\']?                 # optional nose
          [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
          |
          [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
          [\-o\*\']?                 # optional nose
          [:;=8]                     # eyes
          [<>]?
        )"""
        ,
        # HTML tags:
         r"""<[^>]+>"""
        ,
        # Twitter username:
        r"""(?:@[\w_]+)"""
        ,
        # Twitter hashtags:
        r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
        ,
        # Remaining word types:
        r"""
        (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
        |
        (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
        |
        (?:[\w_]+)                     # Words without apostrophes or dashes.
        |
        (?:\.(?:\s*\.){1,})            # Ellipsis dots.
        |
        (?:\S)                         # Everything else that isn't whitespace.
        """
        )


def html2unicode(s):
    # These are for regularizing HTML entities to Unicode:
    html_entity_digit_re = re.compile(r"&#\d+;")
    html_entity_alpha_re = re.compile(r"&\w+;")

    # First the digits:
    ents = set(html_entity_digit_re.findall(s))
    if len(ents) > 0:
        for ent in ents:
            entnum = ent[2:-1]
            try:
                entnum = int(entnum)
                s = s.replace(ent, unichr(entnum))
            except:
                pass

    # Now the alpha versions:
    ents = set(html_entity_alpha_re.findall(s))
    ents = filter((lambda x : x != "&amp;"), ents)

    for ent in ents:
        entname = ent[1:-1]
        try:
            s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
        except:
            pass
        s = s.replace("&amp;", " and ")

    return s


def tokenize(s):
    # This is the core tokenizing regex:
    word_re = re.compile(r"""(%s)""" % "|".join(get_regex_strings()), re.VERBOSE | re.I | re.UNICODE)

    # The emoticon string gets its own regex so that we can preserve case for them as needed:
    emoticon_re = re.compile(get_regex_strings()[1], re.VERBOSE | re.I | re.UNICODE)

    # Try to ensure unicode:
    try:
        s = unicode(s)
    except UnicodeDecodeError:
        s = str(s).encode('string_escape')
        s = unicode(s)

    # Fix HTML character entitites:
    s = html2unicode(s)

    # Tokenize:
    words = word_re.findall(s)

    # Possible alter the case, but avoid changing emoticons like :D into :d:
    words = map((lambda x : x if emoticon_re.search(x) else x.lower()), words)

    return words
