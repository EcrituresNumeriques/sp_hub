import React from 'react';

import Typography from 'material-ui/Typography';
import Card, {CardActions, CardHeader, CardContent} from 'material-ui/Card';
import Button from 'material-ui/Button';

export default class SpCardList extends React.Component {
    // define state in constructor (ES6)
    constructor(props) {
        super(props);
        this.state = { data: [] };
    }

    render() {
        if(this.state.data) {
            var myItems = this.state.data.map(function(item) {
                console.log(item);
                return <SpCard
                    title={item.title}
                    description={item.description}
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

export class SpCard extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Card>
                <CardHeader title={this.props.title} subheader={this.props.created_by} />
                <CardContent>
                    <Typography component="p">
                        {this.props.description ? this.props.description : 'vide'}
                    </Typography>
                </CardContent>
                <CardActions>
                  <Button label="Action1" />
                  <Button label="Action2" />
                </CardActions>
            </Card>
        );
    }
}
