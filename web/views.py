#!/usr/bin/env python
# encoding=utf-8

from django.contrib.auth import authenticate, login
from django.shortcuts import (render_to_response, HttpResponseRedirect, 
                              HttpResponse)
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from datetime import datetime, date

import sys

from models import *
from utils import *

def handle_uploaded_file(f):
    fname = '/tmp/form_%s.xls' % datetime.now().strftime('%s')
    destination = open(fname, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return fname

@login_required
def index(request):

    context = {}
    context.update({'user': request.user})

    reports = MalariaReport.objects.all().order_by('-year', '-month', 'health_center')
    context.update({'reports': reports})

    return render_to_response('index.html', context, context_instance=RequestContext(request))

@login_required
def view(request, report_id):

    context = {}
    context.update({'user': request.user})

    try:
        report = MalariaReport.objects.get(id=report_id)
    except:
        report = None
    context.update({'report': report})

    return render_to_response('view.html', context, context_instance=RequestContext(request))

@login_required
def add(request):

    context = {}
    context.update({'user': request.user})

    if request.method == 'POST':
        if 'fichier' in request.FILES:
            print "RECEIVED FILE"
            filepath = handle_uploaded_file(request.FILES['fichier'])
            print filepath

            status, errors, instance = analyze_xls_form(filepath, request.user)

            print status
            print errors
            print instance

            context.update({'answer': True, 'status': status, 'verbose_status': verbose_status(status), 'instance': instance, 'errors': errors})

    return render_to_response('add.html', context, context_instance=RequestContext(request))
