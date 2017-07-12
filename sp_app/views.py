"""
declare
  %rest:path("/sph/tim/titles")
  %rest:GET
  %output:method("json")
  function page:getTitlesTim() {
    let $sph := db:open("sph")//*:html
    return <json type='array'> {
    for $title in $sph/head/meta[@name="DC.title"]
      return <_ type='object'><name>{fn:data($title/@content)}</name></_>
    }</json>

  };

declare
  %rest:path("/sph/tim/authors")
  %rest:GET
  %output:method("json")
  function page:getAuthorsTim() {
    let $authors := db:open("sph")//meta[@name="DC.creator"]
    let $authors := fn:distinct-values($authors/@content)

    return <json type='array'> {
      for $author in $authors
        return <_ type='object'><name>{$author}</name></_>
    }</json>
  };

"""

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
