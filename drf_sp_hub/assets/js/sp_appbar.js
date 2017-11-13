import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';

import Link from 'react-router-dom/Link';

import Typography from 'material-ui/Typography';

import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Drawer from 'material-ui/Drawer';
import Button from 'material-ui/Button';
import IconButton from 'material-ui/IconButton';
import List, { ListItem, ListItemText } from 'material-ui/List';
import Divider from 'material-ui/Divider';


import MenuIcon from 'material-ui-icons/Menu';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import ChevronRightIcon from 'material-ui-icons/ChevronRight';

const drawerWidth = 240;

const styles = theme => ({
  root: {
    width: '100%',
    height: 430,
    marginTop: theme.spacing.unit * 3,
    zIndex: 1,
    overflow: 'hidden',
  },
  appFrame: {
    position: 'relative',
    display: 'flex',
    width: '100%',
    height: '100%',
  },
  appBar: {
    position: 'absolute',
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 20,
  },
  hide: {
    display: 'none',
  },
  drawerPaper: {
    position: 'relative',
    height: '100%',
    width: drawerWidth,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
  },
  flex: {
    flex: 1,
  },
  content: {
    width: '100%',
    marginLeft: -drawerWidth,
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    height: 'calc(100% - 56px)',
    marginTop: 56,
    [theme.breakpoints.up('sm')]: {
      content: {
        height: 'calc(100% - 64px)',
        marginTop: 64,
      },
    },
  },
  contentShift: {
    marginLeft: 0,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
});

class SpAppBar extends React.Component {
  constructor() {
    super();

    this.state = { open: false };
    this.handleDrawerOpen = () => {
        this.setState({ open: true });
    };
    this.handleDrawerClose = () => {
      this.setState({ open: false });
    }
  }

  render() {
    const { classes, theme } = this.props;

    return (
      <div className={classes.root}>
        <div className={classes.appFrame}>
          <AppBar className={classNames(classes.appBar, this.state.open && classes.appBarShift)}>
            <Toolbar>
              <IconButton
                color="contrast"
                onClick={this.handleDrawerOpen}
                className={classNames(classes.menuButton, this.state.open && classes.hide)}
                aria-label="Menu"
              >
                <MenuIcon />
              </IconButton>
              <Typography type="title" color="inherit" className={classes.flex}>
                Sens Public
              </Typography>
              <Button color="contrast">Login</Button>
            </Toolbar>
          </AppBar>
          <Drawer
            type="persistent"
            classes={{paper: classes.drawerPaper}}
            open={this.state.open}
          >
            <div className={classes.drawerInner}>
              <div className={classes.drawerHeader}>
                <IconButton onClick={this.handleDrawerClose}>
                  {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                </IconButton>
              </div>
              <Divider />
              <List className={classes.list}>
                <ListItem button>
                  <Button
                    component={Link}
                    className={classes.button}
                    to="/articles"
                  >
                    Articles
                  </Button>
                </ListItem>
                <ListItem button>
                  <ListItemText primary="Conversations" />
                </ListItem>
              </List>
            </div>
          </Drawer>
        </div>
      </div>
    );
  }
}

SpAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(SpAppBar);
