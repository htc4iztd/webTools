import React, { useState, useEffect }  from 'react';
import animation from "./loading.gif";
import downloadImage from "./logo.svg";
import {
    Button,
    Modal,
    Fade,
    Backdrop,
  } from '@mui/material';
  

function FileUploadForm(){
    const [loading2, setLoading2] = useState(false);
    const [fileName, setFileName] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);

    const [openModal, setOpenModal] = React.useState(false);

    const handleOpenModal = () => {
        setOpenModal(true);
    };

    const handleCloseModal = () => {
        setOpenModal(false);
    };

    //MaterialUIを使ったファイルアップロードアイテム
    const FileUploadButton = ({ onFileSelect }) => {
        const inputRef = React.useRef();
    
        const handleClick = () => {
            inputRef.current.click();
        };
    
        const handleChange = (event) => {
            const file = event.target.files[0];
            if (file) {
                setFileName(file.name);
                setSelectedFile(file); // 選択されたファイルを状態に保存
                onFileSelect(file); // 親コンポーネントに選択されたファイルを渡す
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
        if (!selectedFile) {
            alert('ファイルを選択してください');
            return;
        }
    
        // ファイルをFormDataオブジェクトに追加
        const formData = new FormData();
        formData.append('file', selectedFile);

        // アップロード処理中の状態を表示
        setLoading2(true);
    
        try {
            // サーバーにファイルをPOST
            const response = await fetch('http://localhost:8000/api/uploadOperationData', {
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
            setLoading2(false);
        }
    };

    const handleFileSelect = (file) => {
        setSelectedFile(file);
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
                        <image src={downloadImage} alt="Image for explanation of CSV download." />
                    </div>
                </Fade>
            </Modal>
        );
    };

    return (
        <React.Fragment>
            <form onSubmit={handleUpdateCSV}>
                <h2>課題状況最新化機能</h2>
                <p>※本機能ではBacklogから取得した課題一覧のCSVをアップロードすることができます。（CSVのダウンロード方法は<a href="#" onClick={handleOpenModal}>こちら</a>）<br/>
                    　ここでCSVをアップロードすることで、最新の課題状況を反映することができます。<br/>
                    　処理終了には数分かかることもありますがご了承ください。また、処理中にページを閉じるなどはお控えください。<br/>
                    　必ずCSVは最新のものをダウンロードし、アップロードして下さい。 <br/>
                    　最終更新日時：2024/4/10 10:00:00
                </p>
                <FileUploadButton onFileSelect={handleFileSelect} />
                <input className="submitButton" type="submit" value="CSVアップロード" />
                <CsvDownloadModal open={openModal} handleClose={handleCloseModal} />
                {loading2 && <image src={animation} alt="ローディングアニメーション"/>}
            </form>
        </React.Fragment>
    );
}

export default FileUploadForm;