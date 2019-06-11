from django.core.management.base import BaseCommand, CommandError
from scrubber.models import sentence
import os
import glob

class Command(BaseCommand):
    help = 'Import enron dataset'
    def handle(self, *args, **options):
        for filename in glob.glob(os.path.join('../../dataset/enron/enron_dataset_v4/', '*.txt')):
            file = open(filename, 'r');
            stc = sentence.objects.create(originalText = file.read().rstrip("\n"));
            self.stdout.write(self.style.SUCCESS("Created sentence id: %d" % stc.id));
            file.close();
