import pandas as pd

def Interp_StdBase(Data: pd.DataFrame,
        NumAdditionalPoints: int,
        Col_LinearInterpol: list,
        Col_PadInterpol: list,
        Col_AkimaInterpol: list,
        StdToleranceFactor: float = 1):
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