import React from 'react';

import Typography from 'material-ui/Typography';
import Card, {CardActions, CardHeader, CardContent} from 'material-ui/Card';
import Button from 'material-ui/Button';

import { Link } from 'react-router-dom'

export default class SpCardList extends React.Component {
  // define state in constructor (ES6)
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  render() {
    if(this.state.data) {
      var myItems = this.state.data.map(function(item) {
        return <SpCard
          article_id={item.created_by}
          title={item.title}
          description={item.description}
          url={item.url}
        />;
      });
    }
    return (
      <div>{myItems}</div>
    )
  }

  componentDidMount() {
    $.ajax({
      url: this.props.url,
      datatype: 'json',
      cache: false,
      success: (data) => {
        this.setState({data: data});
      }
    });
  }
}

class SpCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  componentDidMount() {
    if(this.props.url) {
      $.ajax({
        url: this.props.url,
        datatype: 'json',
        cache: false,
        success: (data) => {
          this.setState({data: data});
        }
      });
    }
  }

  render() {
    return (
      <Card>
        <CardHeader title={this.state.data.title} subheader={this.state.data.created_by} />
        <CardContent>
          <Button>{this.state.data.title}</Button>
          <Typography component="p">
            {this.state.data.description ? this.state.data.description : 'vide'}
          </Typography>
        </CardContent>
        <CardActions>
          <Button label="Action1">Action1</Button>
          <Button label="Action2">Action2</Button>
        </CardActions>
      </Card>
    );
  }
}

export { SpCard };
