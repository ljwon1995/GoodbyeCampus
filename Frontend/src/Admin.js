import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import './Admin.css';
import System from './System';

class Admin extends Component {
  
  constructor(props) {
    super(props);

    this.state = {
      mode: true,
      userId: '',
      userPw: '',
    };
  }

  _idhandler = e =>{
    e.preventDefault();
    this.setState({
    userId: e.target.value    
    })
  }

  _pwhandler = e=>{
    e.preventDefault();
    this.setState({
    userPw: e.target.value
})    
  }


  _pagehandler = e => {
    e.preventDefault();

    if(this.state.userId === '' || this.state.userPw === ''){
      alert('아이디, 비번을 확인해주세요');
    }

    else if(this.state.userId === 'admin' && this.state.userPw === 'admin') {
      if(this.state.mode===true) {
        this.setState({
          mode: false
        })
      }
    }
    else{
      alert('비번틀림');
    }

  }

  render() {

    if(this.state.mode === true){
      return(
          <div className='Container'>
            <div className='Container-Head'>
              <h1>GoodbyeCampus</h1>
            </div>
            <div className='Container-Body'>
              <TextField placeholder='아이디를 입력해주세요..' type='id' onChange={this._idhandler}/><br/>
              <TextField placeholder='비밀번호를 입력해주세요..' type='password' style={{'marginTop' : '15px'}} onChange={this._pwhandler}/><br/>
              <Button variant="contained" color="primary" size='large' style={{'marginTop':'20px'}} onClick={this._pagehandler}>확인</Button>
            </div>
          </div>
      );
    }
    else{
      return(
        <div>
          <System/>
        </div>
      );
      
    }
  }
}


export default Admin;