import os
import json
import pathlib
from typing import Union
from fastapi import APIRouter, Query
from starlette.requests import Request
from ..init_logger import logger
from ..utils.FileProcessing import FileProcessing


router = APIRouter()


@router.post('/file_transfer_with_n', tags=['File operations'])
@logger.catch_router
def file_transfer_with_n(
    request: Request,
    source_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (from A)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (to B)"),
    extension: str = Query(default='jpg', description="填入file的extension, any : 全部"),
    n: int = Query(default=20000, description="填入移動數量"),
    copy_mode: bool = Query(default=True, description="True : copy, False : move"),
    replace_dict: dict = json.dumps({})
):
    '''
    - 主要功能：部分數量資料轉移 (from A to B with n)
    - remarks : 
        - (1) 部分數量經過隨機抽樣
        - (2) replace_dict 可將 filename 中的字串做替換
        - (3) target_path 若無此路徑會自度新增
        
    '''
    source_path = os.path.normpath(source_path.strip('\u202a'))
    target_path = os.path.normpath(target_path.strip('\u202a'))
    mode = 'copy' if copy_mode else 'move'

    status, message = FileProcessing.file_transfer_with_n(
        source=source_path,
        target=target_path,
        extension=extension,
        n=n,
        mode=mode,
        replace_dict=replace_dict
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
    
    
