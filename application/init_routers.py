import os
import importlib
from .utils.FileProcessing import FileProcessing

def init_routers(app,path):
    routers=FileProcessing.get_file_list(path=path,extension='py')
    for router in routers:
        router_name=os.path.basename(router).split('.')[0]
        router_=importlib.import_module(f'application.routers.{router_name}')
        app.include_router(router_.router)