import glob
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error
import itertools
from scipy.stats.qmc import LatinHypercube as LHC
import gc
from scipy.signal import butter, filtfilt, sosfiltfilt
import re
import matplotlib as mpl

def PlotTemplate(fontsize):
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['mathtext.fontset'] = 'stix'
    # plt.rcParams['text.usetex']=True

def Cut(DF: pd.DataFrame, strColumnName: str, Start: float, End: float):
    DF = DF[Start <= DF[strColumnName]]
    DF = DF[DF[strColumnName] <= End]
    DF = DF.reset_index(drop=True)
    return DF

def Shift(DF: pd.DataFrame, strColumnName: str, ShiftValue: float):
    DF[strColumnName] += ShiftValue
    return DF

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

def ReadExpTrailer(ExpDataPath):
    ExpData = pd.read_csv(ExpDataPath, skiprows=[0, 1, 3, 4, 5, 6, 7], index_col=0)
    ExpData = ExpData.rename({"Unnamed: 1": "Time"}, axis=1)
    ExpData = ExpData.fillna(0)
    
    ExpData = ExpData[['Time', 'A1Z', 'A2Z', 'A3Z', 'A6Z', 'A7Z', 'A8Z',
                       'A9Z', 'A10Z', 'A11Z', 'A12Z', 'A13X', 'A13Y', 'A13Z', 'A14X', 'A14Y',
                       'A14Z', 'A15X', 'A15Y', 'A15Z', 'A16X', 'A16Y', 'A16Z', 'A17X', 'A17Y',
                       'A17Z', 'A18X', 'A18Y', 'A18Z', 'A19X', 'A19Y', 'A19Z', 'A20X', 'A20Y',
                       'A20Z', 'A21X', 'A21Y', 'A21Z', 'A22X', 'A22Y', 'A22Z', 'A23X', 'A23Y',
                       'A23Z', 'A24X', 'A24Y', 'A24Z', 'A25Z', 'A26Z', 'A27X', 'A27Y', 'A27Z',
                       'A29X', 'A29Y', 'A29Z', 'A30Z', 'A31Z', 'A32Z', 'A33X', 'A33Y', 'A33Z']]
    ExpData.iloc[:, 1:] *= 9806.65  # g -> mm/s^2
    ExpData.iloc[:, 1:] /= 1000  # mm/s^2 -> m/s^2
    return ExpData

def ConcatCSV(csvpath: str, timecut: tuple = (), shift: float = 0,
              interpolate: bool = False, inc_samplerate:int=1, col_linear: list = None, col_pad: list = None, col_akima:list=None,
              plot:bool=False):
    """csvpath 경로 내의 csv파일들을 전부 병합하여 1개의 DataFrame으로 반환"""
    DataPathLists = glob.glob(csvpath + "\*.csv")
    DataCSV = []
    for idx_data,datapath in enumerate(DataPathLists):
        Data = pd.read_csv(datapath, index_col=0)
        if timecut:
            Data = Cut(Data, "TIME", timecut[0], timecut[1])
            Data = Shift(Data, 'TIME', shift)
        if interpolate:
            Data = Interp_IntervalBase(Data, inc_samplerate,col_linear,col_pad)
            # Data=Interp_StdBase(Data,inc_samplerate,col_linear,col_pad,col_akima,0.3)
        DataCSV.append(Data)
        if plot:
            PlotTemplate(15)
            fig,ax=plt.subplots(3,1,figsize=(10,7))
            ax[0].plot(Data['TIME'],Data['Pos_PSI@Rod2'],'-o')
            ax[1].plot(Data['TIME'],Data['Vel_RZ@Rod2'],'-o')
            ax[2].plot(Data['TIME'],Data['Acc_RZ@Rod2'],'-o')
            fig.tight_layout()
            plt.show()
        if (idx_data+1)%100==0:
            print(f"Concatenation {idx_data+1}/{len(DataPathLists)}")
    Data = pd.concat(DataCSV)
    Data = Data.reset_index(drop=False)
    return Data

def ConcatCSV_FixDZ(csvpath: str):
    """특정 column의 값을 fix해서 반환"""
    DataPathLists = glob.glob(csvpath + "\*.csv")
    DispZ = ['Pos_TZ@Sensor_20', 'Pos_TZ@Sensor_51', 'Pos_TZ@Sensor_52', 'Pos_TZ@Sensor_53']
    DataCSV = []
    for datapath in DataPathLists:
        Data = pd.read_csv(datapath, index_col=0)
        DataFileName = os.path.basename(datapath)
        # Data['ScaleVX'] = float(DataFileName[7:10])
        # Data['ScaleVY'] = float(DataFileName[-7:-4])
        # Data['F1(Ex_Scale_VX)@ExRq5'] = float(DataFileName[7:11])
        # Data['F2(Ex_Scale_VY)@ExRq5'] = float(DataFileName[-8:-4])
        
        for dispZcolumn in DispZ:
            Data[dispZcolumn].iloc[:399] = Data[dispZcolumn].iloc[399]
            Data[dispZcolumn] += 555.2562
        
        DataCSV.append(Data)
    
    Data = pd.concat(DataCSV, axis=0)
    Data = Data.reset_index(drop=True)
    return Data

def ConcatCSV_AE(csvpath: str):
    """csvpath 경로 내의 csv파일들을 전부 병합하여 1개의 DataFrame으로 반환"""
    DataPathLists = glob.glob(csvpath + "\*.csv")
    Sample = pd.read_csv(DataPathLists[0], index_col=0)
    NumData = len(DataPathLists)
    NumTimeSteps = Sample.shape[0]
    NumFeatures = Sample.shape[1]
    Tensor = torch.zeros((NumData, NumFeatures, NumTimeSteps))
    
    for idx, datapath in enumerate(DataPathLists):
        Data = pd.read_csv(datapath, index_col=0).transpose()
        Tensor[idx, :, :] = torch.tensor(Data.values, dtype=torch.float32)
    return Tensor


def Difference(DF: pd.DataFrame, TargetColumns: list):
    """특정 column의 행방향 차이를 계산하여 반환"""
    FixColumns = DF[TargetColumns].diff(periods=1)
    FixColumns = FixColumns.shift(periods=-1)
    DF[TargetColumns] = FixColumns
    DF = DF.fillna(0)
    return DF


def Shuffle(DF: pd.DataFrame, SeedNum: int = 777):
    np.random.seed(SeedNum)
    DF = DF.sample(frac=1)
    return DF

def Split(DF: pd.DataFrame, *args):
    """args에 주어진 비율대로 DF를 행으로 분할하여 리스트로 반환한다"""
    SplitDFList = []
    DFLength = DF.shape[0]
    StartIndex = 0
    for idx, rate in enumerate(args):
        DeltaIndex = int(rate * DFLength)
        EndIndex = StartIndex + DeltaIndex
        if idx == (len(args) - 1) and EndIndex < DFLength:
            EndIndex = DFLength
        SplitDFList.append(DF.iloc[StartIndex:EndIndex, :])
        StartIndex += DeltaIndex
    return SplitDFList

def FactorialSampler(LevelList, NumFeatures: int):
    Cases = itertools.product(LevelList, repeat=NumFeatures)
    Samples = np.empty((len(LevelList) ** NumFeatures, NumFeatures))
    for idx, case in enumerate(Cases):
        Samples[idx, :] = case
    return Samples

def LHCSampler(NumSamples, NumFeatures: int, seed: int = None):
    Sampler = LHC(d=NumFeatures, centered=False, seed=seed)
    ScaleSet = Sampler.random(n=NumSamples)  # LHC
    return ScaleSet

def Interp_StdBase(Data: pd.DataFrame, NumAdditionalPoints: int, Col_LinearInterpol: list, Col_PadInterpol: list, Col_AkimaInterpol: list, StdToleranceFactor: float = 1):
    len_old = Data.shape[0]
    for column in Data[Col_AkimaInterpol].columns:  # 응답 열에 대하여
        Std = Data[column].copy().std()
        print(f"DevBaseInterpolating {column}...")
        additional_rows = []
        for row in Data.index:  # 인덱스
            if row < Data.index[-1]:  # index~index+1
                if abs(Data[column].loc[row + 1] - Data[column].loc[row]) > Std * StdToleranceFactor and len(Data.loc[row:row + 1]) == 2:
                    # Add NAN row
                    additional_index = np.linspace(row, row + 1, NumAdditionalPoints + 2, endpoint=True)
                    additional_row = pd.DataFrame(data=None, index=additional_index, columns=Data.columns)  # to all columns
                    additional_row = additional_row.drop(index=[additional_index[0], additional_index[-1]])
                    additional_rows.append(additional_row)
    # Interpolate
    additional_rows = pd.concat(additional_rows, axis=0)  # NaN DF
    additional_rows = additional_rows.apply(pd.to_numeric, errors='coerce')  # NaN -> Numeric dtype
    Data = Data.append(additional_rows, ignore_index=False)
    Data = Data.sort_index()
    Data[Col_LinearInterpol] = Data[Col_LinearInterpol].interpolate(method='linear', axis=0)  # 시간 및 번호 열
    Data[Col_PadInterpol] = Data[Col_PadInterpol].interpolate(method='pad', axis=0)  # 파라미터 열
    Col_rest = [x for x in Data.columns if x not in Col_LinearInterpol + Col_PadInterpol]
    Data[Col_rest] = Data[Col_rest].interpolate(method='akima', axis=0)
    Data = Data.reset_index(drop=True)
    len_new = Data.shape[0]
    print(f"{len_new - len_old} data points added.")
    return Data

def Interp_IntervalBase(DF, NumAdditionalPoints, Col_LinearInterpol: list, Col_PadInterpol: list):
    additional_rows = []
    for row_idx, row in enumerate(DF.index):
        if row_idx < DF.index[-1]:
            additional_index = np.linspace(row, row + 1, NumAdditionalPoints + 2, endpoint=True)
            additional_row = pd.DataFrame(data=None, index=additional_index, columns=DF.columns)  # to all columns
            additional_row = additional_row.drop(index=[additional_index[0], additional_index[-1]])
            additional_rows.append(additional_row)
            if (row_idx + 1) % 1000 == 0:
                print(f"Interpolating {row_idx + 1}/{DF.index[-1]}")
    
    DF = pd.concat([DF] + additional_rows, axis=0)
    DF = DF.sort_index()
    
    for col in DF.columns:
        DF[col] = pd.to_numeric(DF[col], errors='coerce')
    DF[Col_LinearInterpol] = DF[Col_LinearInterpol].interpolate(method='linear', axis=0)
    DF[Col_PadInterpol] = DF[Col_PadInterpol].interpolate(method='pad', axis=0)  # 파라미터 열
    Col_rest = [x for x in DF.columns if x not in Col_LinearInterpol + Col_PadInterpol]
    DF[Col_rest] = DF[Col_rest].interpolate(method='akima', axis=0)
    DF = DF.reset_index(drop=True).dropna(axis=0)
    return DF

def FiltButterworth(data_1darray, cutoff, timestep, order, mode: str = 'low'):
    f_sampling = 1 / timestep
    nyq = f_sampling * 0.5
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, btype=mode, analog=False, output='sos')
    data_1darray = sosfiltfilt(sos, data_1darray)
    return data_1darray

def FFT(data_1Darray, timestep):
    n_samples = len(data_1Darray)
    Freq = np.fft.rfftfreq(n=n_samples, d=timestep)
    Amp = np.abs(np.fft.rfft(data_1Darray, n=n_samples, norm='forward')) * 2  # Magnitude, x2
    return Freq, Amp

def NumFromStr(str):
    list_num = re.findall(r'\d+', str)
    return list_num

def SaveAllActiveFigures(IndexingName:str="Figure"):
    if not os.path.exists("Figures"):
        os.mkdir("Figures")
    for fignum in plt.get_fignums():
        plt.figure(fignum)
        plt.savefig(f"Figures/{IndexingName}_{fignum:02d}.png",dpi=200, bbox_inches='tight')
        # plt.savefig(f"Figures/{fignum}.eps", format='eps')
        print(f"Figures/{IndexingName}_{fignum:02d}.png Saved.")

def ColorbarSubplot(colormapObj,figObj,vmin,vmax,position_ax, ylabel=None, fraction=0.05):
    """
    :param colormapObj: mpl.cm.plasma
    :return:
    """
    Cmap = colormapObj  # rainbow bwr
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cbar = figObj.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=Cmap), ax=position_ax,
                        fraction=fraction, ticks=np.linspace(vmin, vmax, 6, endpoint=True))
    cbar.axes1.set_ylabel(ylabel, rotation=270, labelpad=12)
    
def IncreaseLegendLinewidth(leg, linewidth:float=2):
    for legobj in leg.legendHandles:
        legobj.set_linewidth(linewidth)
        

if __name__ == '__main__':
    pass