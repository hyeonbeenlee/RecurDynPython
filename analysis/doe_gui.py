from recurdyn import *
from GlobalVariables import GlobVar
from . import initialize, dispose
from utils.modeling import *
from utils.sampling import *
import time
import os


def RunDOE_GUI(
    ModelFileDir: str = f"{os.getcwd()}/SampleModel.rdyn",
    TopFolderName: str = "TestDOE_GUI",
    NumCPUCores: int = 8,
    EndTime: float = 1,
    NumSteps: int = 100,
) -> None:
    """
    Run automated simulations in GUI interface solver.
    :param TopFolderName: A new directory for solved files.
    :param NumCPUCores: Number of CPU threads for solving. 'AUTO' if 0. [1,2,4,8,16] are supported values.
    :return:
    """
    application, model_document, plot_document, model = initialize()
    application.ClearMessage()
    assert type(NumSteps) == int, "NumSteps must be integer."
    assert NumCPUCores in [
        0,
        1,
        2,
        4,
        8,
        16,
    ], "NumCPUCores must be one of 0,1,2,4,8,16."
    model_document = application.OpenModelDocument(ModelFileDir)
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    model = model_document.Model
    application.Settings.CreateOutputFolder = False
    model_document.UseOutputFileName = True
    model_document.ModelProperty.DynamicAnalysisProperty.SimulationStep.Value = NumSteps
    model_document.ModelProperty.DynamicAnalysisProperty.SimulationTime.Value = EndTime
    model_document.ModelProperty.DynamicAnalysisProperty.MatchSolvingStepSize = True
    model_document.ModelProperty.DynamicAnalysisProperty.MatchSimulationEndTime = True
    if NumCPUCores:
        application.Settings.AutoCoreNumber = False
        application.Settings.CoreNumber = NumCPUCores
    else:
        application.Settings.AutoCoreNumber = True
    application, model_document, plot_document, model = initialize()
    application.ClearMessage()
    AnalysisStartTime = time.perf_counter()

    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    Counter = 1
    SamplePV = np.logspace(-2, 10, 10, endpoint=True)
    for samplepv in SamplePV:
        ChangePVvalue(model, "PV_SampleK", samplepv)
        SubFolderName = f"{TopFolderName}_{Counter:04d}"
        model_document.OutputFileName = (
            f"{TopFolderName}\\{SubFolderName}\\{SubFolderName}"
        )
        model_document.Analysis(AnalysisMode.Dynamic)
        Counter += 1
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################

    AnalysisEndTime = time.perf_counter()
    s = AnalysisEndTime - AnalysisStartTime
    print(f"Analysis finished within {s:.2f}sec.")
