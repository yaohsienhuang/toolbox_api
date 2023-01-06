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

@router.post('/read_xml_label_counts', tags=['XML operations'])
def read_xml_label_counts(
    request: Request,
    path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/A', description="填入路徑 (A)"),
):
    '''
    - 主要功能：讀取 XML 中的 object name, 並計算 label counts
    '''
    logger.pin(__name__, f'client_host_ip={request.client.host}')
    path = os.path.normpath(path.strip('\u202a'))
    logger.pin(
        __name__, f'path={path}')

    status, message = FileProcessing.read_xml_label_counts(
        path=path,
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
