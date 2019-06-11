from __future__ import unicode_literals

from django.db import models

import re
import json
# import nlp

try:
    import Queue as Q #python version < 3.0
except ImportError:
    import queue as Q #python3.*

class wordBlock():
    def __init__(self, start, end, kind):
        self.start = start;
        self.end = end;
        self.kind = kind;
    def __lt__(self,other):#operator <
        return self.end < other.start
    def __cmp__(self,other):
        #call global(builtin) function cmp for int
        return cmp(self.start,other.end)

class sentence(models.Model):
    originalText = models.TextField(blank=True)
    annotatedText = models.TextField(blank=True)
    #alteredText = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(originalText):
        stc = sentence();
        #stc.originalText = originalText.replace('\n', ' ').replace('\r', ' ').strip();
        stc.originalText = ' '.join((originalText.split())).strip();
        #stc.analyze();
        return stc;

#    def getScrubbedText(self):
#        self.scrubbedText = '';
#        return self.analyze();
#        #we would rescrub due to frequent update of algorithm.
#        if self.scrubbedText is None:
#            return self.analyze();
#        if self.scrubbedText == '':
#            return self.analyze();
#        return self.scrubbedText;

    def __unicode__(self):
        return self.originalText;

#    def analyze(self):
#        scrubbedContent = "test";#nlp.scrub(self.originalText);
#        i = 0;
#        str_suffix = '';
#        for token in scrubbedContent:
#            j = token[0].idx;
#            if self.originalText[j - 1] == ' ':
#                j = j - 1;
#                str_suffix = ''.join((str_suffix, ' '));
#            if token[1] != '':
#                self.scrubbedText = "".join((self.scrubbedText, self.originalText[i:j], str_suffix, "<scrub type='", token[1].lower() ,"'>"));
#                str_suffix = '</scrub>';
#            else:
#                self.scrubbedText = "".join((self.scrubbedText, self.originalText[i:j], str_suffix));
#                str_suffix = '';
#            i = token[0].idx;
#        self.scrubbedText = "".join((self.scrubbedText, self.originalText[i:len(self.originalText)], str_suffix));
#        self.save();
#        #self.scrubbedText = self.scrubbedText.replace('<scrub></scrub>', ' ').strip();
#        return self.scrubbedText;


class task(models.Model):
    #msg_a1 = models.ForeignKey(sentence, related_name="sentence_a1")
    #msg_a2 = models.ForeignKey(sentence, related_name="sentence_a2")
    #msg_b1 = models.ForeignKey(sentence, related_name="sentence_b1")
    #msg_b2 = models.ForeignKey(sentence, related_name="sentence_b2")
    #msg_c1 = models.ForeignKey(sentence, related_name="sentence_c1")
    sentences = models.TextField(default="[]")
    status = models.IntegerField() #0: init 1: opened 2: answered
    workers = models.TextField(default="[]")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return " ".join((self.id, self.status));

    def getSentences(self):
        ret = []
        stc_ids = json.loads(self.sentences)
        for stc_id in stc_ids:
            ret.append(sentence.objects.get(id=stc_id))
        return ret

class hit(models.Model):
    mTurk_id = models.TextField()
    status = models.IntegerField()
    code = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return " ".join((self.mTurk_id, self.code, self.status));
