import React from 'react'
import { AppBar as AppBarMaterial, List, ListItem } from 'material-ui'
import './styles.scss'


export default class AppBar extends React.Component {
    static propTypes = {
        data: React.PropTypes.shape({
            servers: React.PropTypes.arrayOf(React.PropTypes.shape({
                server: React.PropTypes.string,
                playersOnline: React.PropTypes.number,
            })),
            loading: React.PropTypes.bool,
        })
    }

    renderServers() {
        return !this.props.data.loading && this.props.data.servers ? (
            <List>
                {this.props.data.servers.map((info) => (
                    <ListItem
                        leftIcon={<span className="serverInfoID">[{info.server}]</span>}
                        primaryText={info.playersOnline}
                        key={`server-info-${info.server}`}
                    />
                ))}
            </List>
        ) : null
    }

    render() {
        return (
            <AppBarMaterial title="Wargaming Open Source" iconElementRight={this.renderServers()} />
        )
    }
}
