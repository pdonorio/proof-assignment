import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { AppContainer } from 'react-hot-loader';
import DateFnsUtils from 'material-ui-pickers/utils/date-fns-utils';
import MuiPickersUtilsProvider from 'material-ui-pickers/utils/MuiPickersUtilsProvider';
import { MuiThemeProvider } from '@material-ui/core/styles';
import 'typeface-roboto';

import App from './App';
import store from './store';
import theme from './theme';
import './index.css';

const root = document.getElementById('root');
const load = () => render(
  (
    <Provider store={store}>
      <AppContainer>
        <MuiThemeProvider theme={theme}>
          <MuiPickersUtilsProvider utils={DateFnsUtils}>
            <App />
          </MuiPickersUtilsProvider>
        </MuiThemeProvider>
      </AppContainer>
    </Provider>
  ), root,
);

// This is needed for Hot Module Replacement
if (module.hot) {
  module.hot.accept('./App', load);
}

load();
