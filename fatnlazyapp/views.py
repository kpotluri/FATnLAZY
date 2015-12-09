from django.shortcuts import render

from django.http import HttpResponse
from .forms import GoogleForm


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # return render(request, 'index.html')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
    	# create a form instance and populate it with data from the request:
        form = GoogleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            return render(request, 'index.html', {'form': form })
        else:
        	print('Invalid entry!')
    else:
        form = GoogleForm()
        # params = get_search_parameters(37.8717,-122.2728) # initially, user's location is hardcoded to Berkeley
        # #print(params)
        # results = call_yelp_api(params)

    return render(request, 'index.html', {'form': form})

def currentlocation(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'map_search.html')
