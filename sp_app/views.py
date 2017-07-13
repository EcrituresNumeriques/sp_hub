from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
import requests
import json

BASEX_API_URL = "http://basex.ecrituresnumeriques.ca:8984"
BASEX_API_PATH = "/sph/tim"

HYPOTHESIS_API_URL = "https://hypothes.is/api"

def display(request, docid):
    data = ''
    my_url = BASEX_API_URL + BASEX_API_PATH + "/articles/view/" + docid.__str__()
    r_basex = requests.get(my_url)

    if r_basex.status_code == 200:
        data = r_basex.content
        
    """ Look for annotations in hypothes.is """
    my_url = HYPOTHESIS_API_URL + "/search?uri=" + request.build_absolute_uri()
    r_hypothesis = requests.get(my_url)
    
    if r_hypothesis.status_code == 200:
        annotations = json.loads(r_hypothesis.content)
        print(annotations['rows'])
        
    return render(request, 'articles/display.html', { 'article': data, 'annotations': annotations['rows'] })


def list_articles(request):
    my_url = BASEX_API_URL + BASEX_API_PATH + "/articles/list"
    r = requests.get(my_url)

    if r.status_code == 200:
        data = json.loads(r.content)

    return render(request, 'articles/list.html', { 'articles': data, 'source_url': my_url})
