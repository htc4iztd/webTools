import React, { useState }  from 'react';
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
    const [apiKey, setApiKey] = React.useState('');
    const [projectId, setProjectId] = useState('');
    const [typeId, setTypeId] = useState('');
    const [name, setName] = useState('');
    const [itemString, setItemString] = useState('');
    const [required, setRequired] = useState(false);
    const [log, setLog] = useState(null);

    React.useEffect(() => {
        fetch('https://localhost:8080/api/getJoinTable')
            .then(response => response.json())
            .then(data => setRows(data))
            .catch(error => console.error("Error:", error));
    }, []);

    const [openModal, setOpenModal] = React.useState(false);

    const handleOpenModal = () => {
        setOpenModal(true);
    };

    const handleCloseModal = () => {
        setOpenModal(false);
    };

    const handleSubmitTable = (e) => {
        e.preventDefault();
        // 必須項目チェック
        if (!apiKey || !projectId || !typeId || !name) {
            alert('必須項目が入力されていません');
            return;
        }
        if (typeId === '6' && !itemString) {
            alert('リスト項目が入力されていません');
            return;
        }
    
        const formData = new URLSearchParams();
        formData.append('typeId', typeId);
        formData.append('name', name);
        if (typeId === '6') {
            itemString.split(',').forEach(item => formData.append('items[]', item.trim()));
        }
        formData.append('required', required);
    
        fetch(`https://isp-sekkei.backlog.com/api/v2/projects/${projectId}/customFields?apiKey=${apiKey}`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        })
        .then(response => {
            setLog({
                statusCode: response.status,
                response: null
            });
            return response.json();
        })
        .then(data => {
            setLog(prevLog => ({ ...prevLog, response: data }));
        })
        .catch(error => {
            console.error('Error:', error);
            setLog(prevLog => ({ ...prevLog, response: error }));
        });
    };


    const handleSubmitTasks = (e) => {
        e.preventDefault();
        // 必須項目チェック
        if (!apiKey || !projectId || !typeId || !name) {
            alert('必須項目が入力されていません');
            return;
        }
        if (typeId === '6' && !itemString) {
            alert('リスト項目が入力されていません');
            return;
        }
    
        const formData = new URLSearchParams();
        formData.append('typeId', typeId);
        formData.append('name', name);
        if (typeId === '6') {
            itemString.split(',').forEach(item => formData.append('items[]', item.trim()));
        }
        formData.append('required', required);
    
        fetch(`https://isp-sekkei.backlog.com/api/v2/projects/${projectId}/customFields?apiKey=${apiKey}`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        })
        .then(response => {
            setLog({
                statusCode: response.status,
                response: null
            });
            return response.json();
        })
        .then(data => {
            setLog(prevLog => ({ ...prevLog, response: data }));
        })
        .catch(error => {
            console.error('Error:', error);
            setLog(prevLog => ({ ...prevLog, response: error }));
        });
    };

    //MaterialUIを使ったファイルアップロードアイテム
    const FileUploadButton = ({ onFileSelect }) => {
        const inputRef = React.useRef();
    
        const handleClick = () => {
            inputRef.current.click();
        };
    
        const handleChange = (event) => {
            if (event.target.files.length > 0) {
                onFileSelect(event.target.files[0]);
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
            </div>
        );
    };
    

    // MaterialUIを使ったファイルアップロードアイテムに対するアクションロジック
    const handleUpdateCSV = (event) => {
        event.preventDefault();
        // ここにCSVアップロードの処理を書きます
        alert('ファイルがアップロードされました');
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