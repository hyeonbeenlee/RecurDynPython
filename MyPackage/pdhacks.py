import pandas as pd
import glob
import matplotlib.pyplot as plt

def Cut(DF: pd.DataFrame, strColumnName: str, Start: float, End: float):
    DF = DF[Start <= DF[strColumnName]]
    DF = DF[DF[strColumnName] <= End]
    DF = DF.reset_index(drop=True)
    return DF

def Shift(DF: pd.DataFrame, strColumnName: str, ShiftValue: float):
    DF[strColumnName] += ShiftValue
    return DF

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