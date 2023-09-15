import shutil
import os
import glob
import time
import joblib
import subprocess
from utils.modeling import *
from utils.sampling import *

from recurdyn import *
from GlobalVariables import GlobVar
from . import initialize, dispose


def RunDOE_Batch(
    ModelFileDir: str = f"{os.getcwd()}/SampleModel.rdyn",
    TopFolderName: str = "TestDOE_GUI",
    NumCPUCores: int = 8,
    EndTime: float = 1.0,
    NumSteps: int = 100,
    NumParallelBatches: int = 3,
    NumBatRunsOnThisPC: int = None,
) -> None:
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
    application.ClearMessage()
    if NumBatRunsOnThisPC is None:
        NumBatRunsOnThisPC = NumParallelBatches
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
        ExportSolverFiles(
            TopFolderName, SubFolderName, EndTime=EndTime, NumSteps=NumSteps
        )
        Counter += 1
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################
    ######################################### EDIT HERE #########################################

    batfilespath = WriteBatch(TopFolderName, NumParallelBatches)
    run = joblib.Parallel(n_jobs=NumBatRunsOnThisPC)(
        joblib.delayed(RunSubprocess)(bat) for bat in batfilespath[:NumBatRunsOnThisPC]
    )
    AnalysisEndTime = time.perf_counter()
    s = AnalysisEndTime - AnalysisStartTime
    print(f"Analysis finished within {s:.2f}sec.")


def ExportSolverFiles(
    OutputFolderName: str,
    OutputFileName: str,
    EndTime: int = 1,
    NumSteps: int = 101,
    PlotMultiplierStepFactor: int = 1,
):
    """
    Exports *.rmd, *.rss, and copies *.(DependentExt) to directory modelPath/OutputFolderName/*.* for batch automated solving.
    DependentExt may include tire files (*.tir), GRoad files (*.rdf), or flexible meshes.
    :param OutputFolderName:
    :param OutputFileName:
    :param EndTime: Simulation end time
    :param NumSteps: Simulation steps
    :param PlotMultiplierStepFactor:
    :return:
    """
    application, model_document, plot_document, model = initialize()
    model_document = application.ActiveModelDocument
    model = model_document.Model
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    print(f"{modelPath}{OutputFolderName}\\{OutputFileName}")
    os.makedirs(f"{modelPath}{OutputFolderName}\\{OutputFileName}", exist_ok=True)
    # Copy dependency files
    DependentExt = (
        "tir",
        "rdf",
    )
    DependentFiles = []
    for ext in DependentExt:
        DependentFiles.extend(glob.glob(f"{modelPath}*.{ext}"))
    for file in DependentFiles:
        shutil.copy(file, f"{modelPath}{OutputFolderName}\\{OutputFileName}")
    # Analysis Property
    model_document.ModelProperty.DynamicAnalysisProperty.MatchSolvingStepSize = True
    model_document.ModelProperty.DynamicAnalysisProperty.MatchSimulationEndTime = True
    model_document.ModelProperty.DynamicAnalysisProperty.PlotMultiplierStepFactor.Value = (
        PlotMultiplierStepFactor
    )
    # RMD export
    model_document.FileExport(
        f"{modelPath}{OutputFolderName}\\{OutputFileName}\\{OutputFileName}.rmd", True
    )
    # RSS export
    RSScontents = f"SIM/DYN, END = {EndTime}, STEP = {NumSteps}\nSTOP"
    rss = open(
        f"{modelPath}{OutputFolderName}\\{OutputFileName}\\{OutputFileName}.rss", "w"
    )
    rss.write(RSScontents)
    rss.close()


def WriteBatch(SolverFilesFolderName: str, parallelBatches: 1):
    """
    Write *.bat execution files for batch solving.
    :param SolverFilesFolderName:
    :param parallelBatches:
    :return:
    """
    application, model_document, plot_document, model = initialize()
    application.ClearMessage()
    model_document = application.ActiveModelDocument
    model = model_document.Model
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    RMDlist = glob.glob(
        f"{modelPath}{SolverFilesFolderName}\\**\\*.rmd", recursive=True
    )
    batfilespath = []
    for i in range(parallelBatches):
        BatchFileName = f"{SolverFilesFolderName}_{i + 1}.bat"
        interval = round(len(RMDlist) / parallelBatches)
        bat = open(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}", "w")
        if i == parallelBatches - 1:  # Last index
            idx_start = i * interval
            idx_end = len(RMDlist)
        else:
            idx_start = i * interval
            idx_end = (i + 1) * interval
        for rmdName in RMDlist[idx_start:idx_end]:
            solverfilename = os.path.basename(rmdName).split(".")[:-1]
            if len(os.path.basename(rmdName).split(".")) > 2:
                solverfilename = ".".join(os.path.basename(rmdName).split(".")[:-1])
            else:
                solverfilename = "".join(solverfilename)
            BATcontent = []
            BATcontent.append(modelPath[:2])  # Drive Name
            BATcontent.append(f"cd {os.path.dirname(rmdName)}")  # cd RMD path
            BATcontent.append(
                f"{GlobVar.rdSolverDir} {solverfilename} {solverfilename}"
            )  #
            bat.writelines(line + "\n" for line in BATcontent)
        bat.close()
        application.PrintMessage(
            f"Created batch executable {modelPath}{SolverFilesFolderName}\\{BatchFileName}"
        )
        print(
            f"Created batch executable {modelPath}{SolverFilesFolderName}\\{BatchFileName}"
        )
        batfilespath.append(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}")
    return batfilespath


def RunSubprocess(single_batfilepath):
    subprocess.run(single_batfilepath, creationflags=subprocess.CREATE_NEW_CONSOLE)
