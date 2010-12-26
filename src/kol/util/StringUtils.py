# -*- coding: utf-8 -*-

HTML_ENTITY_ENCODINGS = {
    '"' : "&quot;",
    "'" : "&apos;",
    '<' : "&lt;",
    '>' : "&gt;",
    '™' : "&trade;",
    '©' : "&copy;",
    '®' : "&reg;",
    '°' : "&deg;",
    '¿' : "&iquest;",
    'ñ' : "&ntilde;"
}

def htmlEntityEncode(text):
    text = text.replace('&', "&amp;")
    for k,v in HTML_ENTITY_ENCODINGS.iteritems():
        text = text.replace(k, v)
    return text

def htmlEntityDecode(text):
    for k,v in HTML_ENTITY_ENCODINGS.iteritems():
        text = text.replace(v, k)
    text = text.replace("&amp;", '&')
    return text
