import os
import json
import pathlib
from typing import List
from typing import Union
from fastapi import APIRouter, Query
from starlette.requests import Request
from ..init_logger import logger
from ..utils.FileProcessing import FileProcessing

router = APIRouter()

@router.post('/merge_dirs', tags=['File operations'])
@logger.catch_router
def merge_dirs(
    request: Request,
    source_path: List[str] = Query(default=['/tf/cp1ai01/A/', '/tf/cp1ai01/B/'], description="填入路徑 List (from A, B)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/C/..', description="填入路徑 (to C)"),
    copy_mode: bool = Query(default=False, description="True : copy, False : move"),
):
    '''
    - 主要功能：資料夾合併 (from A, B to C)
    - remarks : 
        (1) 全部 extension 進行轉移 (move)
    '''
    source_path = [os.path.normpath(sour.strip('\u202a')) for sour in source_path]
    target_path = os.path.normpath(target_path.strip('\u202a'))
    mode = 'copy' if copy_mode else 'move'

    status, message = FileProcessing.merge_dirs(
        sources=source_path,
        target=target_path,
        mode=mode
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
