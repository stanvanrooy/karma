import React from 'react';
import {initializeIcons} from '@fluentui/react';
import ReactDOM from 'react-dom';
import { App } from './App';

initializeIcons();

ReactDOM.render(<App />, document.getElementById('root'));

