from fastapi import APIRouter
import os

router = APIRouter()

def get_file_list(directory: str):
    """
    指定されたディレクトリ内のファイルとサブディレクトリのリストを返す。
    """
    files = []
    full_path = os.path.abspath(directory)
    if os.path.exists(full_path) and os.path.isdir(full_path):
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            item_type = 'file' if os.path.isfile(item_path) else 'directory'
            files.append({
                "name": item,
                "path": item_path,
                "type": item_type
            })
        return files
    else:
        return {"error": "指定されたパスが存在しないか、ディレクトリではありません。"}