# -*- coding: utf-8 -*-
'''
    Author    : Huseyin BIYIK <husenbiyik at hotmail>
    Year      : 2016
    License   : GPL

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
nth = {
       1: "first",
       2: "second",
       3: "third",
       4: "fourth",
       5: "fifth",
       6: "sixth",
       7: "seventh",
       8: "eight",
       9: "ninth",
       10: "tenth",
       11: "eleventh",
       12: "twelfth",
       13: "thirteenth",
       14: "fourteenth",
       15: "fifteenth",
       16: "sixteenth",
       17: "seventeenth",
       18: "eighteenth",
       19: "nineteenth",
       20: "twentieth",
       }

iconrate = {
            "bad-icon": 0,
            "neutral-icon": 3,
            "positive-icon": 5,
            }


def fixlangs(code):
    langs = {
        'Big 5 code': 'vi',
        'Brazillian Portuguese': 'pt',
        'Chinese BG code': 'zh',
        'Farsi/Persian': 'fa',
    }
    if code in langs.keys():
        return langs[code]
    else:
        return code
