import React from 'react';
import DropdownMenu from './DropdownMenu';
import CustomAttributeForm from './CustomAttributeForm';
import IssuesForm from './IssuesForm';
import EditableTableForm from './EditableTableForm';
import CountTask from './CountTask';
import { AppBar, Toolbar, Typography } from '@mui/material';
import ErrorBoundary from './ErrorBoundary';

function App() {
    const [currentApi, setCurrentApi] = React.useState(null);

    const manageMenuItems = [
        { label: '稼働状況照会', api: 'editableTable' },
    ];

    const inquiryMenuItems = [
        { label: '課題一覧取得', api: 'countTask' },
    ];

    const userMenuItems = [
        { label: 'カスタム属性追加', api: 'customAttribute' },
    ];

    const projectMenuItems = [
        { label: 'プロジェクトユーザ追加', api: 'userAdd'},
        { label: 'プロジェクトユーザ削除', api: 'userDel'}
    ];

    return (
        <ErrorBoundary>
            <div>
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h5" style={{ flexGrow: 1 }}>
                            システム企画部　業務管理ツール
                        </Typography>
                        <DropdownMenu title="管理系" menuItems={manageMenuItems} setCurrentApi={setCurrentApi} />
                        <DropdownMenu title="照会系" menuItems={inquiryMenuItems} setCurrentApi={setCurrentApi} />
                        <DropdownMenu title="ユーザ操作系" menuItems={userMenuItems} setCurrentApi={setCurrentApi} />
                        <DropdownMenu title="プロジェクト操作系" menuItems={projectMenuItems} setCurrentApi={setCurrentApi} />
                    </Toolbar>
                </AppBar>
                {currentApi === 'customAttribute' && <CustomAttributeForm />}
                {currentApi === 'issues' && <IssuesForm />}
                {currentApi === 'editableTable' && <EditableTableForm />}
                {currentApi === 'countTask' && <CountTask />}
            </div>
        </ErrorBoundary>
    );
}

export default App;