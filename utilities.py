import http
import re
import urllib
from urllib import parse
from urllib.parse import urlparse, quote, urlunparse
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup

count = 0


class Printer:
    eq = '===================================================================================================='
    minus = '----------------------------------------------------------------------------------------------------'
    base = len('PROGRAM START')

    @staticmethod
    def print_equal(to_print):
        other_len = len(to_print)
        eq = Printer.eq
        base = Printer.base
        if other_len > base:
            diff = int((other_len - base) / 2)
            eq = eq[:-diff]
        elif other_len < base:
            diff = int((base - other_len) / 2)
            for j in range(diff):
                eq = ''.join([eq, '='])
        print(''.join([eq, " ", to_print, " ", eq]))

    @staticmethod
    def print_minus(to_print):
        other_len = len(to_print)
        minus = Printer.minus
        base = Printer.base
        if other_len > base:
            diff = int((other_len - base) / 2)
            minus = minus[:-diff]
        elif other_len < base:
            diff = int((base - other_len) / 2)
            for j in range(diff):
                minus = ''.join([minus, '-'])
        print(''.join([minus, " ", to_print, " ", minus]))


def url_encode_non_ascii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b.decode('utf-8'))


def iri_to_uri(iri):
    parts = urllib.parse.urlparse(iri)
    return urllib.parse.urlunparse([url_encode_non_ascii(part.encode('utf-8')) for part in parts])


def open_connection(url):
    req = requests.get(url).text
    return BeautifulSoup(req, 'html.parser')


def check_link(url):
    url_split = urlparse(url)
    url_path = parse.quote(url_split[2])
    url = ''.join([url_split[0], "://", url_split[1], "/", url_path])
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        urlopen(req).read()
    except http.client.IncompleteRead:
        return True
    except urllib.error.HTTPError as e:
        if e.getcode() == 404:
            return False
    return True
