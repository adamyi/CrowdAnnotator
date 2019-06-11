from django.core.management.base import BaseCommand, CommandError
from scrubber.models import sentence

class Command(BaseCommand):
    help = 'Import twitter dataset'
    def handle(self, *args, **options):
        with open("../../dataset/twitter-chat/twitter_en_downsized_v3.txt") as file:
            for line in file:
                stc = sentence.objects.create(originalText = line);
                self.stdout.write(self.style.SUCCESS("Created sentence id: %d" % stc.id));
