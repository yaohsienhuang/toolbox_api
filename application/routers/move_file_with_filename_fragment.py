import os
import json
import pathlib
from typing import Union
from fastapi import APIRouter, Query
from starlette.requests import Request
from ..init_logger import logger
from ..utils.FileProcessing import FileProcessing


router = APIRouter()


@router.post('/file_transfer_with_filename_fragment', tags=['File operations'])
@logger.catch_router
def file_transfer_with_filename_fragment(
    request: Request,
    source_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (from A)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (to B)"),
    extension: str = Query(default='any', description="填入file的extension, any : 全部"),
    fragment: str = Query(default='DM74D1', description="填入 fragment 字串 (when fragment in filename) "),
    copy_mode: bool = Query(default=False, description="True : copy, False : move"),
):
    '''
    - 主要功能：當 filename 包含指定字串進行資料轉移 (from A to B when fragment in filename)
    '''
    source_path = os.path.normpath(source_path.strip('\u202a'))
    target_path = os.path.normpath(target_path.strip('\u202a'))
    mode = 'copy' if copy_mode else 'move'

    status, message = FileProcessing.file_transfer_with_filename_fragment(
        source=source_path,
        target=target_path,
        fragment=fragment,
        extension=extension,
        mode=mode
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
    
    
