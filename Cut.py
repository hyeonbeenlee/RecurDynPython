import pandas as pd
import DataProcessing as DP
path="D:\Research\Trailer2021\SimFiles\DNN\Case015_LocalDisp\Case015_LocalDisp"
data=pd.read_csv(f"{path}.csv")
data=DP.Cut(data,"TIME",5,data["TIME"].iloc[-1])
data=DP.Shift(data,"TIME",-5)
print(data)
data.to_csv(f"{path}_TimeCut.csv")