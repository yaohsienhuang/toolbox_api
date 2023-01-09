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
        file_list = cls.get_file_list(source, extension)
        file_nums = len(file_list)
        yield f'total file(.{extension})={file_nums}'
        choiced_num = int(round(file_nums*float(f), 0))
        choiced_list = np.random.choice(
            file_list, choiced_num, replace=False)
        yield f'ramdom smaple={choiced_num}/{file_nums}'
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
                
        yield f'completed={cnt}; pass_cnt={pass_cnt}; sample={choiced_num}; total={file_nums}'
        
        return {
            'total':file_nums,
            'sample':choiced_num,
            'completed':cnt,
            'pass_cnt':pass_cnt,
        }

    @classmethod
    @logger.catch
    def file_transfer_with_n(cls, source:str, target:str, extension:str, n:int, mode:str='copy', replace_dict:dict=dict()):
        file_list = cls.get_file_list(source, extension)
        file_nums = len(file_list)
        yield f'total file(.{extension})={file_nums}'
        choiced_num = int(n)
        choiced_list = np.random.choice(
            file_list, choiced_num, replace=False)
        yield f'ramdom smaple={choiced_num}/{file_nums}'
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
                
        yield f'completed={cnt}; pass_cnt={pass_cnt}; sample={choiced_num}; total={file_nums}'
            
        return {
            'total':file_nums,
            'sample':choiced_num,
            'completed':cnt,
            'pass_cnt':pass_cnt,
        }
    
    @classmethod
    @logger.catch
    def merge_dirs(cls,sources:str,target:str,mode:str):
        target=target+os.sep
        nums=len(sources)
        cnt=0
        for source in sources:
            source=source+os.sep
            status, message = cls.file_transfer_with_frac(
                source=source,
                target=target,
                extension='any',
                f=1,
                mode=mode,
                replace_dict=dict()
            )
            cnt+=1
            yield f'source={source}, target={target}, status={status}, msg={message}'
            
        return {
            'total':nums,
            'completed':cnt,
        }
    
    @classmethod
    @logger.catch
    def split_folder_with_n(cls,source:str,target:str,n:int,mode:str,start_num:int):
        target=target+os.sep
        file_list = cls.get_file_list(source, 'any')
        file_nums = len(file_list)
        yield f'total file(any)={file_nums}'
   
        folder_nums=math.ceil(file_nums/n)
        yield f'Each folders contains {n} pcs -> {file_nums} pcs should split to {folder_nums} folders.'
        random.shuffle(file_list)
        folder_cnt=start_num
        cnt=0
        for i in range(file_nums):
            path=file_list[i]
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
        return {
            'total_dir':folder_nums,
            'completed_dir':folder_cnt
        }
    
    @classmethod
    @logger.catch
    def replace_filename_fragment(cls,path,extension,replace_dict):
        file_list = cls.get_file_list(path, extension)
        file_nums = len(file_list)
        yield f'total file(.{extension})={file_nums}'
        cnt=0
        for path in file_list:
            base_path=os.path.split(path)[0]
            new_filename=os.path.split(path)[-1]
            for key,values in replace_dict.items():
                new_filename = new_filename.replace(key,values)
            new_path =base_path + new_filename
            os.rename(path,new_path)
            cnt+=1
        yield f'completed={cnt}; total={file_nums}'
        return {
            'total':file_nums,
            'completed':cnt
        } 
        
    @classmethod
    @logger.catch
    def read_xml_label_counts(cls,path):
        file_list = cls.get_file_list(path, 'xml')
        result=[]
        for xml in file_list:
            tree = ET.parse(xml)
            root = tree.getroot()
            for elem in root:
                if elem.tag=='object':
                    name = elem.find('name').text
                    result.append(name)
        values, counts = np.unique(result, return_counts=True)
        msg=dict(zip(values,counts.tolist()))
        yield f'label counts={msg}'
        return msg
                
    @classmethod
    @logger.catch
    def extract_image_xml_both_exist(cls,source,target,mode,image_extension='JPG'):
        target=target+os.sep
        file_list = cls.get_file_list(source, 'xml')
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
            
        yield f'completed={cnt}; total={total_n}'
        
        return {
            'total':total_n,
            'completed':cnt
        }
        
    @classmethod
    @logger.catch
    def file_transfer_with_filename_fragment(cls,source,target,fragment,extension,mode):
        file_list = cls.get_file_list(source, extension)
        file_nums = len(file_list)
        cnt=0
        pass_cnt=0
        for path in file_list:
            try:
                filename=os.path.split(path)[-1]
                source_diff=path.replace(source,'')
                subdirs=os.path.split(source_diff)[0]
                if fragment in filename:
                    target_path=target+os.sep+subdirs+os.sep
                    if not os.path.isdir(target_path):
                        os.makedirs(target_path,exist_ok=True)
                    if mode=='move':
                        shutil.move(path,target_path)
                    elif mode=='copy':
                        shutil.copy(path,target_path)
                    cnt+=1

            except :
                pass_cnt+=1
                
        yield f'completed={cnt}; pass_cnt={pass_cnt}; total={file_nums}'
            
        return {
            'total':file_nums,
            'completed':cnt,
            'pass_cnt':pass_cnt,
        }
    
    @classmethod
    @logger.catch
    def replace_xml_object_name(cls,path,replace_dict):
        file_list = cls.get_file_list(path, 'xml')
        
        status, label_counts_before=cls.read_xml_label_counts(path)
        
        for file in file_list:
            tree = ET.parse(file)
            root = tree.getroot()
            name_elts = root.findall(".//name")
            for elt in name_elts:
                for key,values in replace_dict.items():
                    elt.text = elt.text.replace(key,values)
            tree.write(file)
                        
        status, label_counts_after=cls.read_xml_label_counts(path)
        
        yield f'before={label_counts_before}; after={label_counts_after}'
        
        return label_counts_after
    
    @classmethod
    @logger.catch
    def delete_xml_object_name(cls,path,remove_name):
        file_list = cls.get_file_list(path, 'xml')
        
        status, label_counts_before=cls.read_xml_label_counts(path)
        for file in file_list:
            tree = ET.parse(file)
            root = tree.getroot()
            for elt in root.findall('object'):
                if elt.find('name').text==remove_name:
                    root.remove(elt)
            tree.write(file)
            
        status, label_counts_after=cls.read_xml_label_counts(path)
        
        yield f'before={label_counts_before}; after={label_counts_after}'
        
        return label_counts_after
    
    @classmethod
    @logger.catch
    def move_file_and_xml_with_blank_object(cls,path,target,extension):
        if not os.path.isdir(target):
            os.makedirs(target,exist_ok=True)
        file_list=cls.get_file_list(path,'xml')
        file_nums=len(file_list)*2
        cnt=0
        for file in file_list:
            image_path=file.replace('.xml', f'.{extension}')
            tree = ET.parse(file)
            root = tree.getroot()
            objs = root.findall('object')
            if not objs:
                shutil.move(file,target)
                shutil.move(image_path,target)
                cnt+=2
                
        yield f'completed={cnt}; total={file_nums}'
            
        return {
            'total':file_nums,
            'completed':cnt,
        }
            
        
            
        

            
