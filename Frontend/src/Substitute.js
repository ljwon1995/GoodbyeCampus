import React, {Component} from 'react';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import {DialogTitle, TextField, DialogActions} from '@material-ui/core';
import DialogContent from '@material-ui/core/DialogContent';
import RadioGroup from '@material-ui/core/RadioGroup';
import Radio from '@material-ui/core/Radio';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';

class Substitute extends Component {
    
    constructor(props){
        super(props);

        this.state = {
         subject: [],
         options: [],
         open: false,
         oldCode: '',
         oldNm: '',
         newCode: '',
         newNm: '',
         mode : "과목명",
         search: "",
         label : {
             "과목명" : "과목명",
             "과목코드" : "과목코드"
         }
        };
    }

    _inputData(e) {
        let nextState = {};

        nextState[e.target.name] = e.target.value;
        
        this.setState(nextState);
    }

    _btnClick() {
        this.setState({
            open: true
        })
    }

    _closeBtn = () => {
        this.setState({
            oldCode: '',
            oldNm: '',
            newCode: '',
            newNm: '',
            open: false
        })
    }

    _modeChange = (event) => {
        this.setState({
            mode : event.target.value
        })
    }

    render(){

        let content = null;

        if(this.state.subject.length === 0) {
            content = <div style = {{"textAlign" : "center", "marginTop" : "160px"}}>검색결과가 없습니다.</div>
        }
        return(
            <div>
                <div style={{"textAlign":"center", "marginTop":"15px"}}>
                    <FormControl component="fieldset">
                        <RadioGroup value={this.state.mode} row aria-label="position" onChange={this._modeChange}>
                            <FormControlLabel
                            value="과목명"
                            control={<Radio color="primary" />}
                            label="과목명"
                            />
                            <FormControlLabel
                            style={{"marginLeft":'20px'}}
                            value="과목코드"
                            control={<Radio color="primary" />}
                            label="과목코드"
                            />
                        </RadioGroup>               
                    </FormControl>
                    <TextField value={this.state.search} variant="outlined" style={{"marginLeft":'20px', "width":"4cm"}} size="small" label={this.state.label[this.state.mode]} type="text" name="search" onChange={this._inputData.bind(this)}></TextField>
                    <Button variant="contained" color="primary" size="large" style={{'marginLeft':'20px'}} onClick={function(){
                    if(this.state.search === ""){
                        if(this.state.mode === "과목명") {
                            alert("과목명을 입력해주세요")
                        }

                        else {
                            alert("과목코드를 입력해주세요")
                        }
                    }

                    else {
                        fetch("http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/course", {
                            method: 'post',
                            body: JSON.stringify({
                                data: this.state.search,
                                mode: this.state.mode,
                                type: 'Subs'
                            })
                        }).then(res=>res.json())
                        .then(function(json){
                            this.setState({
                                search: "",
                                subject: json                                
                            })
                        }.bind(this))
                    }
                    }.bind(this)}>검색</Button>
                </div>
                <Paper style={{"height":"450px", "overflow":"auto"}}>
                <Table size="small" style={{"marginTop":"15px"}}>
                    <TableHead>
                        <TableRow>
                            <TableCell style={{"width":"1px", "alignItems":"center"}}></TableCell>
                            <TableCell style={{"textAlign":"center"}}>과목코드</TableCell>
                            <TableCell style={{"textAlign":"center"}}>과목명</TableCell>
                            <TableCell style={{"textAlign":"center"}}>대체코드</TableCell>
                            <TableCell style={{"textAlign":"center"}}>대체과목명</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody style={{"alignSelf":"center"}}>
                    {this.state.subject.map((item, index) => 
                            {return <TableRow key={item.pk} style={{'alignItems':'center'}}>
                                <TableCell style={{"textAlign":"center" , "width":"1px"}}><Checkbox onChange={function(e){
                                    let selected = Array.from(this.state.options)
                                    let cancel

                                    if(e.target.checked){
                                        selected.push(index)
                                    }

                                    else{
                                        cancel = selected.indexOf(index)
                                        selected.splice(cancel,1)
                                    }
                                    this.setState({
                                        options: selected
                                    })
                                }.bind(this)}></Checkbox></TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_id}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_title}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.sub_id}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.sub_title}</TableCell>                               
                            </TableRow>}
                            )}
                    </TableBody>
                </Table>
                {content}
                </Paper>
                <div style={{'textAlign':'center','margin':'auto', 'marginTop':'10px'}}>
                    <Button variant="contained" color="primary" size='large' style={{'marginRight':'20px'}} onClick={this._btnClick.bind(this)}>추가</Button>
                    <Button variant="contained" color="primary" size='large' onClick={
                        ()=>{
                            let selected = Array.from(this.state.options);
                            let newList = Array.from(this.state.subject);
                            let pass = [];

                            if(selected.length !== 0) {
                                if(selected.length > 1) {
                                    let i;
                                    selected.sort(function(a,b) {
                                        return b-a;
                                    });    
                                    
                                    for(i=0; i<selected.length; i++){
                                        pass.push(newList[selected[i]].pk);
                                        newList.splice(selected[i],1);
                                    }
                                }

                                else {
                                    pass.push(newList[selected[0]].pk);
                                    newList.splice(selected[0],1);
                                }

                                fetch("http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/delete", {
                                    method: 'post',
                                    body: JSON.stringify({
                                        data: pass,
                                        type: 'Subs'
                                    })
                                })
                            
                                this.setState({
                                    options: [],
                                    subject: newList
                                })
				alert("삭제되었습니다.");    
                            }
                        }
                    }>삭제</Button>
                </div>
                <Dialog open={this.state.open} onClose={this._closeBtn}>
                    <DialogTitle>대체과목추가</DialogTitle>
                    <DialogContent>
                        <TextField label="과목코드" type="text" name="oldCode" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="과목명" type="text" name="oldNm" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="대체코드" type="text" name="newCode" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="대체과목명" type="text" name="newNm" onChange={this._inputData.bind(this)}></TextField><br/>
                    </DialogContent>
                    <DialogActions>
                    <Button variant="contained" color="primary" onClick={()=>
                    {
                        if(this.state.oldCode !== "" && this.state.oldNm !== "" && this.state.newCode !== "" && this.state.newNm !== "") {
                            let pass = [];
                            pass.push(this.state.oldCode);
                            pass.push(this.state.oldNm);
                            pass.push(this.state.newCode);
                            pass.push(this.state.newNm);
                            fetch("http://ec2-3-21-126-101.us-east-2.compute.amazonaws.com:8888/add", {
                                method: 'post',
                                body: JSON.stringify({
                                    data: pass,
                                    type: 'Subs'
                                })
                            })
                            .then(this._closeBtn)
                        }

                        else {
                            alert('항목을 채워주세요')
                        }
                        
                    }}>확인</Button>
                    <Button variant="outlined" color="primary" onClick={this._closeBtn}>취소</Button>
                    </DialogActions>

                </Dialog>
            </div>
        );
    }
}

export default Substitute;





