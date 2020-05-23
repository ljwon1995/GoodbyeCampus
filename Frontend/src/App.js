import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Chat from './Chat';
import Admin from './Admin';


class App extends Component {
    render(){
        return(
            <div>
                <Route exact path='/' component={Chat}/>
                <Route path='/admin' component={Admin}/>
            </div>
        );
    }    
}

export default App;