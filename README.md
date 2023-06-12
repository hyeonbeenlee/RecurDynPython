# ProcessNetPython for RecurDyn V9R5

**_Written by. Hyeonbeen Lee_**  
Automates RecurDyn operations with ProcessNet and Python.  
For initial setups, please follow this [link](http://www.safetyman.kr/processnet-python-%ec%82%ac%ec%9a%a9%eb%b2%95/) (Korean).  
For official tutorials provided by FunctionBay Inc., refer to this [link](https://www.youtube.com/watch?v=QjCFDidGmHo) (Korean).

# Setup

Set `rdSolverDir` to `"<YOUR_RECURDYN_INSTALL_DIR>\Bin\Solver\RDSolverRun.exe"` in `GlobalVariables.py`.

# Initialization

Initialize with imports and global variables

```
from recurdyn import *

# from recurdyn import Chart
# from recurdyn import MTT2D
# from recurdyn import FFlex
# from recurdyn import RFlex
from recurdyn import Tire
from datetime import datetime
import numpy as np
import re
import os
import glob
import os
import pandas as pd

from utils.modeling import *
from analysis.doe_batch import *
from analysis.doe_gui import *
from analysis.export_data import *

app = None
application = None
model_document = None
plot_document = None
model = None

ref_frame_1 = None
ref_frame_2 = None
```

#### Define `initialize()` and `dispose()` functions.

```
# initialize() should be called before ProcessNet function call.
def initialize():
    global app
    global application
    global model_document
    global plot_document
    global model

    app = dispatch_recurdyn()
    application = IApplication(app.RecurDynApplication)
    model_document = application.ActiveModelDocument
    if model_document is not None:
        model_document = IModelDocument(model_document)
    plot_document = application.ActivePlotDocument
    if plot_document is not None:
        plot_document = IPlotDocument(plot_document)

    if model_document is None and plot_document is None:
        application.PrintMessage("No model file")
        model_document = application.NewModelDocument("Examples")
    if model_document is not None:
        model_document = IModelDocument(model_document)
        model = ISubSystem(model_document.Model)

    return application, model_document, plot_document, model


# dispose() should be called after ProcessNet function call.


def dispose():
    global application
    global model_document

    model_document = application.ActiveModelDocument
    if model_document is not None:
        model_document = IModelDocument(model_document)
    else:
        return

    if not model_document.Validate():
        return
    # Redraw() and UpdateDatabaseWindow() can take more time in a heavy model.
    # model_document.Redraw()
    # model_document.PostProcess() # UpdateDatabaseWindow(), SetModified()
    # model_document.UpdateDatabaseWindow()
    # If you call SetModified(), Animation will be reset.
    # model_document.SetModified()
    model_document.SetUndoHistory("Python ProcessNet")
```

# Simulate using GUI solver

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

#### Export data from results using `analysis.export_data.rplt2csv`

Exported variables are defined in `GlobalVariables.GlobVar.DataExportTargets`.

```
rplt2csv(f"{os.getcwd()}/TestDOE_GUI")
```

# Simulate using batch solver

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

Exported variables are defined in `GlobalVariables.GlobVar.DataExportTargets`.

```
rplt2csv(f"{os.getcwd()}/TestDOE_Batch")
```
