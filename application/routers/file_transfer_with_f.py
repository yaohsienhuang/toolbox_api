import os
import json
import pathlib
from typing import Union
from fastapi import APIRouter, Query
from starlette.requests import Request
from ..init_logger import logger
from ..utils.FileProcessing import FileProcessing

router = APIRouter()

@router.post('/file_transfer_with_f', tags=['File operations'])
def file_transfer_with_f(
    request: Request,
    source_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (from A)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (to B)"),
    extension: str = Query(default='jpg', description="填入file的extension, any : 全部"),
    f: float = Query(default=1, description="填入移動比例"),
    copy_mode: bool = Query(default=True, description="True : copy, False : move"),
    replace_dict: dict = json.dumps({})
):
    '''
    - 主要功能：部分比例資料轉移 (from A to B with ratio-f)
    - remarks : 
        (1) 部分比例經過隨機抽樣
        (2) replace_dict 可將 filename 中的字串做替換
        (3) target_path 若無此路徑會自度新增
    '''
    logger.pin(__name__, f'client_host_ip={request.client.host}')
    source_path = os.path.normpath(source_path.strip('\u202a'))
    target_path = os.path.normpath(target_path.strip('\u202a'))
    mode = 'copy' if copy_mode else 'move'
    logger.pin(
        __name__, f'source_path={source_path}; target_path={target_path}; f={f}; extension={extension}; mode={mode}; replace_dict={replace_dict}')

    status, message = FileProcessing.file_transfer_with_frac(
        source=source_path,
        target=target_path,
        extension=extension,
        f=f,
        mode=mode,
        replace_dict=replace_dict
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
