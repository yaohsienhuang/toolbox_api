import os
import numpy as np
import pandas as pd
import math
import random
import shutil
import xml.etree.ElementTree as ET
from ..init_logger import logger


class FileProcessing:

    file_list = list()
    file_nums = 0

    @classmethod
    def get_file_list(cls, path:str, extension:str):
        file_list = []
        for maindir, subdir, file_name_list in os.walk(path):
            for filename in file_name_list:
                fullPath = os.path.join(maindir, filename)
                ext = fullPath.split('.')[-1]
                if (ext == extension)|(extension=='any'):
                    file_list.append(fullPath)
        return file_list

    @classmethod
    @logger.catch
    def file_transfer_with_frac(cls, source:str, target:str, extension:str, f:float=1, mode:str='copy', replace_dict:dict=dict()):
        file_list = cls().get_file_list(source, extension)
        cls.file_list, cls.file_nums = file_list, len(file_list)
        yield f'total file(.{extension})={cls.file_nums}'
        choiced_num = int(round(cls.file_nums*float(f), 0))
        choiced_list = np.random.choice(
            cls.file_list, choiced_num, replace=False)
        yield f'ramdom smaple={choiced_num}/{cls.file_nums}'
        cnt = 0
        pass_cnt = 0
        for path in choiced_list:
            try:
                subdirs = path.replace(path, '')
                if replace_dict:
                    for word, replacement in replace_dict.items():
                        subdirs = subdirs.replace(word, replacement)
                target_path = target+os.path.split(subdirs)[0]+os.sep
                if not os.path.isdir(target_path):
                    os.makedirs(target_path, exist_ok=True)
                if mode == 'move':
                    shutil.move(path, target_path)
                if mode == 'copy':
                    shutil.copy(path, target_path)

            except:
                pass_cnt += 1

            finally:
                cnt += 1
                
        msg = f'completed/pass_cnt/total={cnt}/{pass_cnt}/{choiced_num}'
        yield msg
        cls.file_list = list()
        cls.file_nums = 0
        
        return msg

    @classmethod
    @logger.catch
    def file_transfer_with_n(cls, source:str, target:str, extension:str, n:int, mode:str='copy', replace_dict:dict=dict()):
        file_list = cls().get_file_list(source, extension)
        cls.file_list, cls.file_nums = file_list, len(file_list)
        yield f'total file(.{extension})={cls.file_nums}'
        choiced_num = int(n)
        choiced_list = np.random.choice(
            cls.file_list, choiced_num, replace=False)
        yield f'ramdom smaple={choiced_num}/{cls.file_nums}'
        cnt = 0
        pass_cnt = 0
        for path in choiced_list:
            try:
                subdirs = path.replace(path, '')
                if replace_dict:
                    for word, replacement in replace_dict.items():
                        subdirs = subdirs.replace(word, replacement)
                target_path = target+os.path.split(subdirs)[0]+os.sep
                if not os.path.isdir(target_path):
                    os.makedirs(target_path, exist_ok=True)
                if mode == 'move':
                    shutil.move(path, target_path)
                if mode == 'copy':
                    shutil.copy(path, target_path)

            except:
                pass_cnt += 1

            finally:
                cnt += 1
                
        msg = f'completed/pass_cnt/total={cnt}/{pass_cnt}/{choiced_num}'
        yield msg
        cls.file_list = list()
        cls.file_nums = 0
            
        return msg
    
    @classmethod
    @logger.catch
    def merge_dirs(cls,sources:str,target:str,mode:str):
        target=os.path.normpath(target)+os.sep
        nums=len(sources)
        cnt=0
        for source in sources:
            source=os.path.normpath(source)+os.sep
            status, message = cls().file_transfer_with_frac(
                source=source,
                target=target,
                extension='any',
                f=1,
                mode='move',
                replace_dict=dict()
            )
            cnt+=1
            yield f'source={source}, target={target}, status={status}, msg={message}'
        return f'completed={cnt}/{nums}'
    
    @classmethod
    @logger.catch
    def split_folder_with_n(cls,source:str,target:str,n:int,mode:str,start_num:int):
        '''sample:
        file_processor=fileProcessing(path='/tf/cp1ai01/COG/03_POC訓練資料/backup/split_test/test')
        file_processor.split_folder_with_n(
            n=500,
            target='/tf/cp1ai01/COG/03_POC訓練資料/object_detection/FM_model-preparing',
            mode='move',
            start_num=1
        )
        '''
        target=os.path.normpath(target)+os.sep
        file_list = cls().get_file_list(source, 'any')
        cls.file_list, cls.file_nums = file_list, len(file_list)
        yield f'total file(any)={cls.file_nums}'
   
        folder_nums=math.ceil(cls.file_nums/n)
        yield f'Each folders contains {n} pcs -> {cls.file_nums} pcs should split to {folder_nums} folders.'
        random.shuffle(cls.file_list)
        folder_cnt=start_num
        cnt=0
        for i in range(cls.file_nums):
            path=cls.file_list[i]
            subdir=os.path.split(path)[0].split(os.sep)[-1]
            target_path=target+f'{subdir}-{folder_cnt}'+os.sep
            if not os.path.isdir(target_path):
                os.makedirs(target_path,exist_ok=True)
            if mode=='move':
                shutil.move(path,target_path)
            elif mode=='copy':
                shutil.copy(path,target_path)
            cnt+=1
            if cnt%n==0:
                yield f'completed={folder_cnt}/{folder_nums}'
                folder_cnt+=1
        return f'completed={folder_cnt}/{folder_nums}'
    
    @classmethod
    @logger.catch
    def read_xml_label_counts(cls,path):
        file_list = cls().get_file_list(path, 'xml')
        result=[]
        for xml in file_list:
            tree = ET.parse(xml)
            root = tree.getroot()
            for elem in root:
                if elem.tag=='object':
                    name = elem.find('name').text
                    result.append(name)
        values, counts = np.unique(result, return_counts=True)
        msg=dict(zip(values,counts))
        yield f'label counts={msg}'
        return msg
                
    @classmethod
    @logger.catch
    def extract_image_xml_both_exist(cls,source,target,mode,image_extension='JPG'):
        target=os.path.normpath(target)+os.sep
        file_list = cls().get_file_list(source, 'xml')
        total_n=len(file_list)*2
        cnt=0
        for path in file_list:
            if not os.path.isdir(target):
                os.makedirs(target,exist_ok=True)
            image_path=path.replace('.xml', f'.{image_extension}')
            if mode=='move':
                shutil.move(path,target)
                shutil.move(image_path,target)
            elif mode=='copy':
                shutil.copy(path,target)
                shutil.copy(image_path,target)
            cnt+=2
        yield f'completed={cnt}/{total_n}'
        return f'completed={cnt}/{total_n}'
        
            
        

            
