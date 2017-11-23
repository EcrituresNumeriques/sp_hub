import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom'

import SpApp from './sp_app'
import SpCardList, { SpCard } from './sp_cards'
import SpArticles from './sp_articles'

render (
  <BrowserRouter>
    <SpApp>
      <Route path="/articles" component={SpArticles} />
      <Route path="/conversations" render={()=><SpCardList url='http://localhost:8080/api/conversations/' />}/>
    </SpApp>
  </BrowserRouter>
  , document.getElementById('container'))
