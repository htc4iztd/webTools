from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from databases import Database
from sqlalchemy import Table, Column, Integer, String, Float, Text, Date, DateTime, MetaData
from sqlalchemy.dialects.postgresql import insert
import pandas as pd
import logging

DATABASE_URL = "postgresql://syskiuser:syskipassword@127.0.0.1:5432/syskidatabase"
database = Database(DATABASE_URL)
metadata = MetaData()

router = APIRouter()

tasks = Table(
    "task", metadata,
    Column('id', Integer),
    Column('project_id', Integer),
    Column('project_name', String(100)),
    Column('key_id', Integer),
    Column('key', String(50)),
    Column('type_id', Integer),
    Column('type', String(30)),
    Column('category_id', Integer),
    Column('category_name', String(10)),
    Column('subject', String(1000)),
    Column('description', Text),
    Column('status_id', Integer),
    Column('status', String(10)),
    Column('close_reason_id', Integer),
    Column('close_reason', String(10)),
    Column('incharge_id', Integer),
    Column('incharge', String(10)),
    Column('register_id', Integer),
    Column('register', String(10)),
    Column('register_date', DateTime),
    Column('parent_task_key', Integer),
    Column('deadline', Date),
    Column('changer_id', Integer),
    Column('changer', String(10)),
    Column('change_date', DateTime),
    Column('attached', Integer),
    Column('system_under_consideration', String(30)),
    Column('system_tobe_consideration', String(30)),
    Column('quarters', Integer),
    Column('issues_type', String(10)),
    Column('issues_seq_no', String(10)),
    Column('require_doc_capture_necessity', String(10)),
    Column('require_doc_capture_version', Float)
)

@router.post("/uploadOperationData")
async def upload_operation_data(file: UploadFile = File(...)):
    try:
        if not database.is_connected:
            logging.error("DatabaseBackend is not connected. Trying to connect...")
            await database.connect()

        # エンコーディングの自動検出
        import chardet
        raw_data = file.file.read()
        result = chardet.detect(raw_data)
        file_encoding = result['encoding']

        # ファイルを再度読み込み（ファイルポインタを先頭に戻す必要があります）
        file.file.seek(0)
        dataframe = pd.read_csv(file.file, encoding=file_encoding)

        # NaN値を適切なデフォルト値に置き換え
        dataframe = dataframe.fillna({
            'ID': 0,
            'プロジェクトID': 0,
            'プロジェクト名': '',
            'キーID': 0,
            'キー': '',
            '種別ID': 0,
            '種別': '',
            'カテゴリーID': 0,
            'カテゴリー名': '',
            '件名': '',
            '詳細': '',
            '状態ID': 0,
            '状態': '',
            '完了理由ID': 0,
            '完了理由': '',
            '担当者ID': 0,
            '担当者': '',
            '登録者ID': 0,
            '登録者': '',
            '登録日': '1970-01-01',  # 適切なデフォルト日付
            '親課題キー': 0,
            '期限日': '1970-01-01',  # 適切なデフォルト日付
            '更新者ID': 0,
            '更新者': '',
            '更新日': '1970-01-01',  # 適切なデフォルト日付
            '添付': 0,
            '検討元システム': '',
            '検討先システム': '',
            '四半期': 0,
            '案件種別': '',
            '案件SEQ No.': '',
            '要求定義書取込要否': '',
            '要求定義書取込版数': 0.0
        })
        
        from io import StringIO
        import os

        # Pandasの表示設定を調整
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.expand_frame_repr', False)
        
        output_directory = "/home/admin/webTools"
        os.makedirs(output_directory, exist_ok=True)
        
        dataframe_str = dataframe.to_string()
        
        buffer = StringIO()
        dataframe.info(buf=buffer)
        info_str = buffer.getvalue()
        
        dataframe_file_path = os.path.join(output_directory, "dataframe_contents.txt")
        with open(dataframe_file_path, "w", encoding="utf-8") as f:
            f.write(dataframe_str)
        logging.info(f"DataFrame contents written to {dataframe_file_path}")
        
        # データフレームの情報をファイルに出力
        info_file_path = os.path.join(output_directory, "dataframe_info.txt")
        with open(info_file_path, "w", encoding="utf-8") as f:
            f.write(info_str)
        logging.info(f"DataFrame info written to {info_file_path}")

        for _, row in dataframe.iterrows():
            try:
                query = insert(tasks).values(
                    id=int(row['ID']),
                    project_id=int(row['プロジェクトID']),
                    project_name=str(row['プロジェクト名']),
                    key_id=int(row['キーID']),
                    key=str(row['キー']),
                    type_id=int(row['種別ID']),
                    type=str(row['種別']),
                    category_id=int(row['カテゴリーID']),
                    category_name=str(row['カテゴリー名']),
                    subject=str(row['件名']),
                    description=str(row['詳細']),
                    status_id=int(row['状態ID']),
                    status=str(row['状態']),
                    close_reason_id=int(row['完了理由ID']),
                    close_reason=str(row['完了理由']),
                    incharge_id=int(row['担当者ID']),
                    incharge=str(row['担当者']),
                    register_id=int(row['登録者ID']),
                    register=str(row['登録者']),
                    register_date=pd.to_datetime(row['登録日'], errors='coerce'),
                    parent_task_key=int(row['親課題キー']),
                    deadline=pd.to_datetime(row['期限日'], errors='coerce').date(),
                    changer_id=int(row['更新者ID']),
                    changer=str(row['更新者']),
                    change_date=pd.to_datetime(row['更新日'], errors='coerce'),
                    attached=int(row['添付']),
                    system_under_consideration=str(row['検討元システム']),
                    system_tobe_consideration=str(row['検討先システム']),
                    quarters=int(row['四半期']),
                    issues_type=str(row['案件種別']),
                    issues_seq_no=str(row['案件SEQ No.']),
                    require_doc_capture_necessity=str(row['要求定義書取込要否']),
                    require_doc_capture_version=float(row['要求定義書取込版数'])
                ).on_conflict_do_update(
                    index_elements=['id'],
                    set_=dict(
                        project_id=int(row['プロジェクトID']),
                        project_name=str(row['プロジェクト名']),
                        key_id=int(row['キーID']),
                        key=str(row['キー']),
                        type_id=int(row['種別ID']),
                        type=str(row['種別']),
                        category_id=int(row['カテゴリーID']),
                        category_name=str(row['カテゴリー名']),
                        subject=str(row['件名']),
                        description=str(row['詳細']),
                        status_id=int(row['状態ID']),
                        status=str(row['状態']),
                        close_reason_id=int(row['完了理由ID']),
                        close_reason=str(row['完了理由']),
                        incharge_id=int(row['担当者ID']),
                        incharge=str(row['担当者']),
                        register_id=int(row['登録者ID']),
                        register=str(row['登録者']),
                        register_date=pd.to_datetime(row['登録日'], errors='coerce'),
                        parent_task_key=int(row['親課題キー']),
                        deadline=pd.to_datetime(row['期限日'], errors='coerce').date(),
                        changer_id=int(row['更新者ID']),
                        changer=str(row['更新者']),
                        change_date=pd.to_datetime(row['更新日'], errors='coerce'),
                        attached=int(row['添付']),
                        system_under_consideration=str(row['検討元システム']),
                        system_tobe_consideration=str(row['検討先システム']),
                        quarters=int(row['四半期']),
                        issues_type=str(row['案件種別']),
                        issues_seq_no=str(row['案件SEQ No.']),
                        require_doc_capture_necessity=str(row['要求定義書取込要否']),
                        require_doc_capture_version=float(row['要求定義書取込版数'])
                    )
                )
                await database.execute(query)
            except ValueError as e:
                logging.error(f"ValueError: {str(e)} for row {row.to_dict()}")
                continue

        return JSONResponse(status_code=200, content={"message": "Data uploaded successfully"})
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        return JSONResponse(status_code=400, content={"message": str(e)})