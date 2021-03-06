from itertools import chain
import cutlet
from pyjyutping import jyutping


def add_phonetics(lines, p):
    if p == 'J':
        katsu = cutlet.Cutlet()
        katsu.use_foreign_spelling = False
        phonetics = ['[tr]' + katsu.romaji(l) for l in lines]
        return list(chain.from_iterable(zip(lines, phonetics)))
    if p == 'Y':
        phonetics = ['[tr]' + jyutping.convert(l) for l in lines]
        return list(chain.from_iterable(zip(lines, phonetics)))
    return lines
