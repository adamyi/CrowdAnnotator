from django.shortcuts import render
from django.http import HttpResponse
from .models import sentence
from .models import task
from .models import hit
import re
import json
import random
import string
# from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html', {});

def doScrub(request):
    tsk = task.objects.get(id = request.POST['task_id']);
    hid = request.POST['hit_id'];
    user_hit = hit.objects.get(id=hid);

    if (tsk.status == -1 and user_hit.mTurk_id != "warmup"):
        response_data = {};
        count = 0.0;
        correct = 0.0;

        for stc_id, stc_content in json.loads(request.POST['msg']).iteritems():
            stc = sentence.objects.get(id=stc_id)
            scrubbed = json.loads(stc.annotatedText)
            response_data[stc_id] = scrubbed["warmup"]
            scrubList = re.findall(r'<scrub type=[\'"]\w+?[\'"]>.+?</scrub>', scrubbed["warmup"]);
            count += len(scrubList);
            for scrub in scrubList:
                if (stc_content.find(scrub) != -1):
                    correct += 1;

        if (count > 0 and correct / count < 0.5):
            workers = json.loads(tsk.workers);
            workers.append(user_hit.mTurk_id);
            tsk.workers = json.dumps(workers);
            tsk.save();
            user_hit.status = -2;
            user_hit.save();
            return HttpResponse(json.dumps(response_data), content_type="application/json");
    else:
        if (user_hit.mTurk_id == "warmup"):
            hid = "warmup";
        #TODO: check sentences against task
        for stc_id, stc_content in json.loads(request.POST['msg']).iteritems():
            stc = sentence.objects.get(id=stc_id)
            if (stc.annotatedText == '' or stc.annotatedText is None):
                scrubbed = {}
            else:
                scrubbed = json.loads(stc.annotatedText)
            scrubbed[hid] = stc_content;
            stc.annotatedText = json.dumps(scrubbed);
            stc.save();

        if (hid == "warmup"):
            tsk.status = -1;
        else:
            tsk.status += 1;

    workers = json.loads(tsk.workers);
    workers.append(user_hit.mTurk_id);
    tsk.workers = json.dumps(workers);
        
    user_hit.status += 1;

    tsk.save();
    user_hit.save();
    return HttpResponse("OK");

def getTask(request):
    hid = request.POST['hit_id'];
    user_hit = hit.objects.get(id=hid);
    response_data = {};
    refetch = False;
    # if (1): # for testing
    if (user_hit.status == 3):
        response_data['code'] = user_hit.code;
    if (user_hit.status == -1 and user_hit.mTurk_id != "warmup"):
        tasks = task.objects.filter(status=-1).order_by('status', 'updated_at')[0:10];
    else:
        tasks = task.objects.exclude(status=-1).exclude(status=3).order_by('status', 'updated_at')[0:10];
    for tsk in tasks:
        workers = json.loads(tsk.workers);
        if ( user_hit.mTurk_id not in workers ):
            tsk.save(); #update updated_at timestamp
            if (tsk.status == -1):
                response_data['result'] = 2; # warm-up
            else:
                response_data['result'] = 1; # normal
            response_data['task_id'] = tsk.id;
            stcs = {};
            for stc in tsk.getSentences():
                stcs[stc.id] = stc.originalText;
            response_data['sentences'] = stcs;
            return HttpResponse(json.dumps(response_data), content_type="application/json");
    if (user_hit.status == -1 and user_hit.mTurk_id != "warmup"):
        if (hit.objects.filter(status__gt=-1).filter(mTurk_id=user_hit.mTurk_id).count() > 0):
            tasks = task.objects.exclude(status=-1).exclude(status=3).order_by('status', 'updated_at')[0:10];
            for tsk in tasks:
                workers = json.loads(tsk.workers);
                if ( user_hit.mTurk_id not in workers ):
                    tsk.save(); #update updated_at timestamp
                    user_hit.status = 0; #skip warmup
                    user_hit.save();
                    response_data['result'] = 1; # normal
                    response_data['task_id'] = tsk.id;
                    stcs = {};
                    for stc in tsk.getSentences():
                        stcs[stc.id] = stc.originalText;
                    response_data['sentences'] = stcs;
                    return HttpResponse(json.dumps(response_data), content_type="application/json");
    response_data['result'] = 0;
    response_data['msg'] = "No available tasks for you right now.";
    return HttpResponse(json.dumps(response_data), content_type="application/json");

def getHit(request):
    mTurk_id = request.POST['mTurk_id'];
    user_hit = hit.objects.create(mTurk_id=mTurk_id, status=-1, code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)));
    return HttpResponse(user_hit.id);
