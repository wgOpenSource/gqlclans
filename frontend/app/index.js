import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import thunkMiddleware from 'redux-thunk'
import { ApolloProvider } from 'react-apollo'
import { createStore, applyMiddleware, compose } from 'redux'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import App from 'components/App'
import client from 'client'
import settings from 'settings'
import rootReducer from 'reducers'

import 'stylesheets/styles.scss'

const enhancer = compose(applyMiddleware(thunkMiddleware))
const store = createStore(rootReducer, { settings }, enhancer)

const app = (store) => (
    <Provider store={store}>
        <ApolloProvider client={client}>
            <MuiThemeProvider>
                <App />
            </MuiThemeProvider>
        </ApolloProvider>
    </Provider>
)

ReactDOM.render(
    app(store),
    document.getElementById('app'),
)
