import os
import re
import torch
import pandas as pd
import glob


def Sec2Time(seconds):
    Hr = int(seconds // 3600)
    seconds -= Hr * 3600
    Min = int(seconds // 60)
    seconds -= Min * 60
    Sec = seconds
    return Hr, Min, int(Sec)


def CreateDir(DirectoryPath):
    if not os.path.exists(DirectoryPath):
        os.makedirs(DirectoryPath)
        print(f"Created new directory: {DirectoryPath}")
    else:
        pass

def NumFromStr(str):
    list_num = re.findall(r'\d+', str)
    return list_num

def df2tensor(df: pd.DataFrame):
    return torch.FloatTensor(df.to_numpy())

def path2filename(path:str):
    filefullname=os.path.basename(path)
    filename='.'.join(filefullname.split('.')[:-1])
    return filename

def Conv1D_Lout(Lin, padding, dilation, kernel_size, stride):
    Lout = int((Lin + 2 * padding - dilation * (kernel_size - 1) - 1) / stride)+1
    return Lout

def ubar2space(path):
    files=glob.glob(f"{path}\\**\*.pdf", recursive=True)
    for f in files:
        new_path=f"{os.path.dirname(f)}\\{os.path.basename(f).replace('_',' ')}"
        os.rename(f,new_path)