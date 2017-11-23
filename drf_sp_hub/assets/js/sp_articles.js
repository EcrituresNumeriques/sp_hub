import React from 'react';

import Typography from 'material-ui/Typography';
import Card, {CardActions, CardHeader, CardContent} from 'material-ui/Card';
import Button from 'material-ui/Button';

import SpCardList, { SpCard } from './sp_cards'

export default class SpArticles extends React.Component {
  // define state in constructor (ES6)
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  render() {
    if(this.props.match.isExact && this.state.data) {
      var output = this.state.data.map(function(item) {
        return <SpCard
          article_id={item.id}
          title={item.title}
          description={item.description}
          url={item.url}
        />;
      });
    } else {
      output = <SpCard url={{"/articles/" + {this.props.url}}}/>;
    }
    return (
      <div>{output}</div>
    )
  }

  componentDidMount() {
    $.ajax({
      url: "http://localhost:8080/api/articles/",
      datatype: 'json',
      cache: false,
      success: (data) => {
        this.setState({data: data});
      }
    });
  }
}
