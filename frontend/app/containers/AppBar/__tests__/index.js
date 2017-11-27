import React from 'react'
import { query } from '../'

it('has a known query shape', () => {
    expect(query).toMatchSnapshot();
})
