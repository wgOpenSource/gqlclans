import React from 'react'
import { TextField, RaisedButton } from 'material-ui'
import AppBar from 'containers/AppBar'
import ClansList from 'containers/ClansList'

export default class App extends React.Component {
    state = {
        ids: ['12345', '12344', '10164'],
        value: '12345,12344,10164',
    }


    handleChange = (event) => {
        this.setState({ value: event.target.value.trim() })
    }

    handleClick = () => {
        this.setState({ ids: this.state.value.split(',') })
    }

    render() {
        return (
            <div>
                <div className="bottom-bar">
                    <AppBar />
                    <h3>Enter Clan ids, separated by comma</h3>
                    <TextField id="clan-ids-input" value={this.state.value} onChange={this.handleChange} />
                    <RaisedButton secondary onClick={this.handleClick} label="Search clans" />
                </div>
                <ClansList ids={this.state.ids} />
            </div>
        )
    }
}
