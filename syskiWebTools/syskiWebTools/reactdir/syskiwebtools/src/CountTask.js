import React from 'react';

function CountTask(){
    function handleSubmitTasks(e) {
        e.preventDefault();
        // ここでタスク提出のロジックを処理します
    }
    
    return (
        <React.Fragment>
            <h1>稼働状況照会ツール</h1>
            <form onSubumit={handleSubmitTasks}>
                <h2>課題数最新化</h2>
                <p>※正確な稼働管理のために都度課題数の最新化をする機能です。稼働管理表の利用前に押下してください</p>
                <input class="submitButton" type="submit" value="課題数の最新化" />
            </form>
            <br/>
        </React.Fragment>
    )
}

export default CountTask;