import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import All from './All';
import Substitute from './Substitute';
import Requirement from './Requirement';

class System extends Component{

    constructor(props) {
        super(props);
        this.state = {
            value: 0
        };
    }

    handleChange = (event, newValue) => {
        this.setState({
            value: newValue
        })
    }

    render(){
        var content = null;
        if(this.state.value === 0) {
            content = <All/>
        }
        else if(this.state.value === 1) {
            content = <Substitute/>
        }
       // else {
           // content = <Requirement/>
        //}
        return(
            <div>
                <AppBar position="static">
                    <Tabs value={this.state.value} onChange={this.handleChange} style={{'alignSelf' : 'center'}}>
                        <Tab label="전체 과목"/>
                        <Tab label="대체 과목"/>
                    </Tabs>
                </AppBar>
                <div>{content}</div>
            </div>
        );
    }
}

export default System;
