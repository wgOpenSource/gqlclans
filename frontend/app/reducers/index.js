import { combineReducers } from 'redux'
import clans from 'reducers/Clans'

export default combineReducers({
    clans,
    settings: (state = {}) => state,
})
