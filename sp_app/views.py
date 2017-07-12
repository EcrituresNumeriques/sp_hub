from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

BASEX_API_URL = "http://basex.ecrituresnumeriques.ca:8984"
BASEX_API_PATH = "/sph/tim"

def display(request, docid):
    my_url = BASEX_API_URL + BASEX_API_PATH + "/articles/view/" + docid.__str__()
    r = requests.get(my_url)

    if r.status_code == 200:
        data = r.content

    return render(request, 'articles/display.html', { 'article': data })


def list_articles(request):
    my_url = BASEX_API_URL + BASEX_API_PATH + "/articles/list"
    r = requests.get(my_url)

    if r.status_code == 200:
        data = json.loads(r.content)

    return render(request, 'articles/list.html', { 'articles': data, 'source_url': my_url})
