import React, { useState } from 'react';

function CustomAttributeForm(){
    const [apiKey, setApiKey] = React.useState('');
    const [projectId, setProjectId] = React.useState('');
    const [typeId, setTypeId] = React.useState('');
    const [name, setName] = React.useState('');
    const [required, setRequired] = React.useState(false);
    const [itemString, setItemString] = React.useState('');

    const isTypeSelected = ['5','6','7','8'].includes(typeId);

    const [log, setLog] = React.useState(null);

    const handleSubmit = (e) => {
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

    return (
        <React.Fragment>
            <h1>カスタム属性追加ツール</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="apiKey">APIキー(必須)：</label><br/>
                <input type="text" id="apiKey" value={apiKey} onChange={e => setApiKey(e.target.value)} /><br/>

                <label htmlFor="projectId">プロジェクトID（必須）：</label><br/>
                <input type="text" id="projectId" value={projectId} onChange={e => setProjectId(e.target.value)} /><br/>
            
                <label htmlFor="typeId">属性タイプ（必須）：</label><br/>
                <select id="typeId" value={typeId} onChange={e => setTypeId(e.target.value)}>
                    <option value="">選択してください</option>
                    <option value="1">文字列</option>
                    <option value="2">文章</option>
                    <option value="3">数値</option>
                    <option value="4">日付</option>
                    <option value="5">単一リスト</option>
                    <option value="6">複数リスト</option>
                    <option value="7">チェックボックス</option>
                    <option value="8">ラジオ</option>
                </select><br/>
                <label htmlFor="name">属性名(必須):</label><br/>
                <input type="text" id="name" value={name} onChange={e => setName(e.target.value)} /><br/>
                {isTypeSelected && (
                    <div>
                        <label htmlFor="items">
                            項目： <small>※複数項目を定義する場合、「,」区切りで入力してください（例：リンゴ,みかん,バナナ）</small>
                        </label><br/>
                        <input
                            type="text"
                            id="items"
                            value={itemString}
                            onChange={(e) => setItemString(e.target.value)}
                        /><br/>
                    </div>
                )}
                <input type="checkbox" id="required" checked={required} onChange={e => setRequired(e.target.checked)} />
                <label htmlFor="required">属性の入力必須化</label><br/>
                <input class="submitButton" type="submit" value="カスタム属性作成" />
            </form>

            {log && (
                <div>
                    <h3>実行ログ:</h3>
                    {log.statusCode && (
                        <div>
                            <strong>HTTPリクエスト結果：</strong>{log.statusCode}
                        </div>
                    )}
                    {log.response && (
                        <div>
                            <strong>HTTPレスポンス:</strong>
                            <pre>{JSON.stringify(log.response, null, 2)}</pre>
                        </div>
                    )}
                </div>
            )}
        </React.Fragment>
    );
}


export default CustomAttributeForm;