import React from 'react';
import { withStyles } from 'material-ui/styles';

import Link from 'react-router-dom/Link';

import Button from 'material-ui/Button';

class SpHeader extends React.Component {
  render() {
    return(
      <div>
        <Button component={Link}
          to='/articles'
        >
          Articles
        </Button>
        <Button component={Link}
          to='/conversations'
        >
          Conversations
        </Button>
      </div>
    );
  }
}

export { SpHeader };
