import React from 'react';
import ReactDOM from 'react-dom';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'm  aterial-ui/styles/getMuiTheme';

import AppBar from 'material-ui/AppBar';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';

class SpConversationsCardList extends React.Component {
    // define state in constructor (ES6)
    constructor(props) {
        super(props);
        this.state = { data: [] };
    }

    render() {
        if(this.state.data) {
            console.log('We have data!');
            var articlesItems = this.state.data.map(function(article) {
                console.log(article);
                return <SpArticleCard
                    title={article.title}
                    created_by={article.created_by}
                />;
            });
        }
        return (
            <div>{articlesItems}</div>
        )
    }

    componentDidMount() {
        $.ajax({
            url: 'http://localhost:8080/api/articles/',
            datatype: 'json',
            cache: false,
            success: (data) => {
                this.setState({data: data});
                console.log(data);
            }
        });
    }
}

class SpArticleCard extends React.Component {
    constructor(props) {
        super(props);
        this.title = this.props.title;
        console.log(this.state);
    }

    render() {
        return(
            <Card>
                <CardHeader
                  title={this.props.title}
                  subtitle={this.props.created_by}
                  actAsExpander={true}
                  showExpandableButton={true}
                />
                <CardTitle title={this.title} subtitle={this.props.created_by} />
                <CardText>
                  Là on va charger en AJAX.
                </CardText>
                <CardActions>
                  <FlatButton label="Action1" />
                  <FlatButton label="Action2" />
                </CardActions>
            </Card>
        );
    }
}

export default class Hello extends React.Component {
    render() {
        return (
            <MuiThemeProvider muiTheme={getMuiTheme()}>
              <div>
                <SpAppBar />
                <SpArticleCardList />
              </div>
            </MuiThemeProvider>
        )
    }
}

ReactDOM.render(<Hello />, document.getElementById('container'))
