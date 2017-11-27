import React from 'react'
import { graphql, compose } from 'react-apollo'
import { connect } from 'react-redux'
import gql from 'graphql-tag'

import AppBar from 'components/AppBar'

const mapStateToProps = (state) => ({
    limit: state.settings.serversInfoLimit,
})

export const query = gql`    
    query serversInfo($limit: Int) {
        servers(limit: $limit) {
            ...AppBar_ServerInfo
        }
    }
`

const options = {
    options: ({ limit }) => ({
        variables: { limit }
    })
}

export default compose(connect(mapStateToProps), graphql(query, options))(AppBar)
