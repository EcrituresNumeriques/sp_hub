module namespace page = 'http://basex.org/modules/web-page';
declare default function namespace 'local' ;
(: import module namespace functx = "http://www.functx.com"; :)

declare
  %rest:path("/sph/tim/articles/list")
  %rest:GET
  %output:method("json")
  function page:getAllArticles() {
    let $nodes := db:open("sph")
    return <json type='array'>{
    for $node in $nodes
      return <_ type='object'>
        <id>{fn:substring-after(fn:document-uri($node), 'sph/')}</id>
        <name>{fn:data($node/html/head/meta[@name="DC.title"]/@content)}</name>
    </_>
    }</json>

  };

declare
  %rest:path("/sph/tim/articles/view/{$idDocument}")
  %rest:GET
  %output:method("xml")
  function page:getRawTim($idDocument as xs:string) {
    let $document := db:open("sph", $idDocument)/html/body/*
    return $document

  };

declare
  %rest:path("/sph/tim/keywords/{$keyw}")
  %rest:GET
  %output:method("json")
  function page:getArticlesByKeywords($keyw as xs:string) {
    let $nodes := db:open("sph")
    return <json type='array'>{
    for $node in $nodes[//meta[@name="keywords" and fn:contains(@content, $keyw)]]
      return <_ type='object'>
        <id>{fn:substring-after(fn:document-uri($node), 'sph/')}</id>
        <name>{fn:data($node/html/head/meta[@name="DC.title"]/@content)}</name>
    </_>
    }</json>
  }
  
  
 