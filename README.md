# Python ProcessNet for RecurDyn
> Automates RecurDyn operations with ProcessNet and Python.  
For initial setups, please follow this [link](http://www.safetyman.kr/processnet-python-%ec%82%ac%ec%9a%a9%eb%b2%95/) (Korean).    
For official tutorials provided by FunctionBay Inc., refer to this [link](https://www.youtube.com/watch?v=QjCFDidGmHo) (Korean).


### Detailed instructions are provided in [Tutorial.ipynb](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/Tutorial.ipynb)
### For useful tips, check out [Tips.md](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/Tips.md) (Korean)
# Setup
Set `rdSolverDir` to `"<YOUR_RECURDYN_INSTALL_DIR>\Bin\Solver\RDSolverRun.exe"` in `GlobalVariables.py`.

# Simulate using GUI solver
![gui_demo](https://github.com/hyeonbeenlee/RecurDynPython/assets/78078652/fc98aef7-bc89-43e6-9415-4245846be155)

Call `analysis.doe_gui.RunDOE_GUI` with arguments.  
**You can modify DOE scenario by editing line 55~65 in `analysis/doe_gui.py`**  
This method is **_not parallelizable_**.

#### Arguments

- `ModelFileDir: str` Absolute path of model file (\*.rdyn).
- `TopFolderName: str` Folder name to create.
- `NumCPUCores: int` Number of CPU threads to use per simulation. Must be one of `[0,1,2,4,8,16]`
- `EndTime: float` Simulation end time.
- `NumSteps: int` Number of time steps.

```
RunDOE_GUI(
    ModelFileDir=f"{os.getcwd()}/SampleModel.rdyn",
    TopFolderName="TestDOE_GUI",
    NumCPUCores=8,
    EndTime=1,
    NumSteps=100,
)
```

# Simulate using batch solver
![batch_demo](https://github.com/hyeonbeenlee/RecurDynPython/assets/78078652/62b8ddea-f3a2-438a-a322-77b9e1c2b7ec)

Call `analysis.doe_batch.RunDOE_Batch` with arguments.  
**You can control DOE scenario by editing line 59~67 in `analysis/doe_batch.py`**  
This method is **_parallelizable_**, but requires corresponding number of licenses.

#### Arguments

- `ModelFileDir: str` Absolute path of model file (\*.rdyn).
- `TopFolderName: str` Folder name to create.
- `NumCPUCores: int` Number of CPU threads to use per simulation. Must be one of `[0,1,2,4,8,16]`
- `EndTime: float` Simulation end time.
- `NumSteps: int` Number of time steps.
- `NumParallelBatches: int` Number of parallelized simulations (\*.bat) to create.
- `NumBatRunsOnThisPC: int` Number of simulations to run on your current machine. Defaults to `NumParallelBatches`. Range should be within `0`~`NumParallelBatches`.

```
RunDOE_Batch(
    ModelFileDir="SampleModel.rdyn",
    TopFolderName="TestDOE_Batch",
    NumCPUCores=8,
    EndTime=1,
    NumSteps=100,
    NumParallelBatches=5,
)
```
#### Export data from results using `analysis.export_data.rplt2csv`
Exported variables are defined in ```GlobalVariables.GlobVar.DataExportTargets```.
```
rplt2csv(f"{os.getcwd()}/TestDOE_Batch")
```
