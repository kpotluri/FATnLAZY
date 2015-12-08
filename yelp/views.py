from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.template.loader import get_template

from django.shortcuts import render

from .forms import YelpForm

from django.http import JsonResponse

import os
import rauth

import json

import django_tables2 as tables


class ResultsTable(tables.Table):
    name = tables.Column()
    address = tables.Column()
    phone = tables.Column()
    url = tables.Column()
    rating = tables.Column()
    distance = tables.Column()
    business_long = tables.Column()
    business_lat = tables.Column()

# Create your views here.
def uber_map(request):
    return render(request, 'uber-map.html')

def index(request):
    return HttpResponse("<b>Yelp Results Page!<b>")

def get_search_parameters(lat,long, keyword='restaurant', radius="2000", results_limit="5"):
    #See the Yelp API for more details
    params = {}
    #params["term"] = "restaurant"
    params["term"] = keyword
    params["ll"] = "{},{}".format(str(lat),str(long))
    params["radius_filter"] = radius
    params["limit"] = results_limit
    return params

def call_yelp_api(params):

    # retrieve envronmental variables
    consumer_key = os.environ['YELP_CONSUMER_KEY']
    consumer_secret = os.environ['YELP_CONSUMER_SECRET']
    token = os.environ['YELP_TOKEN']
    token_secret = os.environ['YELP_TOKEN_SECRET']

    # establish session
    # note: need to configure web server with environmental variables
    session = rauth.OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = token,
        access_token_secret = token_secret)

    # send request to Yelp API
    request = session.get("http://api.yelp.com/v2/search", params=params)

    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()

    return data

def get_results(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YelpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            if not request.POST.get('num_results', ''):
                num_results = 1
            else:
                num_results = request.POST['num_results']

            if not request.POST.get('keyword', ''):
                params = get_search_parameters(37.8717,-122.2728, results_limit=num_results) # initially, user's location is hardcoded to Berkeley
            else:
                # pass-in user's keyword in form, if entered
                params = get_search_parameters(37.8717,-122.2728, request.POST['keyword'], results_limit=num_results) # initially, user's location is hardcoded to Berkeley

            # retrieve results
            results = call_yelp_api(params)
            #print(results)

            # extract resultsname'] = yelp_listing['name']
            businesses = results['businesses']
            yelp_result_set = []

            for business in businesses:
                business_result = {}
                business_result['name'] = business['name']
                business_result['address'] = business['location']['address'][0]
                business_result['phone'] = business['phone']
                business_result['url'] = business['url']
                business_result['rating'] = business['rating']
                business_result['distance'] = business['distance']
                business_result['business_long'] = business['location']['coordinate']['longitude']
                business_result['business_lat'] = business['location']['coordinate']['latitude']
                yelp_result_set.append(business_result)

            # render HTML page:
            return render(request, 'yelp-results.html', {'form': form, 'table':ResultsTable(yelp_result_set) })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = YelpForm()
        params = get_search_parameters(37.8717,-122.2728) # initially, user's location is hardcoded to Berkeley
        #print(params)
        results = call_yelp_api(params)

    return render(request, 'yelp-results.html', {'form': form, 'table':ResultsTable({})})
