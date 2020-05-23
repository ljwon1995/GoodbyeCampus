import React, {Component} from 'react';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';

class All extends Component {
    
    constructor(props){
        super(props);

        this.state = {
         subject: [
             {"id":"0", "year":"2018", "sem":1, "code":"123", "title":"asdf", "credit":"3", "etc":"~~~"},
             {"id":"1", "year":"2018", "sem":1, "code":"123", "title":"asdf", "credit":"3", "etc":"~~~"},
             {"id":"2", "year":"2018", "sem":1, "code":"123", "title":"asdf", "credit":"3", "etc":"~~~"},
             {"id":"3", "year":"2018", "sem":1, "code":"123", "title":"asdf", "credit":"3", "etc":"~~~"},
             {"id":"4", "year":"2018", "sem":1, "code":"123", "title":"asdf", "credit":"3", "etc":"~~~"}
         ],
         options: []
        };
    }
    onChange(e) {
        // current array of options
        const options = this.state.options
        let index
 
        // check if the check box is checked or unchecked
        if (e.target.checked) {
          // add the numerical value of the checkbox to options array
          options.push(e.target.value)
        } else {
          // or remove the value from the unchecked checkbox from the array
          index = options.indexOf(e.target.index)
          options.splice(index, 1)
        }
 
        // update the state with the new array of options
        this.setState({ options: options })
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
                    <Button variant="contained" color="primary" size='large' style={{'marginRight':'20px'}}>추가</Button>
                    <Button variant="contained" color="primary" size='large'>삭제</Button>
                </div>
            </div>
        );
    }
}

export default All;





