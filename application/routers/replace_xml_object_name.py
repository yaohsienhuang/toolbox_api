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

@router.post('/replace_xml_object_name', tags=['XML operations'])
@logger.catch_router
def replace_xml_object_name(
    request: Request,
    path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/A', description="填入路徑 (A)"),
    replace_dict: dict={'OK2':'OK'}
):
    '''
    - 主要功能：讀取 XML 中的 object name, 若符合 replace_dict 中的 key 則用 value 取代之
    '''
    path = os.path.normpath(path.strip('\u202a'))

    status, message = FileProcessing.replace_xml_object_name(
        path=path,
        replace_dict=replace_dict
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
