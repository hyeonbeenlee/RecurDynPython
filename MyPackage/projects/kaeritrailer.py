import pandas as pd

def ReadExpTrailer(ExpDataPath):
    ExpData = pd.read_csv(ExpDataPath, skiprows=[0, 1, 3, 4, 5, 6, 7], index_col=0)
    ExpData = ExpData.rename({"Unnamed: 1": "Time"}, axis=1)
    ExpData = ExpData.fillna(0)
    
    ExpData = ExpData[
        ['Time', 'A1Z', 'A2Z', 'A3Z', 'A6Z', 'A7Z', 'A8Z', 'A9Z', 'A10Z', 'A11Z', 'A12Z', 'A13X', 'A13Y', 'A13Z', 'A14X', 'A14Y', 'A14Z', 'A15X',
         'A15Y', 'A15Z', 'A16X', 'A16Y', 'A16Z', 'A17X', 'A17Y', 'A17Z', 'A18X', 'A18Y', 'A18Z', 'A19X', 'A19Y', 'A19Z', 'A20X', 'A20Y', 'A20Z',
         'A21X', 'A21Y', 'A21Z', 'A22X', 'A22Y', 'A22Z', 'A23X', 'A23Y', 'A23Z', 'A24X', 'A24Y', 'A24Z', 'A25Z', 'A26Z', 'A27X', 'A27Y', 'A27Z',
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
            visualize.PlotTemplate(15)
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