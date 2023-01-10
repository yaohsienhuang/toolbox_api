import os
import json
import pathlib
from typing import Union
from fastapi import APIRouter, Query
from starlette.requests import Request
from ..init_logger import logger
from ..utils.FileProcessing import FileProcessing

router = APIRouter()

@router.post('/replace_filename_fragment', tags=['File operations'])
@logger.catch_router
def replace_filename_fragment(
    request: Request,
    path: Union[str, pathlib.Path] = Query(default='/tf/cp1ai01/A', description="填入路徑 (A)"),
    extension: str = Query(default='jpg', description="填入file的extension, any : 全部"),
    replace_dict: dict={'#OK2':'#OK'}
):
    '''
    - 主要功能 : filename 中符合 replace_dict.key 者，以 replace_dict.value 取代
    '''
    path = os.path.normpath(path.strip('\u202a'))

    status, message = FileProcessing.replace_filename_fragment(
        path=path,
        extension=extension,
        replace_dict=replace_dict
    )

    return {
        'status': 'success' if status == True else 'error',
        'message': message
    }
