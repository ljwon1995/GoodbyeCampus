import React, { Component } from 'react';
import { Widget, addResponseMessage, toggleWidget } from 'react-chat-widget';
import './Chat.css';

class Chat extends Component {

  user = '';

  _randomUser() {
    var data1 = String(Math.floor(Math.random()*100000)+1);
    var data2 = String(Math.floor(Math.random()*100000)+1);
    var data3 = String(Math.floor(Math.random()*100000)+1);
    var data4 = String(Math.floor(Math.random()*100000)+1);
    console.log(data1);
    console.log(data2);
    console.log(data3);
    console.log(data4);

    var result = data1+data2+data3+data4;

    return result;
  }

  async componentDidMount() {

    this.user = this._randomUser();

    try {
            const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/message/start');
            const posts = await res.json();
            
            addResponseMessage(posts.content);
          
        } 
    catch (e) {
      console.log(e);
    }
  }

  async handleNewUserMessage (newMessage) {

    try {
      const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/message/' + newMessage);
      const posts = await res.json();
            
      addResponseMessage(posts.content);
          
    } 
    catch (e) {
      console.log(e);
    }    
  }

  render() {

    toggleWidget();

    return (
      <div className="App">
        <Widget
         handleNewUserMessage={this.handleNewUserMessage.bind(this)}
         fullScreenMode={true}
         showCloseButton={false}
         title="Goodbye Campus"
         subtitle="당신의 졸업 도우미"/>
      </div>
    );
  }
}

export default Chat;