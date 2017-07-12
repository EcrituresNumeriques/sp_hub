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
import requests
import json

def list_titles(request, action):
    my_url = "http://basex.ecrituresnumeriques.ca:8984/sph/tim/" + action
    r = requests.get(my_url)
    print(r.content.decode("utf-8"))
    if r.status_code == 200:
        data = json.loads(r.content)

    return render(request, 'list.html', { 'objects_list': data, 'source_url': my_url})
