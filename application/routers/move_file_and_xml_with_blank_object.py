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

@router.post('/move_file_and_xml_with_blank_object', tags=['XML operations'])
def move_file_and_xml_with_blank_object(
    request: Request,
    source_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (from A)"),
    target_path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/...', description="填入路徑 (to B)"),
    extension: str = Query(default='jpg', description="填入 image 的 extension"),
):
    '''
    - 主要功能：讀取 XML 中有無 oject label，若無則將其移至 target dir
    '''
    logger.pin(__name__, f'client_host_ip={request.client.host}')
    path = os.path.normpath(path.strip('\u202a'))
    logger.pin(
        __name__, f'path={path}')

    status, message = FileProcessing.move_file_and_xml_with_blank_object(
        path=source_path,
        target=target_path,
        extension=extension
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
