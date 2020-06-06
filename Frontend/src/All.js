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
import DialogContent from '@material-ui/core/DialogContent';

class All extends Component {    
    constructor(props){
        super(props);

        this.state = {
            options: [],
            subject: [],
            open: false, 
            year:"2020", sem:"1", shyr:"1", dist:"교양", colgnm:"", sust:"", title:"", prof:"", time:"", code:"", credit:"", etc:"",
            s_title : "", s_year: '2020', s_sem: '1',
            main: "소프트웨어대학",
            sub : "소프트웨어학부"
        };
    }

    _inputData(e) {
        let nextState = {};

        nextState[e.target.name] = e.target.value;
        
        this.setState(nextState);
    }

    _subSelect = (event) => {
        this.setState({
            sub: event.target.value
        })
    }

    _btnClick() {
        this.setState({
            open: true
        })
    }

    _closeBtn = () => {
        this.setState({
            year:"2020", 
            sem:"1", 
            shyr:"1", 
            dist:"교양", 
            colgnm:"", 
            sust:"", 
            title:"", 
            prof:"", 
            time:"", 
            code:"", 
            credit:"", 
            etc:"",
            open: false
        })
    }

    _selectYear = (event) => {
        this.setState({
            s_year: event.target.value
        })
    }

    _selectsem = (event) => {
        this.setState({
            s_sem: event.target.value
        })
    }

    _addFormSelect = (event) => {
        let nextState = {};

        nextState[event.target.name] = event.target.value;
        
        this.setState(nextState);
    }
    render(){

        const category = {
            "문과대학" : ["국어국문학과", "영어영문학과", "독어독문학과", "문헌정보학과", "불어불문학과", "일어일문학과", "심리학과", "청소년학과", "철학과", "사회복지학과", "아동복지학과", "사회학과", "민속학과", "역사학과"],
            "자연과학대학" : ["물리학과", "화학과", "수리통계학부", "수학전공", "통계전공", "생명과학과", "생명과학부", "수학과", "생명과학전공", "의생명과학전공"],
            "공과대학" : ["기계공학부", "건설환경공학과", "전자전기공학부", "컴퓨터공학부", "건축학부", "건축공학전공", "건축학전공", "화학신소재공학부", "도시공학과", "사회기반시스템공학부", "융합공학부", "건설시스템공학전공", "도시시스템공학전공", "디지털이미지전공", "나노바이오소재공학전공", "의료공학전공", "건설환경플랜트공학전공", "바이오메디컬공학전공", "에너지시스템 공학부", "발전기계전공", "원자력전공", "발전전기전공"],
            "사범대학" : ["교육학과", "유아교육과", "가정교육과", "체육교육과", "영어교육과"],
            "법과대학" : ["법학과"],
            "정경대학" : ["정치외교학과", "행정학과", "경제학과", "광고홍보학과", "정경계열"],
            "경영대학" : ["경영학부"],
            "의과대학" : ["간호학과", "의학부"],
            "약학대학" : ["약학전공", "제약학전공", "약학부"],
            "미디어공연영상대학" : ["신문방송학부", "언론저널리즘전공", "미디어콘텐츠전공", "공연영상미술전공", "연극전공", "영화전공"],
            "자유전공학부" : ["자유전공학부"],
            "공공인재학부" : ["공공인재학부"],
            "글로벌지식학부" : ["글로벌지식학부"],
            "사회과학대학" : ["정치국제학과", "공공인재학부", "심리학과", "문헌정보학과", "사회복지학부", "신문방송학부", "사회학과", "가족복지전공", "사회복지전공", "아동복지전공", "청소년전공", "미디어콘텐츠전공", "언론저널리즘전공", "도시계획·부동산 학과", "미디어커뮤니케이션학부", "언론정보학부", "디지털미디어콘텐츠전공"],
            "경영경제대학" : ["글로벌금융전공", "경제학부(서울)", "응용통계학과", "광고홍보학과", "지식경영학부", "경영학부(서울)", "국제물류 학과", "산업보안학과", "경영학전공"],
            "예술대학" : ["공간연출전공", "영화전공", "연극전공", "공연영상창작학부", "디자인학부"],
            "인문대학" : ["국어국문학과", "영어영문학과", "유럽문화학부", "아시아문화학부", "철학과", "역사학과"],
            "적십자간호대학" : ["간호학과"],
            "창의ICT공과대학" : ["융합교양학부", "전자전기공학부", "컴퓨터공학부", "소프트웨어전공", "컴퓨터공학전공", "융합공학부", "바이오메디컬공학전공", "나노바이오소재공학전공", "디지털이미징전공", "소프트웨어학부"],
            "교양학부대학" : ["교양학부"],
            "소프트웨어대학" : ["소프트웨어학부"]
        }        


        let content = null;

        if(this.state.subject.length === 0) {
            content = <div style = {{"textAlign" : "center", "marginTop" : "160px"}}>검색결과가 없습니다.</div>
        }

        return(
            <div style={{"marginTop":"15px"}}>
                <div style={{"textAlign":"center"}}>
                    <Select value={this.state.s_year ? this.state.s_year : ""} onChange={this._selectYear}>
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
                    <Select value={this.state.s_sem ? this.state.s_sem : ""} style={{"marginLeft":'20px'}} onChange={this._selectsem}>
                        <MenuItem value={"1"}>1학기</MenuItem>
                        <MenuItem value={"S"}>하계</MenuItem>
                        <MenuItem value={"2"}>2학기</MenuItem>
                        <MenuItem value={"W"}>동계</MenuItem>
                    </Select>
                    <Select value={this.state.main ? this.state.main : ""} style={{"marginLeft":'20px'}} onChange={(event)=>{
                            this.setState({
                                main: event.target.value,
                                sub: category[event.target.value][0]});
                    }}>
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
                    <Select value={this.state.sub ? this.state.sub : ""} style={{"marginLeft":'20px'}} onChange={this._subSelect}>
                        {category[this.state.main].map((item, index) => 
                                <MenuItem key={index} value={item}>{item}</MenuItem>)}
                    </Select>
                    <TextField value={this.state.s_title} variant="outlined" style={{"marginLeft":'20px'}} size="small" label="과목명" type="text" name="s_title" onChange={this._inputData.bind(this)}></TextField>
                    <Button variant="contained" color="primary" size='large' style={{'marginLeft':'20px'}} onClick={
                        function(){
                            let pass = [];

                            pass.push(this.state.s_year);
                            pass.push(this.state.s_sem);
                            pass.push(this.state.main);
                            pass.push(this.state.sub);
                            pass.push(this.state.s_title);
                            
                            fetch("http://localhost:8000/course", {
                                method : 'post',
                                body : JSON.stringify({
                                    data : pass,
                                    type : "All"
                                })
                            }).then(res=>res.json())
                            .then(function(json){
                                this.setState({
                                    s_title: "",
                                    subject: json
                                })
                            }.bind(this))}.bind(this)}>검색</Button>
                </div>
                <Paper style={{"height":"450px", "overflow":"auto"}}>
                <Table size="small" style={{"marginTop":"15px"}}>
                    <TableHead>
                        <TableRow>
                            <TableCell style={{"width":"1px", "alignItems":"center"}}></TableCell>
                            <TableCell style={{"textAlign":"center"}}>년도</TableCell>
                            <TableCell style={{"textAlign":"center"}}>학기</TableCell>
                            <TableCell style={{"textAlign":"center"}}>대학</TableCell>
                            <TableCell style={{"textAlign":"center"}}>학부</TableCell>
                            <TableCell style={{"textAlign":"center"}}>과목분류</TableCell>
                            <TableCell style={{"textAlign":"center"}}>과목코드</TableCell>
                            <TableCell style={{"textAlign":"center"}}>과목이름</TableCell>
                            <TableCell style={{"textAlign":"center"}}>학점</TableCell>
                            <TableCell style={{"textAlign":"center"}}>비고</TableCell>
                        </TableRow>
                    </TableHead>    
                    <TableBody style={{"alignSelf":"center"}}>
                        {this.state.subject.map((item, index) => 
                            {return <TableRow key={item.pk} style={{'alignItems':'center'}}>
                                <TableCell style={{"textAlign":"center"}}><Checkbox onChange={function(e){
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
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_year}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_semester}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_colgnm}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_sustnm}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_pobjnm}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_sbjtclss}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_clssnm}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_pnt}</TableCell>
                                <TableCell style={{"textAlign":"center"}}>{item.fields.course_remk}</TableCell>                                
                            </TableRow>}
                            )}
                        </TableBody>
                </Table>
                {content}
                </Paper>
                <div style={{'textAlign':'center','margin':'auto', 'marginTop':'10px'}}>
                    <Button variant="contained" color="primary" size='large' style={{'marginRight':'20px'}} onClick={this._btnClick.bind(this)}>추가</Button>
                    <Button variant="contained" color="primary" size='large' onClick=
                    {

                        e=>{

                            let selected = Array.from(this.state.options);
                            let newList = Array.from(this.state.subject);
                            let pass = [];
                            
                            if(selected.length !== 0){
                                if(selected.length > 1){
                                    let i
                                    selected.sort(function(a, b) { // 내림차순
                                        return b - a;
                                        // 11, 10, 4, 3, 2, 1
                                    });
                                    for(i=0; i<selected.length; i++){
                                        pass.push(newList[selected[i]].pk)
                                        newList.splice(selected[i],1)
                                    }
                                }
                    
                                else{
                                    pass.push(newList[selected[0]].pk)
                                    newList.splice(selected[0],1)
                                }     

                                fetch("http://localhost:8000/delete", {
                                method: 'post',
                                body: JSON.stringify({
                                    data: pass,
                                    type: 'All'
                                    })
                                })
                    
                                this.setState({
                                    options: [],
                                    subject: newList
                                })
                            }
                        }                 
                    }
                    >삭제</Button>
                </div>
                <Dialog open={this.state.open} onClose={this._closeBtn}>
                    <DialogTitle style={{"textAlign":"center"}}>과목추가</DialogTitle>
                    <DialogContent style={{"textAlign":"center"}}>
                        <Select name="year" value={this.state.year ? this.state.year : ""}
                        onChange={this._addFormSelect}>
                            <MenuItem value={"2020"}>2020년</MenuItem>
                        </Select>
                        <Select name="sem" value={this.state.sem ? this.state.sem : ""}
                        onChange={this._addFormSelect}>
                            <MenuItem value={"1"}>1학기</MenuItem>
                            <MenuItem value={"S"}>하계</MenuItem>
                            <MenuItem value={"2"}>2학기</MenuItem>
                            <MenuItem value={"W"}>동계</MenuItem>
                        </Select>
                        <Select name="shyr" value={this.state.shyr ? this.state.shyr : ""}
                        onChange={this._addFormSelect}>
                            <MenuItem value={"1"}>1학년</MenuItem>
                            <MenuItem value={"2"}>2학년</MenuItem>
                            <MenuItem value={"3"}>3학년</MenuItem>
                            <MenuItem value={"4"}>4학년</MenuItem>
                        </Select>
                        <Select name="dist" value={this.state.dist ? this.state.dist : ""}
                        onChange={this._addFormSelect}>
                            <MenuItem value={"교양"}>교양</MenuItem>
                            <MenuItem value={"전공"}>전공</MenuItem>
                            <MenuItem value={"전공필수"}>전공필수</MenuItem>
                        </Select><br/>
                        <TextField label="단과대학" type="text" name="colgnm" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="학부" type="text" name="sust" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="과목명" type="text" name="title" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="교수" type="text" name="prof" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField label="시간표" type="text" name="time" onChange={this._inputData.bind(this)}></TextField><br/>
                        <TextField style={{"width":'30%'}} label="과목코드-분반" type="text" name="code" onChange={this._inputData.bind(this)}></TextField>
                        <TextField style={{"width":'25%', "marginLeft":"5px"}} label="학점-시간" type="text" name="credit" onChange={this._inputData.bind(this)}></TextField><br/>                        
                        <TextField label="비고" type="text" name="etc" onChange={this._inputData.bind(this)}></TextField><br/>
                    </DialogContent>
                    <DialogActions>
                    <Button variant="contained" color="primary" onClick={
                        (event) => {
                            if(!(this.state.colgnm === "") && !(this.state.sust === "") && !(this.state.title === "")){
                                let pass = [];
                                pass.push(this.state.year); 
                                pass.push(this.state.sem);
                                pass.push(this.state.shyr);
                                pass.push(this.state.dist);
                                pass.push(this.state.colgnm);
                                pass.push(this.state.sust);
                                pass.push(this.state.title);
                                pass.push(this.state.prof);
                                pass.push(this.state.time);
                                pass.push(this.state.code);
                                pass.push(this.state.credit);
                                pass.push(this.state.etc);

                                let i;
                                for(i=0; i<pass.length; i++){
                                    if(pass[i] === "") {
                                        pass[i] = "None";
                                    }
                                }

                                fetch("http://localhost:8000/add",
                                {
                                    method: 'post',
                                    body: JSON.stringify({
                                        data: pass,
                                        type: 'All'
                                    })
                                })
                                .then(this._closeBtn)
                            }
                            else {
                                alert('항목을 채워주세요')
                            }
                    }
                    }>확인</Button>
                    <Button variant="outlined" color="primary" onClick={this._closeBtn}>취소</Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default All;





