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
import {DialogTitle, TextField, DialogActions, Select, MenuItem} from '@material-ui/core';
import DialogContent from '@material-ui/core/DialogContent'

class All extends Component {
    
    constructor(props){
        super(props);

        this.state = {
         subject: [
             {"year":"2020", "sem":1, "code":"111", "title":"test1", "credit":"3", "etc":"-"},
             {"year":"2020", "sem":1, "code":"112", "title":"test2", "credit":"3", "etc":"-"},
             {"year":"2020", "sem":1, "code":"113", "title":"test3", "credit":"3", "etc":"-"}
         ],
         options: [],
         open: false, year: '', sem: '', code: '', title: '', credit: '', etc: '',
         main: "문과대학"
        };
    }

    _inputData(e) {
        let nextState = {};

        nextState[e.target.name] = e.target.value;
        
        this.setState(nextState);
    }

    _selectChange(e) {
        this.setState({
            main: e.target.value
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
        var sub = ''
        if(this.state.main === "문과대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"국어국문학과"}>국어국문학과</MenuItem>
                <MenuItem value={"영어영문학과"}>영어영문학과</MenuItem>
                <MenuItem value={"독어독문학과"}>독어독문학과</MenuItem>
                <MenuItem value={"문헌정보학과"}>문헌정보학과</MenuItem>
                <MenuItem value={"불어불문학과"}>불어불문학과</MenuItem>
                <MenuItem value={"일어일문학과"}>일어일문학과</MenuItem>
                <MenuItem value={"심리학과"}>심리학과</MenuItem>
                <MenuItem value={"청소년학과"}>청소년학과</MenuItem>
                <MenuItem value={"철학과"}>철학과</MenuItem>
                <MenuItem value={"사회복지학과"}>사회복지학과</MenuItem>
                <MenuItem value={"아동복지학과"}>아동복지학과</MenuItem>
                <MenuItem value={"사회학과"}>사회학과</MenuItem>
                <MenuItem value={"민속학과"}>민속학과</MenuItem>
                <MenuItem value={"역사학과"}>역사학과</MenuItem>
            </Select>
        }
        else if(this.state.main === "자연과학대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"물리학과"}>물리학과</MenuItem>
                <MenuItem value={"화학과"}>화학과</MenuItem>
                <MenuItem value={"수리통계학부"}>수리통계학부</MenuItem>
                <MenuItem value={"수학정공"}>수학전공</MenuItem>
                <MenuItem value={"통계전공"}>통계전공</MenuItem>
                <MenuItem value={"생명과학과"}>생명과학과</MenuItem>
                <MenuItem value={"생명과학부"}>생명과학부</MenuItem>
                <MenuItem value={"수학과"}>수학과</MenuItem>
                <MenuItem value={"생명과학전공"}>생명과학전공</MenuItem>
                <MenuItem value={"의생명과학전공"}>의생명과학전공</MenuItem>
            </Select>
        }
        else if(this.state.main === "공과대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"기계공학부"}>기계공학부</MenuItem>
                <MenuItem value={"건설환경공학과"}>건설환경공학과</MenuItem>
                <MenuItem value={"전자전기공학부"}>전자전기공학부</MenuItem>
                <MenuItem value={"컴퓨터공학부"}>컴퓨터공학부</MenuItem>
                <MenuItem value={"건축학부"}>건축학부</MenuItem>
                <MenuItem value={"건축공학전공"}>건축공학전공</MenuItem>
                <MenuItem value={"건축학전공"}>건축학전공</MenuItem>
                <MenuItem value={"화학신소재공학부"}>화학신소재공학부</MenuItem>
                <MenuItem value={"도시공학과"}>도시공학과</MenuItem>
                <MenuItem value={"사회기반시스템공학부"}>사회기반시스템공학부</MenuItem>
                <MenuItem value={"융합공학부"}>융합공학부</MenuItem>
                <MenuItem value={"건설시스템공학전공"}>건설시스템공학전공</MenuItem>
                <MenuItem value={"도시시스템공학전공"}>도시시스템공학전공</MenuItem>
                <MenuItem value={"디지털이미지전공"}>디지털이미지전공</MenuItem>
                <MenuItem value={"나노바이오소재공학전공"}>나노바이오소재공학전공</MenuItem>
                <MenuItem value={"의료공학전공"}>의료공학전공</MenuItem>
                <MenuItem value={"건설환경플랜트공학전공"}>건설환경플랜트공학전공</MenuItem>
                <MenuItem value={"바이오메디컬공학전공"}>바이오메디컬공학전공</MenuItem>
                <MenuItem value={"에너지시스템 공학부"}>에너지시스템 공학부</MenuItem>
                <MenuItem value={"발전기계전공"}>발전기계전공</MenuItem>
                <MenuItem value={"원자력전공"}>원자력전공</MenuItem>
                <MenuItem value={"발전전기전공"}>발전전기전공</MenuItem>
            </Select>
        }
        else if(this.state.main === "사범대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"교육학과"}>교육학과</MenuItem>
                <MenuItem value={"유아교육과"}>유아교육과</MenuItem>
                <MenuItem value={"가정교육과"}>가정교육과</MenuItem>
                <MenuItem value={"체육교육과"}>체육교육과</MenuItem>
                <MenuItem value={"영어교육과"}>영어교육과</MenuItem>
            </Select>
        }
        else if(this.state.main === "법과대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"법학과"}>법학과</MenuItem>
            </Select>
        }
        else if(this.state.main === "정경대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"정치외교학과"}>정치외교학과</MenuItem>
                <MenuItem value={"행정학과"}>행정학과</MenuItem>
                <MenuItem value={"경제학과"}>경제학과</MenuItem>
                <MenuItem value={"광고홍보학과"}>광고홍보학과</MenuItem>
                <MenuItem value={"정경계열"}>정경계열</MenuItem>
            </Select>
        }
        else if(this.state.main === "경영대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"경영학부"}>경영학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "의과대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"간호학과"}>간호학과</MenuItem>
                <MenuItem value={"의학부"}>의학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "약학대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"약학전공"}>약학전공</MenuItem>
                <MenuItem value={"제약학전공"}>제약학전공</MenuItem>
                <MenuItem value={"약학부"}>약학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "미디어공연영상대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"신문방송학부"}>신문방송학부</MenuItem>
                <MenuItem value={"언론저널리즘전공"}>언론저널리즘전공</MenuItem>
                <MenuItem value={"미디어콘텐츠전공"}>미디어콘텐츠전공</MenuItem>
                <MenuItem value={"공연영상미술전공"}>공연영상미술전공</MenuItem>
                <MenuItem value={"연극전공"}>연극전공</MenuItem>
                <MenuItem value={"영화전공"}>영화전공</MenuItem>
            </Select>
        }
        else if(this.state.main === "자유전공학부") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"자유전공학부"}>자유전공학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "공공인재학부") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"공공인재학부"}>공공인재학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "글로벌지식학부") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"글로벌지식학부"}>글로벌지식학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "사회과학대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"정치국제학과"}>정치국제학과</MenuItem>
                <MenuItem value={"공공인재학부"}>공공인재학부</MenuItem>
                <MenuItem value={"심리학과"}>심리학과</MenuItem>
                <MenuItem value={"문헌정보학과"}>문헌정보학과</MenuItem>
                <MenuItem value={"사회복지학부"}>사회복지학부</MenuItem>
                <MenuItem value={"신문방송학부"}>신문방송학부</MenuItem>
                <MenuItem value={"사회학과"}>사회학과</MenuItem>
                <MenuItem value={"가족복지전공"}>가족복지전공</MenuItem>
                <MenuItem value={"사회복지전공"}>사회복지전공</MenuItem>
                <MenuItem value={"아동복지전공"}>아동복지전공</MenuItem>
                <MenuItem value={"청소년전공"}>청소년전공</MenuItem>
                <MenuItem value={"미디어콘텐츠전공"}>미디어콘텐츠전공</MenuItem>
                <MenuItem value={"언론저널리즘전공"}>언론저널리즘전공</MenuItem>
                <MenuItem value={"도시계획·부동산 학과"}>도시계획·부동산 학과</MenuItem>
                <MenuItem value={"미디어커뮤니케이션학부"}>미디어커뮤니케이션학부</MenuItem>
                <MenuItem value={"언론정보학부"}>언론정보학부</MenuItem>
                <MenuItem value={"디지털미디어콘텐츠전공"}>디지털미디어콘텐츠전공</MenuItem>
            </Select>
        }
        else if(this.state.main === "경영경제대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"글로벌금융전공"}>글로벌금융전공</MenuItem>
                <MenuItem value={"경제학부(서울)"}>경제학부(서울)</MenuItem>
                <MenuItem value={"응용통계학과"}>응용통계학과</MenuItem>
                <MenuItem value={"광고홍보학과"}>광고홍보학과</MenuItem>
                <MenuItem value={"지식경영학부"}>지식경영학부</MenuItem>
                <MenuItem value={"경영학부(서울)"}>경영학부(서울)</MenuItem>
                <MenuItem value={"국제물류 학과"}>국제물류 학과</MenuItem>
                <MenuItem value={"산업보안학과"}>산업보안학과</MenuItem>
                <MenuItem value={"경영학전공"}>경영학전공</MenuItem>
            </Select>
        }
        else if(this.state.main === "예술대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"공간연출전공"}>공간연출전공</MenuItem>
                <MenuItem value={"영화전공"}>영화전공</MenuItem>
                <MenuItem value={"연극전공"}>연극전공</MenuItem>
                <MenuItem value={"공연영상창작학부"}>공연영상창작학부</MenuItem>
                <MenuItem value={"디자인학부"}>디자인학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "인문대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"국어국문학과"}>국어국문학과</MenuItem>
                <MenuItem value={"영어영문학과"}>영어영문학과</MenuItem>
                <MenuItem value={"유럽문화학부"}>유럽문화학부</MenuItem>
                <MenuItem value={"아시아문화학부"}>아시아문화학부</MenuItem>
                <MenuItem value={"철학과"}>철학과</MenuItem>
                <MenuItem value={"역사학과"}>역사학과</MenuItem>
            </Select>
        }
        else if(this.state.main === "적십자간호대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"간호학과"}>간호학과</MenuItem>
            </Select>
        }
        else if(this.state.main === "창의ICT공과대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"융합교양학부"}>융합교양학부</MenuItem>
                <MenuItem value={"전자전기공학부"}>전자전기공학부</MenuItem>
                <MenuItem value={"컴퓨터공학부"}>컴퓨터공학부</MenuItem>
                <MenuItem value={"소프트웨어전공"}>소프트웨어전공</MenuItem>
                <MenuItem value={"컴퓨터공학전공"}>컴퓨터공학전공</MenuItem>
                <MenuItem value={"융합공학부"}>융합공학부</MenuItem>
                <MenuItem value={"바이오메디컬공학전공"}>바이오메디컬공학전공</MenuItem>
                <MenuItem value={"나노바이오소재공학전공"}>나노바이오소재공학전공</MenuItem>
                <MenuItem value={"디지털이미징전공"}>디지털이미징전공</MenuItem>
                <MenuItem value={"소프트웨어학부"}>소프트웨어학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "교양학부대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"교양학부"}>교양학부</MenuItem>
            </Select>
        }
        else if(this.state.main === "소프트웨어대학") {
            sub = 
            <Select style={{"marginLeft":'20px'}}>
                <MenuItem value={"소프트웨어학부"}>소프트웨어학부</MenuItem>
            </Select>
        }

        

        return(
            <div style={{"marginTop":"15px"}}>
                <div style={{"textAlign":"center"}}>
                    <Select defaultValue={"2020"}>
                        <MenuItem value={"2010"}>2010년</MenuItem>
                        <MenuItem value={"2011"}>2011년</MenuItem>
                        <MenuItem value={"2012"}>2012년</MenuItem>
                        <MenuItem value={"2013"}>2013년</MenuItem>
                        <MenuItem value={"2014"}>2014년</MenuItem>
                        <MenuItem value={"2015"}>2015년</MenuItem>
                        <MenuItem value={"2016"}>2016년</MenuItem>
                        <MenuItem value={"2017"}>2017년</MenuItem>
                        <MenuItem value={"2018"}>2018년</MenuItem>
                        <MenuItem value={"2019"}>2019년</MenuItem>
                        <MenuItem value={"2020"}>2020년</MenuItem>
                    </Select>
                    <Select defaultValue={"1"} style={{"marginLeft":'20px'}}>
                        <MenuItem value={"1"}>1학기</MenuItem>
                        <MenuItem value={"2"}>2학기</MenuItem>
                    </Select>
                    <Select defaultValue={"문과대학"} style={{"marginLeft":'20px'}} onChange={this._selectChange.bind(this)}>
                        <MenuItem value={"문과대학"}>문과대학</MenuItem>
                        <MenuItem value={"자연과학대학"}>자연과학대학</MenuItem>
                        <MenuItem value={"공과대학"}>공과대학</MenuItem>
                        <MenuItem value={"사범대학"}>사범대학</MenuItem>
                        <MenuItem value={"법과대학"}>법과대학</MenuItem>
                        <MenuItem value={"정경대학"}>정경대학</MenuItem>
                        <MenuItem value={"경영대학"}>경영대학</MenuItem>
                        <MenuItem value={"의과대학"}>의과대학</MenuItem>
                        <MenuItem value={"약학대학"}>약학대학</MenuItem>
                        <MenuItem value={"미디어공연영상대학"}>미디어공연영상대학</MenuItem>
                        <MenuItem value={"자유전공학부"}>자유전공학부</MenuItem>
                        <MenuItem value={"공공인재학부"}>공공인재학부</MenuItem>
                        <MenuItem value={"글로벌지식학부"}>글로벌지식학부</MenuItem>
                        <MenuItem value={"사회과학대학"}>사회과학대학</MenuItem>
                        <MenuItem value={"경영경제대학"}>경영경제대학</MenuItem>
                        <MenuItem value={"예술대학"}>예술대학</MenuItem>
                        <MenuItem value={"인문대학"}>인문대학</MenuItem>
                        <MenuItem value={"적십자간호대학"}>적십자간호대학</MenuItem>
                        <MenuItem value={"창의ICT공과대학"}>창의ICT공과대학</MenuItem>
                        <MenuItem value={"교양학부대학"}>교양학부대학</MenuItem>
                        <MenuItem value={"소프트웨어대학"}>소프트웨어대학</MenuItem>
                    </Select>
                    {sub}
                </div>
                <Paper>
                <Table size="small" style={{"marginTop":"15px"}}>
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





