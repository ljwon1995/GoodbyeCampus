import React, { Component } from 'react';
import { Widget, addResponseMessage, toggleWidget } from 'react-chat-widget';

import './App.css';

class App extends Component {

  componentDidMount() {
    addResponseMessage("환영합니다!!!asdfasdf");

  }

  async handleNewUserMessage (newMessage) {
    


    try {
            const res = await fetch('http://127.0.0.1:8000/message/' + newMessage);
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