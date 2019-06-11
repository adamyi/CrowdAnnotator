from django.core.management.base import BaseCommand, CommandError
from scrubber.models import sentence
from scrubber.models import task
import pandas as pd
import json
import re

class Command(BaseCommand):
    help = 'Import IM dataset'
    def handle(self, *args, **options):
        data = pd.read_csv("../../dataset/anonymous_im.csv", header=None)
        status = 0
        stc = ""
        scount = 1
        mcount = 0
        tsk = task(status=0);
        ids = [];
        ts = r'\d{13},(received|sent)'
        for row in data.values:
            if pd.notna(row[0]):
                if re.match(ts, row[0]) is not None:
                    if mcount >= 30: # split conversation
                        mcount = 0
                        scount += 1
                        tsk.sentences = json.dumps(ids)
                        tsk.save();
                        self.stdout.write(self.style.SUCCESS("Conversation saved! Task ID: %d" % tsk.id));
                        ids = []
                        tsk = task(status = 0);
                    if pd.isnull(row[2]):
                        status = 1
                        stc = row[1]
                    else:
                        status = 0
                        mcount += 1
                        msg = sentence.objects.create(originalText = row[1]);
                        ids.append(msg.id);
                        print "Conversation %d Message %d (%d)" % (scount, mcount, msg.id)
                    continue
            else:
                row[0] = "";
            if pd.isnull(row[1]):
                if status == 1:
                    stc = "%s\n%s" % (stc, row[0])
                else: # new conversation
                    if mcount != 0:
                        scount += 1
                        mcount = 0
                        tsk.sentences = json.dumps(ids)
                        tsk.save()
                        self.stdout.write(self.style.SUCCESS("Conversation saved! Task ID: %d" % tsk.id));
                        tsk = task(status = 0)
                        ids = []
                continue
            if pd.isnull(row[2]):
                if status == 1:
                    stc = "%s\n%s" % (stc, row[0])
                    status = 0
                    mcount += 1
                    msg = sentence.objects.create(originalText = stc);
                    ids.append(msg.id);
                    print "Conversation %d Message %d (%d)" % (scount, mcount, msg.id)
        if status == 1: # last sentence
            msg = sentence.objects.create(originalText = stc)
            ids.append(msg.id)
            mcount += 1
            print "Conversation %d Message %d (%d)" % (scount, mcount, msg.id)
        if mcount > 0:
            tsk.sentences = json.dumps(ids)
            tsk.save()
            self.stdout.write(self.style.SUCCESS("Conversation saved! Task ID: %d" % tsk.id));
        print "%d conversations" % scount
