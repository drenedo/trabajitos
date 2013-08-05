# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,render
from django.db.models import Q
from django.core import serializers
from django.db.models.query import QuerySet
from django.utils.functional import curry

from json import dumps, loads, JSONEncoder

from trabajitos.apps.user.models import Search, Find, Job
from trabajitos.apps.user.vmodels import ViewFind,MyEncoder

from models import Search


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def errorlogin(request,msg):
    return render_to_response('home.html', {'errors': msg})


def loginu(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return home(request)
        else:
            msg = []
            msg.append("User error")
            return errorlogin(request,msg)
    else:
        msg = []
        msg.append("User error")
        return errorlogin(request,msg)
    
def logoutu(request):
    logout(request)
    return index(request)
    
    
@login_required
def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request)
    finds = Find.objects.order_by('-date','-time')[0:20]
    request.session['finds'] = finds
    return render(request,'home.html',{'finds':finds})

@login_required
def addfind(request):
    words = request.POST['words']
    provinces = request.POST['provinces']
    non = request.POST['non']
    locations = request.POST['locations']
    if words and provinces:
        search = Search(provinces=provinces,words=words,user=request.user,non=non,locations=locations)
        search.save()
    return home(request)

@login_required
def mysearchs(request):
    searchs = Search.objects.filter(Q(user=request.user))
    data = serializers.serialize('json', searchs)
    return HttpResponse(data, mimetype='application/json')


@login_required
def myfinds(request):
    searchs = Search.objects.filter(Q(user=request.user))
    finds = Find.objects.all().filter(search_id__in=searchs).order_by('-date','-time')[0:40]
    views = []
    for find in finds:
        for search in searchs:
            if search.id == find.search.id :
                views.append(ViewFind(search=search,find=find))
                #find.search = search
                break
        
    
    data = dumps(views, cls=MyEncoder)
    #data = serializers.serialize('json', finds)
    return HttpResponse(data, mimetype='application/json')

@login_required
def myjobs(request, id=None):
    if id:
        tries = Job.objects.filter(Q(find=id)&Q(user=request.user))
        data = serializers.serialize('json', tries)
        
    return HttpResponse(data, mimetype='application/json')
