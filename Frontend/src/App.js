import React, { Component } from 'react';
import { Widget, addResponseMessage, toggleWidget } from 'react-chat-widget';

import './App.css';

class App extends Component {

  async componentDidMount() {

    try {
            const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/message/start');
            const posts = await res.json();
            
            addResponseMessage(posts.content);
          
        } catch (e) {
            console.log(e);
    }
  }

  async handleNewUserMessage (newMessage) {
    


    try {
            const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/message/' + newMessage);
            const posts = await res.json();
            
            addResponseMessage(posts.content);
          
        } catch (e) {
            console.log(e);
    }
    
  }



  render() {
    toggleWidget()    

    return (
      <div className="App">
        <Widget
         handleNewUserMessage={this.handleNewUserMessage}
         fullScreenMode={true}
         //fullScreenMode={true}
         />
      </div>
    );
  }
}

export default App;
