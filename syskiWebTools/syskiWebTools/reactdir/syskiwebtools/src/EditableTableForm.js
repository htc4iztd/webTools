import React, { useState, useRef, useEffect }  from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Paper
  } from '@mui/material';
  

function EditableTableForm(){
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState([]);

    const fetchTableData = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8080/getJoinTable');
            if(!response.ok){
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setRows(data);
        } catch (error) {
            console.error("Error fetching data: ", error);
            alert('データの取得に失敗しました。');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTableData();
    }, []);

    const handleSubmitTable = async (e) => {
        e.preventDefault();
        // 必須項目チェック
        await fetchTableData();
    };

    return (
        <React.Fragment>
            <form onSubmit={handleSubmitTable}>
                <h2>稼働管理表</h2>
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell rowSpan={2}>SEQNO</TableCell>
                                    <TableCell rowSpan={2}>案件名</TableCell>
                                    <TableCell rowSpan={2}>案件T</TableCell>
                                    <TableCell rowSpan={2}>案件担当者</TableCell>
                                    <TableCell rowSpan={2}>案件規模</TableCell>
                                    <TableCell colSpan={2} align="center">案件検討状況</TableCell>
                                    <TableCell colSpan={3} align="center">課題数（要求部門＋開発）</TableCell>
                                    <TableCell colSpan={2} align="center">想定打合せ時間</TableCell>
                                    <TableCell colSpan={2} align="center">その他作業時間（備考欄要記載）</TableCell>
                                    <TableCell rowSpan={2}>合計工数</TableCell>
                                    <TableCell rowSpan={2}>備考</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>状況</TableCell>
                                    <TableCell>対応中工数</TableCell>
                                    <TableCell>課題残数(シス企関連)</TableCell>
                                    <TableCell>全課題数(参考)</TableCell>
                                    <TableCell>対応中工数</TableCell>
                                    <TableCell>直近2週間 想定時間(h)</TableCell>
                                    <TableCell>対応中工数</TableCell>
                                    <TableCell>直近2週間 想定時間(h)</TableCell>
                                    <TableCell>対応中工数</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {rows.map((row) => (
                                    <TableRow key={row.seq_no}>
                                        <TableCell>
                                            <TextField>
                                                type="helperText"
                                                value={row.seq_no}
                                            </TextField>
                                        </TableCell>
                                        <TableCell>
                                            <TextField>
                                                type="helperText"
                                                value={row.project}
                                            </TextField>
                                        </TableCell>
                                        <TableCell>
                                            <TextField>
                                                type="helperText"
                                                value={row.team}
                                            </TextField>
                                        </TableCell>
                                        <TableCell>
                                            <TextField>
                                                type="helperText"
                                                value={row.prsnInChrg}
                                            </TextField>
                                        </TableCell>
                                        <TableCell>
                                            <TextField>
                                                type="helperText"
                                                value={row.prjctSize}
                                            </TextField>
                                        </TableCell>
                                        <TableCell>
                                            <TextField>
                                                type="helperText"
                                                value={row.prjctSts}
                                            </TextField>
                                        </TableCell>
                                        <TableCell>
                                            {
                                                row.prjctSts === '要求定義中' ?
                                                <TextField value={row.prjctMnHrsValue}/>:
                                                <TextField value="-"/>
                                            }
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.remainTaskSys} />                                                    
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.allTaskSys} />                                                    
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.crspndMnHrs} />                                                    
                                        </TableCell>
                                        <TableCell>
                                            <TextField type="helperText" value={row.estMtgTimeTwWks} />
                                        </TableCell>
                                        <TableCell>
                                            {
                                                row.prjctSts === '要求定義中' ?
                                                <TextField value={row.mtgMnHrs} />:
                                                <TextField value="-"/>
                                            }
                                        </TableCell>
                                        <TableCell>
                                            <TextField type="helperText" value={row.estwkTimeTwWks} />
                                        </TableCell>
                                        <TableCell>
                                            {
                                                row.prjctSts === '要求定義中' ?
                                                <TextField value={row.wkMnHrs} />:
                                                <TextField value="-"/>
                                            }
                                        </TableCell>
                                        <TableCell>
                                            {
                                                row.prjctMnHrsValue + row.crspndMnHrs + row.mtgMnHrs + row.wkMnHrs
                                            }
                                        </TableCell>
                                        <TableCell>
                                            <TextField type="helperText" value={row.remarks} />
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                )}
                <input className="submitButton" type="submit" value="稼働表の更新" />
            </form>
        </React.Fragment>
    );
}

export default EditableTableForm;
