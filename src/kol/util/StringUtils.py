import htmlentitydefs
import re

def htmlEntityEncode(text):
    for k,v in htmlentitydefs.codepoint2name.iteritems():
        text = text.replace(unichr(k).encode('utf-8'), "&%s;" % v)
    return text

def htmlEntityDecode(text):
    for k,v in htmlentitydefs.name2codepoint.iteritems():
        text = text.replace("&%s;" % k, unichr(v).encode('utf-8'))
    return text

def htmlRemoveTags(text):
    return re.sub(r'<[^>]*?>', '', text)
