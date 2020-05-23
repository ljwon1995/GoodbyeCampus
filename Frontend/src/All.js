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
import DialogContent from '@material-ui/core/DialogContent'

class All extends Component {
    
    constructor(props){
        super(props);

        this.state = {
         subject: [
             {"year":"2020", "sem":1, "code":"111", "title":"test1", "credit":"3", "etc":"-"},
             {"year":"2020", "sem":1, "code":"112", "title":"test2", "credit":"3", "etc":"-"},
             {"year":"2020", "sem":1, "code":"113", "title":"test3", "credit":"3", "etc":"-"},
             {"year":"2020", "sem":1, "code":"114", "title":"test4", "credit":"3", "etc":"-"},
             {"year":"2020", "sem":1, "code":"115", "title":"test5", "credit":"3", "etc":"-"}
         ],
         options: [],
         open: false,
         year: '',
         sem: '',
         code: '',
         title: '',
         credit: '',
         etc: ''

        };
    }

    _inputData(e) {
        let nextState = {};

        nextState[e.target.name] = e.target.value;
        
        this.setState(nextState);
    }

    _delete() {
        const options = this.state.options
        const newList = this.state.subject
        if(this.state.options.length > 1) {

            options.sort(function(a, b) { // 내림차순
                return b - a
            });

            let i
            for(i=0; i<options.length; i++){
                newList.splice(options[i],1)
            }

            this.setState({
                subject: newList,
                options: []
            })
        }

        else if(this.state.options.length === 1) {
            newList.splice(options[0],1)

            this.setState({
                subject: newList,
                options: []
            })
        }

    }

    _btnClick() {
        this.setState({
            open: true
        })
    }

    _closeBtn() {
        this.setState({
            year: '',
            sem: '',
            code: '',
            title: '',
            credit: '',
            etc: '',
            open: false
        })
    }

    _addNewItem() {
        const list = this.state.subject
        let newItem = {
            "year": this.state.year,
            "sem": this.state.sem,
            "code": this.state.code,
            "title": this.state.title,
            "credit": this.state.credit,
            "etc": this.state.etc}

        this.setState({
            subject: list.concat(newItem),
            year: '',
            sem: '',
            code: '',
            title: '',
            credit: '',
            etc: '',
            open: false
        })

    }

    render(){
        return(
            <div>
                <Paper>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
                            <TableCell></TableCell>
                            <TableCell>년도</TableCell>
                            <TableCell>학기</TableCell>
                            <TableCell>과목코드</TableCell>
                            <TableCell>과목명</TableCell>
                            <TableCell>학점</TableCell>
                            <TableCell>비고</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {this.state.subject.map((item, index) => 
                            <TableRow style={{'alignItems':'center'}}>
                                <TableCell><Checkbox onChange={function(e){
                                    const options = this.state.options;
                                    let indx;

                                    if(e.target.checked){
                                        options.push(index)
                                    }
                                    else{
                                        indx = options.indexOf(index)
                                        options.splice(indx,1)
                                    }
                                    this.setState({ options: options })
                                }.bind(this)}></Checkbox></TableCell>
                                <TableCell>{index+1}</TableCell>
                                <TableCell>{item.year}</TableCell>
                                <TableCell>{item.sem}</TableCell>
                                <TableCell>{item.code}</TableCell>
                                <TableCell>{item.title}</TableCell>
                                <TableCell>{item.credit}</TableCell>
                                <TableCell>{item.etc}</TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
                </Paper>
                <div style={{'textAlign':'center','margin':'auto', 'marginTop':'10px'}}>
                    <Button variant="contained" color="primary" size='large' style={{'marginRight':'20px'}} onClick={this._btnClick.bind(this)}>추가</Button>
                    <Button variant="contained" color="primary" size='large' onClick={this._delete.bind(this)}>삭제</Button>
                </div>
                <Dialog open={this.state.open} onClose>
                    <DialogTitle>과목추가</DialogTitle>
                    <DialogContent>
                        <TextField label="년도" type="text" name="year" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="학기" type="text" name="sem" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="과목코드" type="text" name="code" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="과목명" type="text" name="title" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="학점" type="text" name="credit" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="비고" type="text" name="etc" onChange={this._inputData.bind(this)}></TextField><br/>
                    </DialogContent>
                    <DialogActions>
                    <Button variant="contained" color="primary" onClick={this._addNewItem.bind(this)}>확인</Button>
                    <Button variant="outlined" color="primary" onClick={this._closeBtn.bind(this)}>취소</Button>
                    </DialogActions>

                </Dialog>
            </div>
        );
    }
}

export default All;





