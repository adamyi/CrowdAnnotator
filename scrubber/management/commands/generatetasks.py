from django.core.management.base import BaseCommand, CommandError
from scrubber.models import task

class Command(BaseCommand):
    help = 'Generate tasks based on enron & twitter data'
    def handle(self, *args, **options):
        y = 17113;
        for x in range(1, 17113):
            tsk = task.objects.create(msg_a1_id=y,msg_a2_id=y+1,msg_b1_id=y+2,msg_b2_id=y+3,msg_c1_id=x,status=0);
            self.stdout.write(self.style.SUCCESS("Created task id: %d" % tsk.id));
            y += 4;
