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

@router.post('/extract_image_xml_both_exist', tags=['XML operations'])
def extract_image_xml_both_exist(
    request: Request,
    source_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/A', description="填入路徑 (from A)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/B', description="填入路徑 (to B)"),
    copy_mode: bool = Query(default=False, description="True : copy, False : move"),
    extension: str = Query(default='jpg', description="填入 image 的 extension, replacing xml to jpg"),
):
    '''
    - 主要功能：移動同時存在 image 與 XML 的檔案
    '''
    logger.pin(__name__, f'client_host_ip={request.client.host}')
    source_path = os.path.normpath(source_path.strip('\u202a'))
    target_path = os.path.normpath(target_path.strip('\u202a'))
    mode = 'copy' if copy_mode else 'move'
    logger.pin(
        __name__, f'source_path={source_path}; target_path={target_path}; extension={extension}; mode={mode}')

    status, message = FileProcessing.extract_image_xml_both_exist(
        source=source_path,
        target=target_path,
        mode=mode,
        image_extension=extension
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
