import React, { useState, useRef, useEffect }  from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Button,
    Modal,
    Fade,
    Backdrop,
    Paper
  } from '@mui/material';
  

function EditableTableForm(){
    const [rows, setRows] = React.useState([]);

    const fetchTableData = async () => {
        setLoading(true);
        try {
            const response = await fetch('https://localhost:8080/api/getJoinTable');
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

    const [openModal, setOpenModal] = React.useState(false);

    const handleOpenModal = () => {
        setOpenModal(true);
    };

    const handleCloseModal = () => {
        setOpenModal(false);
    };

    const handleSubmitTable = async (e) => {
        e.preventDefault();
        // 必須項目チェック
        await fetchTableData();
    };

    //MaterialUIを使ったファイルアップロードアイテム
    const FileUploadButton = ({ onFileSelect }) => {
        const [fileName, setFileName] = useState('');
        const inputRef = React.useRef();
    
        const handleClick = () => {
            inputRef.current.click();
        };
    
        const handleChange = (event) => {
            const file = event.target.files[0];
            if (file) {
                setFileName(file.name);
                onFileSelect(file);
            }
        };
    
        return (
            <div>
                <input
                    ref={inputRef}
                    type="file"
                    style={{ display: 'none' }}
                    onChange={handleChange}
                />
                <Button
                    color="primary"
                    variant="contained"
                    onClick={handleClick}
                >
                    ファイルを選択
                </Button>
                {fileName && <div style={{ marginTop: '10px' }}>選択されたファイル: {fileName}</div>}
            </div>
        );
    };
    
    const handleUpdateCSV = async (event) => {
        event.preventDefault();
        
        // ファイルが選択されていなければ警告を出す
        if (!file) {
            alert('ファイルを選択してください');
            return;
        }
    
        // ファイルをFormDataオブジェクトに追加
        const formData = new FormData();
        formData.append('file', file);
    
        // アップロード処理中の状態を表示
        setLoading(true);
    
        try {
            // サーバーにファイルをPOST
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData,
            });
    
            // レスポンスの確認
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            // JSONデータを取得
            const data = await response.json();
    
            // 成功した場合の処理
            alert('ファイルがアップロードされました');
        } catch (error) {
            // エラー処理
            console.error('Upload failed:', error);
            alert(`アップロードに失敗しました: ${error.message}`);
        } finally {
            // ローディング状態の解除
            setLoading(false);
        }
    };

    const CsvDownloadModal = ({ open, handleClose }) => {
        return (
            <Modal
                open={open}
                onClose={handleClose}
                closeAfterTransition
                BackdropComponent={Backdrop}
                BackdropProps={{
                    timeout: 500,
                }}
            >
                <Fade in={open}>
                    <div style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        width: 400,
                        backgroundColor: 'white',
                        boxShadow: 24,
                        padding: 4,
                    }}>
                        {/* ここにダウンロード方法の説明を入れる */}
                        <p>CSVダウンロードの手順をここに記載します。</p>
                    </div>
                </Fade>
            </Modal>
        );
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
            <br/>
            <form onSubmit={handleUpdateCSV}>
                <h2>課題状況最新化機能</h2>
                <p>※本機能ではBacklogから取得した課題一覧のCSVをアップロードすることができます。（CSVのダウンロード方法は<a href="#" onClick={handleOpenModal}>こちら</a>）<br/>
                    　ここでCSVをアップロードすることで、最新の課題状況を反映することができます。<br/>
                    　処理終了には数分かかることもありますがご了承ください。また、処理中にページを閉じるなどはお控えください。<br/>
                    　必ずCSVは最新のものをダウンロードし、アップロードして下さい。 <br/>
                    　最終更新日時：2024/4/10 10:00:00
                </p>
                {/* MaterialUIを使ったファイルのアップロードアイテム */}
                <FileUploadButton onFileSelect={(file) => console.log(file)} />
                <input className="submitButton" type="submit" value="CSVアップロード" />
                <CsvDownloadModal open={openModal} handleClose={handleCloseModal} />
            </form>
        </React.Fragment>
    );
}

export default EditableTableForm;