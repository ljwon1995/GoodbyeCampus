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

class Substitute extends Component {
    
    constructor(props){
        super(props);

        this.state = {
         subject: [
             {"oldCode":"11111", "oldNm":"old", "newCode":"11222", "newNm":"new"}
         ],
         options: [],
         open: false,
         oldCode: '',
         oldNm: '',
         newCode: '',
         newNm: ''
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

    _closeBtn() {
        this.setState({
            oldCode: '',
            oldNm: '',
            newCode: '',
            newNm: '',
        })
    }

    _addNewItem() {
        const list = this.state.subject
        let newItem = {
            "oldCode": this.state.oldCode,
            "oldNm": this.state.oldNm,
            "newCode": this.state.newCode,
            "newNm": this.state.newNm,
        }

        this.setState({
            subject: list.concat(newItem),
            oldCode: '',
            oldNm: '',
            newCode: '',
            newNm: '',
            open: false
        })

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

    render(){
        return(
            <div>
                <Paper>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
                            <TableCell></TableCell>
                            <TableCell>과목코드</TableCell>
                            <TableCell>과목명</TableCell>
                            <TableCell>대체코드</TableCell>
                            <TableCell>대체과목명</TableCell>
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
                                <TableCell>{item.oldCode}</TableCell>
                                <TableCell>{item.oldNm}</TableCell>
                                <TableCell>{item.newCode}</TableCell>
                                <TableCell>{item.newNm}</TableCell>
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
                    <DialogTitle>대체과목추가</DialogTitle>
                    <DialogContent>
                        <TextField label="과목코드" type="text" name="oldCode" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="과목명" type="text" name="oldNm" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="대체코드" type="text" name="newCode" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="대체과목명" type="text" name="newNm" onChange={this._inputData.bind(this)}></TextField><br/>
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

export default Substitute;





