# -*- coding: utf-8 -*-
import re

HTML_ENTITY_ENCODINGS = {
    '"' : "&quot;",
    "'" : "&apos;",
    '<' : "&lt;",
    '>' : "&gt;",
    '™' : "&trade;",
    '©' : "&copy;",
    '®' : "&reg;",
    '°' : "&deg;",
    '¡' : "&iexcl;",
    '¿' : "&iquest;",
    'æ' : "&aelig;",
    'Æ' : "&AElig;",
    'á' : "&aacute;",
    'Á' : "&Aacute;",
    'ä' : "&auml;",
    'Ä' : "&Auml;",
    'å' : "&aring;",
    'Å' : "&Aring;",
    'ß' : "&szlig;",
    'é' : "&eacute;",
    'É' : "&Eacute;",
    'ë' : "&euml;",
    'Ë' : "&Euml;",
    'í' : "&iacute;",
    'Í' : "&Iacute;",
    'ï' : "&iuml;",
    'Ï' : "&Iuml;",
    'ñ' : "&ntilde;",
    'Ñ' : "&Ntilde;",
    'ó' : "&oacute;",
    'Ó' : "&Oacute;",
    'ö' : "&ouml;",
    'Ö' : "&Ouml;",
    'ø' : "&oslash;",
    'Ø' : "&Oslash;",
    'ú' : "&uacute;",
    'Ú' : "&Uacute;",
    'ü' : "&uuml;",
    'Ü' : "&Uuml;",
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

def htmlRemoveTags(text):
    return re.sub(r'<[^>]*?>', '', text)
