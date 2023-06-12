import shutil
import os
import glob
import sys
import time
import joblib
import subprocess
from datetime import datetime
from utils.modeling import *
from utils.sampling import *

from recurdyn import *
from GlobalVariables import GlobVar
from . import initialize, dispose


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


def RunDOE_Batch(
    TopFolderName: str,
    NumParallelBatches: int = 3,
    NumCPUCores: int = 8,
    NumBatRunsOnThisPC: int = 2,
):
    if NumCPUCores:
        application.Settings.AutoCoreNumber = False
        application.Settings.CoreNumber = NumCPUCores
    else:
        application.Settings.AutoCoreNumber = True
    application, model_document, plot_document, model = initialize()
    application.ClearMessage()
    
    datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
    AnalysisStartTime = time.time()
    
    CaseNo = ["015"]  # ,"012"
    Counter = 1
    for idx_case, c in enumerate(CaseNo):
        
        #################################################################### FIX #################################################################
        model_document = application.OpenModelDocument(
            f"D:\Research\Trailer2022\Ground_Model\\Trailer_{c}.rdyn"
        )
        # model_document = application.OpenModelDocument(f"D:\Research\Trailer2021\SimFiles\DNN\\Trailer_{c}.rdyn")
        modelPath = model_document.GetPath(PathType.WorkingFolder)
        model = model_document.Model
        EndTime = IParametricValue(model.GetEntity("PV_EndTime")).Value
        NumSteps = IParametricValue(model.GetEntity("PV_NumSteps")).Value
        p_values = LHCSampler(10, 1, seed=777) * 2000 + 1000  # 1000~3000
        i_values = LHCSampler(10, 1, seed=777) * 400 + 100  # 100~500
        for n in range(p_values.shape[0]):
            ChangePVvalue(model, "PV_TX_P", 300)
            ChangePVvalue(model, "PV_TX_I", 10)
            ChangePVvalue(model, "PV_TY_P", int(p_values[n, 0]))
            ChangePVvalue(model, "PV_TY_I", int(i_values[n, 0]))
            SubFolderName = (
                f"{Counter:03d}_Case{c}_{int(p_values[n, 0])}_{int(i_values[n, 0])}"
            )
            ExportSolverFiles(
                TopFolderName, SubFolderName, EndTime=EndTime, NumSteps=NumSteps
            )
            Counter += 1

            # Revert to original
            ChangePVvalue(model, "PV_TX_P", 300)
            ChangePVvalue(model, "PV_TX_I", 10)
            ChangePVvalue(model, "PV_TY_P", 1000)
            ChangePVvalue(model, "PV_TY_I", 50)
            
            
    batfilespath = WriteBatch(TopFolderName, NumParallelBatches)
    run = joblib.Parallel(n_jobs=NumBatRunsOnThisPC)(
        joblib.delayed(RunSubprocess)(bat) for bat in batfilespath[:NumBatRunsOnThisPC]
    )
    AnalysisEndTime = time.time()
    s = AnalysisEndTime - AnalysisStartTime
    print(f"Analysis finished within {s}sec.")


def RunSubprocess(single_batfilepath):
    subprocess.run(single_batfilepath, creationflags=subprocess.CREATE_NEW_CONSOLE)
