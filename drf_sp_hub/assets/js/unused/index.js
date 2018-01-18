import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom'

import SpApp from './sp_app'
import Articles, { Article } from './sp_articles'

render (
  <BrowserRouter>
    <Route path='/' component={SpApp}>
      <Route path="/articles" component={Articles}>
        <Route path="/articles/:articleId" title='test' component={Article} />
      </Route>
    </Route>
  </BrowserRouter>
  , document.getElementById('container'))
