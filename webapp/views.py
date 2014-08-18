from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from forms import GetDataForm, KeywordSearchForm, SERVICE_CHOICES
from neemi.data import get_user_data, get_all_user_data
from neemi.search import simple_keyword_search
from neemi.stats import *
import time, datetime

def index(request, template='index.html'):

    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response
def indexIntro(request, template='indexIntro.html'):

    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response
	
	
def register(request, template='register.html'):
    services = SERVICE_CHOICES
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response

def search(request, template='search.html'):

    if request.method == 'POST':
        form = KeywordSearchForm(request.POST)
        if form.is_valid():
            print [form.data]
            print "GOOD DATA"
            print [form.cleaned_data]
            return simple_keyword_search(request=request,
                                         keyword=form.cleaned_data['keyword'],
                                         service=form.cleaned_data['service'])
        else:
            print "invalid form"
            dform = form
    else:
        dform = KeywordSearchForm()
        
    response = render_to_response(
    template, locals(), context_instance=RequestContext(request,{'form':dform})
        )
    return response

def query_results(request, template='results.html'):
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response

def get_data(request, template='data.html'):
    
    if request.method == 'POST':
        form = GetDataForm(request.POST)
        if form.is_valid():
            print [form.data]
            print "GOOD DATA"
            print [form.cleaned_data]
            if 'bt_search' in form.data:
                return get_all_user_data(request=request,
                                         service=form.cleaned_data['service'])
            elif 'bt_get_data_since' in form.data:
                return get_user_data(request=request,
                                     service=form.cleaned_data['service'],
                                     from_date="since_last",
                                     to_date=None,
                                     lastN=None)
            else:
                if form.cleaned_data['from_date'] != None:
                    from_date_epoch=int(time.mktime(form.cleaned_data['from_date'].timetuple()))//1*1000
                else:
                    from_date_epoch = None

                if form.cleaned_data['to_date'] != None:
                    to_date_epoch=int(time.mktime(form.cleaned_data['to_date'].timetuple()))//1*1000
                else:
                    to_date_epoch=None
        
                return get_user_data(request=request,
                                     service=form.cleaned_data['service'],
                                     from_date=from_date_epoch,
                                     to_date=to_date_epoch,
                                     lastN=form.cleaned_data['lastN'])
        else:
            print "invalid form"
            dform = form
    else:
        dform = GetDataForm()
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request,{'form':dform})
        )
    return response

def get_data_facebook(request, template='topk.html'):
    
    return get_user_data(request=request,
                                     service='facebook',
                                     from_date="since_last",
                                     to_date=None,
                                     lastN=None)    
	# elif 'bt_get_data_since' in form.data:
                # return get_user_data(request=request,
                                     # service=form.cleaned_data['service'],
                                     # from_date="since_last",
                                     # to_date=None,
                                     # lastN=None)
            # else:
                # if form.cleaned_data['from_date'] != None:
                    # from_date_epoch=int(time.mktime(form.cleaned_data['from_date'].timetuple()))//1*1000
                # else:
                    # from_date_epoch = None

                # if form.cleaned_data['to_date'] != None:
                    # to_date_epoch=int(time.mktime(form.cleaned_data['to_date'].timetuple()))//1*1000
                # else:
                    # to_date_epoch=None
        
                # return get_user_data(request=request,
                                     # service=form.cleaned_data['service'],
                                     # from_date=from_date_epoch,
                                     # to_date=to_date_epoch,
                                     # lastN=form.cleaned_data['lastN'])
        # else:
            # print "invalid form"
            # dform = form
    # else:
        # dform = GetDataForm()
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    # return response


	
	
def get_data_twitter(request, template='topk.html'):
    
    return get_user_data(request=request,
                                     service='twitter',
                                     from_date="since_last",
                                     to_date=None,
                                     lastN=None)    
	# elif 'bt_get_data_since' in form.data:
                # return get_user_data(request=request,
                                     # service=form.cleaned_data['service'],
                                     # from_date="since_last",
                                     # to_date=None,
                                     # lastN=None)
            # else:
                # if form.cleaned_data['from_date'] != None:
                    # from_date_epoch=int(time.mktime(form.cleaned_data['from_date'].timetuple()))//1*1000
                # else:
                    # from_date_epoch = None

                # if form.cleaned_data['to_date'] != None:
                    # to_date_epoch=int(time.mktime(form.cleaned_data['to_date'].timetuple()))//1*1000
                # else:
                    # to_date_epoch=None
        
                # return get_user_data(request=request,
                                     # service=form.cleaned_data['service'],
                                     # from_date=from_date_epoch,
                                     # to_date=to_date_epoch,
                                     # lastN=form.cleaned_data['lastN'])
        # else:
            # print "invalid form"
            # dform = form
    # else:
        # dform = GetDataForm()
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    # return response
	
	
	
	
	
	
def delete(request, template='delete.html'):
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response

def get_stats(request, template='stats.html'):
    if request.method == 'GET':
        stats = DBAnalysis(request)
        html_stats = stats.basic_stats()   

    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )

#    response = render_to_response(template, locals(), context_instance=RequestContext(request),#{"html_stats":html_stats})

    return response

def error(request, template='error.html'):
    message = request.GET.get('message')
    print "Message: ", message
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response


def get_topk(request, template='topk.html'):
    if request.method == 'GET':
        topk = DBTopk(request)
        top_stats = topk.top_stats()   
        k=[]
        k[0].append('Likes')
        k[1].append('Time')
        print k[0]
    response = render_to_response(
			template, locals(), context_instance=RequestContext(request)
        )

#    response = render_to_response(template, locals(), context_instance=RequestContext(request),#{"html_stats":html_stats})

    return response
def topk(request, service,template='topk.html'):
    print "auth_redirect"
    print [service]
  
    print request.user
    print request.COOKIES['sessionid']
    if service == 'facebook_status':
    	topk = DBTopkFacebook_status(request)
        top_stats = topk.top_stats()
        k=[]
        s='facebook_status'
        k.append([])
        k[0].append('Time')
        k[0].append('Likes')
        print k
	return render_to_response(template, locals(), context_instance=RequestContext(request))	
    elif service == 'facebook_link':
    	topk = DBTopkFacebook_links(request)
        top_stats = topk.top_stats()
        k=[]
        k.append([])
        s='facebook_link'
        k[0].append('Time')
        k[0].append('Likes')
        print k
	return render_to_response(template, locals(), context_instance=RequestContext(request))	
    elif service == 'facebook_albums':
    	topk = DBTopkFacebook_albums(request)
        top_stats = topk.top_stats()
        k=[]
        k.append([])
        s='facebook_albums'
        k[0].append('Time')
        k[0].append('Likes')
        print k
	return render_to_response(template, locals(), context_instance=RequestContext(request))
    elif service == 'twitter_retweets':
    	topk = DBTopkTwitter_retweets(request)
        top_stats = topk.top_stats()
        print top_stats
        k=[]
        k.append([])
        s='twitter_retweets'
        k[0].append('Time')
        k[0].append('Retweets')
        print k
	return render_to_response(template, locals(), context_instance=RequestContext(request))	

	
	
	
def compareft(request,template='compare.html'):
    print "auth_redirect"
  
    print request.user
    print request.COOKIES['sessionid']
    topk1 = DBTopkTwitter_retweets(request)
    top_stats1 = topk1.top_stats()
    print top_stats1
    k1=[]
    k1.append([])
    s='twitter_retweets'
    k1[0].append('Time')
    k1[0].append('Retweets')
    topk2 = DBTopkFacebook_status(request)
    top_stats2 = topk2.top_stats()
    k2=[]
    s='facebook_status'
    k2.append([])
    k2[0].append('Time')
    k2[0].append('Like')	
	
    print k2
    return render_to_response(template, locals(), context_instance=RequestContext(request))	

def simple(request, service,template='topk.html'):
    import random
    import django
    import datetime
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter
    print "auth_redirect"
    print [service]
  
    print request.user
    print request.COOKIES['sessionid']
    if service == 'facebook_status':
    	topk = DBTopkFacebook_status(request)
        top_stats = topk.top_stats()
    elif service == 'facebook_albums':
    	topk = DBTopkFacebook_status(request)
        top_stats = topk.top_stats()
    elif service == 'facebook_link':
    	topk = DBTopkFacebook_status(request)
        top_stats = topk.top_stats()
    elif service == 'twitter_retweets':
    	topk = DBTopkTwitter_retweets(request)
        top_stats = topk.top_stats()
    #topk = DBTopkFacebook_status(request)
    #top_stats = topk.top_stats()
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    #now=datetime.datetime.now()
    #delta=datetime.timedelta(days=1)
    for i in top_stats:
        x.append(i)
        y.append(top_stats[i])
    print x
    print y
    ax.bar(x,y,width=0.1)
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    #fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response