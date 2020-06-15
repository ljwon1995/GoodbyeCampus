import React, { Component } from 'react';
import { Widget, addResponseMessage, toggleWidget} from 'react-chat-widget';
import './Chat.css';
import { TextField } from '@material-ui/core';
import { Dialog, DialogTitle, DialogActions, DialogContent, Button} from '@material-ui/core'

class Chat extends Component {

  constructor(props) {
    super(props);

    this.state = {
      open : false
    };

    toggleWidget();

  }

  user = "";
  userId = "";
  userPw = "";
  idList = [];
  flag = false;



  

  _closeBtn() {
  this.setState({
    open: false
    });
    this.userId = "";
    this.userPw = "";
  }


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

  async componentWillUnmount(){
	 window.addEventListener("beforeunload", (event)=>{
        fetch("http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/refresh",{
            method: 'post',
            body: JSON.stringify({
                data: this.idList
            })
        })
    })




  }

  async componentDidMount() {

  window.addEventListener("beforeunload", (event)=>{
        fetch("http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/refresh",{
            method: 'post',
            body: JSON.stringify({
                data: this.idList
            })
        })
    })


    this.user = this._randomUser();
    

    try {
	    var startTime;
	    startTime = new Date();
            const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/message/start$'+ this.user);
            const posts = await res.json();
	    
	    var str = posts.content
	    str = str.replace(/\n/g,'\n\n')
	    addResponseMessage(str);
	    
	    var endTime;
	    endTime = new Date();
	    var timeDiff = endTime - startTime; //in ms
	    timeDiff /= 1000;
	    addResponseMessage(timeDiff.toString());
          
        } 
    catch (e) {
      console.log(e);
    }
  }

  async handleNewUserMessage (newMessage) {

    if(this.flag === true) {
        this.idList.push(newMessage);
    }

    if(newMessage === 'open') {
      this.setState({
        open : true
      })
    } 
    
    if(newMessage === ':test') {
	try {
		var startTime;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/start');
    		const posts = await res.json()
	   	 
		addResponseMessage(posts.content);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/anal');
    		const posts = await res.json()
	    
		addResponseMessage(posts.content);


		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/makingStudent');
    		const posts = await res.json()
	    	
		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);


		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/totalCredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);


		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());


	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/exclusiveGECredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);


		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/BSMCredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);


		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());


	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/coreGECredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());


	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/majorCredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/majorBasicCredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/majorCompulsoryCredits');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/avgGrade');
    		const posts = await res.json()
		
		
		var str = posts.content
		if (str !== ""){    
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
		}
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/compulsoryNotTaken');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/machGE');
    		const posts = await res.json()

		var str = posts.content
		if (str !== "") {
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
		}
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/machPrac');
    		const posts = await res.json()

		var str = posts.content
		if (str !== "") {
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
		}
	}
	catch (e){
    		console.log(e)
	}

	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/test/others');
    		const posts = await res.json()

		    var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
	}
	catch (e){
    		console.log(e)
	}


	
    } else {

    	try {
		var startTIme;
		startTime = new Date();
    		const res = await fetch('http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/message/notfirst$' + this.user + "$" + newMessage);
    		const posts = await res.json();
            var str = posts.content
		    str = str.replace(/\n/g,'\n\n')
		    if(str === '중앙대학교 포탈 패스워드, 아이디가 필요합니다. 아이디를 입력 해 주세요') {
                this.flag = true;
            }
            else {
                this.flag = false;
            }
    		addResponseMessage(str);
		var endTime;
		endTime = new Date();
		var timeDiff = endTime - startTime; //in ms
		timeDiff /= 1000;
		addResponseMessage(timeDiff.toString());
    	} 
    	catch (e) {
      		console.log(e);
    	}    

    }
  }

  render() {

    return (
      <div className="App">
        <Widget
         handleNewUserMessage={this.handleNewUserMessage.bind(this)}
         fullScreenMode={true}
         showCloseButton={false}
         title="Goodbye Campus"
         subtitle="당신의 졸업 도우미"/>
        <Dialog open={this.state.open} onClose={this._closeBtn.bind(this)}>
          <DialogTitle style={{"textAlign":"center"}}>로그인</DialogTitle>
            <DialogContent style={{"textAlign":"center"}}>
              <TextField label="아이디" type="text" onChange={(event)=>{
                this.userId = event.target.value;
              }}></TextField><br/> 
              <TextField label="비밀번호" type="password" name="userPw" onChange={(event)=>{
                this.userPw = event.target.value;
              }}></TextField><br/>                         
            </DialogContent>
            <DialogActions>
              <Button variant="contained" color="primary" onClick={()=>{
                console.log(this.userId, this.userPw);
                this.setState({
                  open : false
                })
                this.userId = "";
                this.userPw = "";
                }}>확인</Button>
              <Button variant="outlined" color="primary" onClick={this._closeBtn.bind(this)}>취소</Button>
            </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default Chat;
