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
import sublib
import sublib.utils
import defs

import re
import os
from difflib import SequenceMatcher

domain = "http://www.subscene.com"


def norm(txt):
    txt = txt.replace(" ", "")
    txt = txt.lower()
    return txt


def striphtml(txt):
    txt = re.sub("<.*?>", "", txt)
    txt = re.sub("\t", "", txt)
    txt = re.sub("\n", "", txt)
    txt = txt.replace("  ", " ")
    return txt


def similar(a, b, ratio):
    rate = SequenceMatcher(None, norm(a), norm(b)).ratio()
    return rate * 100 >= ratio


class subscene(sublib.service):

    def search(self):
        if self.item.show and self.item.season:
            self.find("%s %s Season" % (self.item.title, defs.nth[self.item.season].title()))
        else:
            self.find(self.item.title)

    def checkpriority(self, name, numfiles=0):
        skip = False
        rank = 0
        if self.item.show:
            title, show, season, episode = sublib.utils.infofromstr(name)
            if episode:
                if self.item.episode == episode:
                    rank = 1
                else:
                    skip = True
        else:
            rank = -numfiles
        return skip, rank

    def scrapepage(self, page):
        rows = re.findall('<tr>\s+?<td class="a1">(.*?)</tr>', page, re.DOTALL)
        for row in rows:
            link = re.search('<a href="(\/subtitles.*?)"', row)
            rate_iso_name = re.search('<span class="l r (.+?)">\s*(.+?)\s*<\/span>\s+?<span>\s*(.+?)\s*?<\/span>', row, re.DOTALL)
            files = re.search('<td class="a3">\s*([0-9]*)\s*<\/td>', row, re.DOTALL)
            cc = re.search('<td class="a41">', row)
            owner = re.search('<td class="a5">\s*(.*?)\s*<\/td>', row, re.DOTALL)
            comment = re.search('<td class="a6">\s*<div>\s*(.*?)\s*<\/div>', row, re.DOTALL)
            name = rate_iso_name.group(3)
            if comment:
                name += ": %s" % striphtml(comment.group(1))
            if owner:
                name += ": %s" % striphtml(owner.group(1))
            lang = defs.fixlangs(rate_iso_name.group(2))
            rate = rate_iso_name.group(1)
            try:
                sub = self.sub(name, lang)
            except ValueError:
                sub = self.sub(name, "en")
            sub.rating = defs.iconrate.get(rate, 0)
            if cc:
                sub.cc = True
            if files and files.group(1).isdigit():
                files = int(files.group(1))
            else:
                files = -1
            skip, priority = self.checkpriority(rate_iso_name.group(3), files)
            if skip:
                continue
            sub.priority = priority
            sub.download(domain + link.group(1))
            self.addsub(sub)

    def find(self, query):
        q = {"q": query, "l": ""}
        page = self.request(domain + "/subtitles/title", q, referer=domain)
        titles = re.findall(r'<a href="(/subtitles/.+?)">(.+?)</a>', page)
        found = False
        poss = range(50, 101, 5)
        poss.sort(reverse=True)
        for pos in poss:
            for link, name in titles:
                year = re.search("\(([0-9]{4})\)", name)
                # check if title has year info
                if year:
                    year = year.group(1)
                    name = name.replace("(%s)" % year, "").strip()
                    year = int(year)
                else:
                    year = None
                season = -1
                # check if title has season info
                for s, n in defs.nth.iteritems():
                    sreg = re.search('(.*?)\s\-\s%s\sSeason' % n.title(), name)
                    if sreg and sreg.lastindex == 1:
                        season = s
                        name = sreg.group(1).strip()
                    if season >= 0:
                        break
                names = []
                # check if title has alternative naming in (alternative name)
                for n in re.findall("\((.+?)\)", name):
                    names.append(name.strip())
                name = re.sub("\((.+?)\)", "", name)
                # check if title has alternative naming seperated with /
                name = name.split("/")
                name = [x.strip() for x in name]
                names.extend(name)
                for name in names:
                    if similar(self.item.title, name, pos) and \
                        ((self.item.show and self.item.season == season) or
                            (self.item.year is None or self.item.year == year)):
                        self.scrapepage(self.request(domain + link, referer=domain))
                        found = True
                        break
                if found:
                    break
            if found:
                break

    def download(self, link):
        page = self.request(link)
        link = re.search('<a href="(/subtitle/download.+?)"', page)
        link = domain + link.group(1)
        remfile = self.request(link, None, None, domain, True)
        fname = remfile.info().getheader("Content-Disposition")
        fname = re.search('filename=(.*)', fname)
        fname = fname.group(1)
        fname = os.path.join(self.path, fname)
        with open(fname, "wb") as f:
            f.write(remfile.read())
        self.addfile(fname)
