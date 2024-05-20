import React from 'react';
import DropdownMenu from './DropdownMenu';
import CustomAttributeForm from './CustomAttributeForm';
import IssuesForm from './IssuesForm';
import EditableTableForm from './EditableTableForm';
import FileUploadForm from './FileUploadForm';
import CountTask from './CountTask';
import { AppBar, Toolbar, Typography } from '@mui/material';
import ErrorBoundary from './ErrorBoundary';

function App() {
    const [currentApi, setCurrentApi] = React.useState(null);

    const manageMenuItems = [
        { label: '稼働状況照会', api: 'editableTable' },
        { label: '各種ファイルアップロード', api: 'fileUpload'},
    ];

    const userMenuItems = [
        { label: 'カスタム属性追加', api: 'customAttribute' },
    ];

    return (
        <ErrorBoundary>
            <div>
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h5" style={{ flexGrow: 1 }}>
                            システム企画部　業務管理ツール
                        </Typography>
                        <DropdownMenu title="案件管理系" menuItems={manageMenuItems} setCurrentApi={setCurrentApi} />
                        <DropdownMenu title="バックログ系" menuItems={userMenuItems} setCurrentApi={setCurrentApi} />
                    </Toolbar>
                </AppBar>
                {currentApi === 'customAttribute' && <CustomAttributeForm />}
                {currentApi === 'issues' && <IssuesForm />}
                {currentApi === 'editableTable' && <EditableTableForm />}
                {currentApi === 'fileUpload' && <FileUploadForm />}
                {currentApi === 'countTask' && <CountTask />}
            </div>
        </ErrorBoundary>
    );
}

export default App;
