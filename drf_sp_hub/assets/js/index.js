import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter } from 'react-router-dom'

import Typography from 'material-ui/Typography'

import SpAppBar from './sp_appbar'
import SpCardList from './sp_cards'

function SpApp() {
    return (
        <div>
            <SpAppBar />
        </div>
    );
}

render(<BrowserRouter><SpApp /></BrowserRouter>, document.getElementById('container'))
