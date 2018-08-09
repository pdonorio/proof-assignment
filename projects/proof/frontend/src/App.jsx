import React from 'react';
import { PropTypes } from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { BrowserRouter, Route } from 'react-router-dom';
import Quizzes from './containers/Quizzes';
import Navbar from './components/Navbar';
import NewQuiz from './containers/NewQuiz';

const styles = theme => ({
  wrapper: {
    backgroundColor: theme.palette.tertiary.main,
    height: '100vh',
  },
});

const App = ({ classes }) => (
  <BrowserRouter>
    <div className={classes.wrapper}>
      <Navbar />
      <Route exact path="/" component={Quizzes} />
      <Route exact path="/quizzes" component={Quizzes} />
      <Route exact path="/quizzes/new" component={NewQuiz} />
    </div>
  </BrowserRouter>
);

App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);
