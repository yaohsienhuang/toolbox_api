import os
import json
import pathlib
from typing import Union
from fastapi import APIRouter, Query
from starlette.requests import Request
from ..init_logger import logger
from ..utils.FileProcessing import FileProcessing

router = APIRouter()

@router.post('/file_split_folder_with_n', tags=['File operations'])
@logger.catch_router
def file_split_folder_with_n(
    request: Request,
    source_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/A', description="填入路徑 (A)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/C', description="填入路徑 (splits to C subdirs with n)"),
    n: int = Query(default=500, description="每個 subdir 的數量"),
    copy_mode: bool = Query(default=False, description="True : copy, False : move"),
    start_num: int = Query(default=1, description="subdir 附加的字串, ex: A-1, A-2..."),
):
    '''
    - 主要功能：資料夾分拆 (A splits to C subdirs with n)
    '''
    source_path = os.path.normpath(source_path.strip('\u202a'))
    target_path = os.path.normpath(target_path.strip('\u202a'))
    mode = 'copy' if copy_mode else 'move'

    status, message = FileProcessing.split_folder_with_n(
        source=source_path,
        target=target_path,
        n=n,
        mode=mode,
        start_num=start_num
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
