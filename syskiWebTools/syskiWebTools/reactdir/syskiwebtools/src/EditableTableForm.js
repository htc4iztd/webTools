import React, { useState, useEffect } from 'react';
import animation from "./loading.gif";
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
    const [loading, setLoading] = useState(false);

    const fetchTableData = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/getJoinedTable');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            // データが配列かどうか確認し、配列でない場合は空配列をセット
            if (Array.isArray(data)) {
                setRows(data);
            } else {
                console.error("Fetched data is not an array:", data);
                setRows([]);
            }
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
                    <img src={animation} alt="ローディングアニメーション"/>
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
                                {Array.isArray(rows) && rows.map((row) => (
                                    <TableRow key={row.seq_no}>
                                        <TableCell>
                                            <TextField value={row.seq_no} />
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.project} />
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.team} />
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.prsnInChrg} />
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.prjctSize} />
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.prjctSts} />
                                        </TableCell>
                                        <TableCell>
                                            {row.prjctSts === '要求定義中' ? (
                                                <TextField value={row.prjctMnHrsValue}/>
                                            ) : (
                                                <TextField value="-"/>
                                            )}
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
                                            <TextField value={row.estMtgTimeTwWks} />
                                        </TableCell>
                                        <TableCell>
                                            {row.prjctSts === '要求定義中' ? (
                                                <TextField value={row.mtgMnHrs} />
                                            ) : (
                                                <TextField value="-"/>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.estwkTimeTwWks} />
                                        </TableCell>
                                        <TableCell>
                                            {row.prjctSts === '要求定義中' ? (
                                                <TextField value={row.wkMnHrs} />
                                            ) : (
                                                <TextField value="-"/>
                                            )}
                                        </TableCell>
                                        <TableCell>
                                            {row.prjctMnHrsValue + row.crspndMnHrs + row.mtgMnHrs + row.wkMnHrs}
                                        </TableCell>
                                        <TableCell>
                                            <TextField value={row.remarks} />
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
