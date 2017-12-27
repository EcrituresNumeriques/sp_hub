import React from 'react';

import Typography from 'material-ui/Typography';
import Card, {CardActions, CardHeader, CardContent} from 'material-ui/Card';

export default class SpArticles extends React.Component {
  // define state in constructor (ES6)
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  render() {
    if(this.state.data) {
      var output = this.state.data.map(function(item) {
        return <Article title={item.title} articleId={item.id}>{item.title}</Article>;
      });
    }
    return (
      <div>
        <h2>Articles</h2>
        {output}
      </div>
    )
  }

  componentDidMount() {
    $.ajax({
      url: '/api/articles/',
      datatype: 'json',
      cache: false,
      success: (data) => {
        this.setState({data: data});
      }
    });
  }
}

export class Article extends React.Component {
  render() {
    return (
      <div>
        <h3>{this.props.params.title}</h3>
      </div>
    )
  }
}
