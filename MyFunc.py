from recurdyn import *
# from recurdyn import Chart
# from recurdyn import MTT2D
# from recurdyn import FFlex
# from recurdyn import RFlex
# from recurdyn import Tire
import numpy as np
import DataProcessing as DP
import glob
import os
import subprocess
import time
import MyVar
import re
import pandas as pd
import shutil
import matplotlib.pyplot as plt

# Common Variables
rdSolverDir = "\"C:\Program Files\FunctionBay, Inc\RecurDyn V9R5\Bin\Solver\RDSolverRun.exe\""
app = None
application = None
model_document = None
plot_document = None
model = None

ref_frame_1 = None
ref_frame_2 = None

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

def ChangePVvalue(PVname: str, PVvalue: float):
    PV = IParametricValue(model.GetEntity(PVname))
    PV.Value = PVvalue

def Import(importfile: str):
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    print(f"Imported file: {importfile}")
    model_document.FileImport(importfile)

def ExportSolverFiles(OutputFolderName: str, OutputFileName: str, EndTime: int = 1, NumSteps: int = 101, PlotMultiplierStepFactor: int = 1):
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    print(f"{modelPath}{OutputFolderName}\\{OutputFileName}")
    DP.CreateDir(f"{modelPath}{OutputFolderName}\\{OutputFileName}")
    # Copy dependency files
    DependentExt = ("tir", "rdf",)
    DependentFiles = []
    for ext in DependentExt:
        DependentFiles.extend(glob.glob(f"{modelPath}*.{ext}"))
    for file in DependentFiles:
        shutil.copy(file, f"{modelPath}{OutputFolderName}\\{OutputFileName}")
    # Analysis Property
    model_document.ModelProperty.DynamicAnalysisProperty.MatchSolvingStepSize = True
    model_document.ModelProperty.DynamicAnalysisProperty.MatchSimulationEndTime = True
    model_document.ModelProperty.DynamicAnalysisProperty.PlotMultiplierStepFactor.Value = PlotMultiplierStepFactor
    # RMD export
    model_document.FileExport(f"{modelPath}{OutputFolderName}\\{OutputFileName}\\{OutputFileName}.rmd", True)
    # RSS export
    RSScontents = f"SIM/DYN, END = {EndTime}, STEP = {NumSteps}\nSTOP"
    rss = open(f"{modelPath}{OutputFolderName}\\{OutputFileName}\\{OutputFileName}.rss", 'w')
    rss.write(RSScontents)
    rss.close()

def WriteBatch(SolverFilesFolderName: str):
    global rdSolverDir
    application.ClearMessage()
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    BatchFileName = f"{SolverFilesFolderName}.bat"
    bat = open(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}", 'w')
    RMDlist = glob.glob(f"{modelPath}{SolverFilesFolderName}\\**\\*.rmd", recursive=True)
    for rmdName in RMDlist:
        solverfilename = os.path.basename(rmdName).split('.')[:-1]
        if len(os.path.basename(rmdName).split('.')) > 2:
            solverfilename = '.'.join(os.path.basename(rmdName).split('.')[:-1])
        else:
            solverfilename = ''.join(solverfilename)
        BATcontent = []
        BATcontent.append(modelPath[:2])  # Drive Name
        BATcontent.append(f"cd {os.path.dirname(rmdName)}")  # cd RMD path
        BATcontent.append(f"{rdSolverDir} {solverfilename} {solverfilename}")  #
        bat.writelines(line + "\n" for line in BATcontent)
    bat.close()
    application.PrintMessage(f"Created batch executable {modelPath}{SolverFilesFolderName}\\{BatchFileName}")

def RunBatch(SolverFilesFolderName: str):
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    BatchFileDir = f"{modelPath}{SolverFilesFolderName}\\{SolverFilesFolderName}.bat"
    print(f"Running {BatchFileDir}...")
    StartTime = time.time()
    subprocess.run(BatchFileDir, creationflags=subprocess.CREATE_NEW_CONSOLE)
    EndTime = time.time()
    Elapsed = EndTime - StartTime
    Hr, Min, Sec = DP.Sec2Time(Elapsed)
    print(f"Finished, simulation time: {Hr}hr {Min}min {Sec:.2f}sec")

def RPLT2CSV(SolverFilesAbsPath: str):
    application.CloseAllPlotDocument()
    CSVExportDir = SolverFilesAbsPath
    DP.CreateDir(CSVExportDir)
    RPLTlist = glob.glob(f"{SolverFilesAbsPath}\\**\\*.rplt", recursive=True)
    StartTime = time.time()
    for idx_rplt, rplt in enumerate(RPLTlist):
        application.NewPlotDocument("PlotDoc")
        application.OpenPlotDocument(rplt)
        plot_document = application.ActivePlotDocument
        rpltname = os.path.basename(rplt).split('.')[:-1]
        if len(os.path.basename(rplt).split('.')) > 2:
            rpltname = '.'.join(os.path.basename(rplt).split('.')[:-1])
        else:
            rpltname = ''.join(rpltname)
        DataExportTargets = [f"{rpltname}/{target}" for target in MyVar.DataExportTargets]
        CSVpath = f"{CSVExportDir}\\{rpltname}.csv"
        plot_document.ExportData(CSVpath, DataExportTargets, True, False, 8)
        application.ClosePlotDocument(plot_document)
        application.PrintMessage(f"Data exported {CSVpath} ({idx_rplt}/{len(RPLTlist)})")
        print(f"Data exported {CSVpath} ({idx_rplt}/{len(RPLTlist)})")
    EndTime = time.time()
    Elapsed = EndTime - StartTime
    Hr, Min, Sec = DP.Sec2Time(Elapsed)
    print(f"Finished, data export time: {Hr}hr {Min}min {Sec:.2f}sec")

def LoopRun(SolverFilesFolderName: str, EndTime: int = 1, NumSteps: int = 101, PlotMultiplierStepFactor: int = 1):
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    
    # DP.PlotTemplate(15)
    # fig,ax=plt.subplots(1,1,figsize=(6,5))
    # ax.plot(Samples[:,0],Samples[:,1],linestyle='none',marker='x',markersize=4,markerfacecolor='black',markeredgecolor='black')
    # ax.set(xlim=(1,2),xlabel='$l_1$',ylim=(1,2),ylabel='$l_2$')
    # fig.tight_layout()
    # plt.show()
    
    Counter = 1
    Svx = np.linspace(0.5, 1.5, 11, endpoint=True)
    Svy = np.linspace(0.5, 1.5, 11, endpoint=True)
    for svx in Svx:
        for svy in Svy:
            ChangePVvalue('PV_Scale_VX', svx)
            ChangePVvalue('PV_Scale_VY', svy)
            ExportSolverFiles(SolverFilesFolderName, f"Train_{Counter:04d}", EndTime=EndTime, NumSteps=NumSteps)
            Counter += 1

    Counter = 1
    Svx = np.linspace(0.5, 1.5, 16, endpoint=True)
    Svy = np.linspace(0.5, 1.5, 16, endpoint=True)
    for svx in Svx:
        for svy in Svy:
            ChangePVvalue('PV_Scale_VX', svx)
            ChangePVvalue('PV_Scale_VY', svy)
            ExportSolverFiles(SolverFilesFolderName, f"Train2_{Counter:04d}", EndTime=EndTime, NumSteps=NumSteps)
            Counter += 1
    
    Counter = 1
    Samples = DP.LHCSampler(100, 2, seed=777)
    Samples[:, 0] += 0.5
    Samples[:, 1] += 0.5
    for sample in Samples:
        svx, svy = sample
        ChangePVvalue('PV_Scale_VX', svx)
        ChangePVvalue('PV_Scale_VY', svy)
        ExportSolverFiles(SolverFilesFolderName, f"Valid_{Counter:04d}", EndTime=EndTime, NumSteps=NumSteps)
        Counter += 1
    
    Counter = 1
    Samples = DP.LHCSampler(300, 2, seed=777)
    Samples[:, 0] += 0.5
    Samples[:, 1] += 0.5
    for sample in Samples:
        svx, svy = sample
        ChangePVvalue('PV_Scale_VX', svx)
        ChangePVvalue('PV_Scale_VY', svy)
        ExportSolverFiles(SolverFilesFolderName, f"Test_{Counter:04d}", EndTime=EndTime, NumSteps=NumSteps)
        Counter += 1
    
    WriteBatch(SolverFilesFolderName)
    RunBatch(SolverFilesFolderName)
    RPLT2CSV(f"{modelPath}{SolverFilesFolderName}")

def SingleRun(SolverFilesFolderName: str, EndTime: int = 1, NumSteps: int = 100, PlotMultiplierStepFactor: int = 1):
    global application
    application.ClearMessage()
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    ExportSolverFiles(SolverFilesFolderName, f"{SolverFilesFolderName}", EndTime=EndTime, NumSteps=NumSteps, PlotMultiplierStepFactor=PlotMultiplierStepFactor)
    WriteBatch(SolverFilesFolderName)
    RunBatch(SolverFilesFolderName)
    Import(f"{modelPath}{SolverFilesFolderName}\\{SolverFilesFolderName}\\{SolverFilesFolderName}.ran")
    RPLT2CSV(f"{modelPath}{SolverFilesFolderName}")

def CreateSplineExpressions(Spline_Dir):
    application.ClearMessage()
    model_document = application.ActiveModelDocument
    model = model_document.Model
    
    FileList = glob.glob(f"{Spline_Dir}\\*.csv")
    Target = ["24", "31"]
    
    for idx_file, file_spline in enumerate(FileList):
        name_file = os.path.basename(file_spline)
        number_sensor = re.sub(r"[^0-9]", "", name_file)
        
        if number_sensor in Target and name_file[0] == 'A':
            name_spline = f"Sp_{os.path.basename(file_spline).split('.')[0]}"
            name_expression = f"Ex_{os.path.basename(file_spline).split('.')[0]}"
            model.CreateSplineWithFile(name_spline, file_spline)
            model.CreateExpression(f"{name_expression}", f"AKISPL(TIME,0,{name_spline},0)")
            print(f"Created {name_spline}: {file_spline}")
    
    # Large mass forces
    model.CreateExpression("Ex_F31AX", "PV_LargeM*AKISPL(TIME,0,Sp_A31AX,0)/1000")
    model.CreateExpression("Ex_F31AY", "PV_LargeM*AKISPL(TIME,0,Sp_A31AY,0)/1000")
    model.CreateExpression("Ex_F31AZ", "PV_LargeM*AKISPL(TIME,0,Sp_A31AZ,0)/1000")
    model.CreateExpression("Ex_F31GX", "PV_LargeIxx*AKISPL(TIME,0,Sp_A31GX,0)/1000")
    model.CreateExpression("Ex_F31GY", "PV_LargeIyy*AKISPL(TIME,0,Sp_A31GY,0)/1000")
    model.CreateExpression("Ex_F31GZ", "PV_LargeIzz*AKISPL(TIME,0,Sp_A31GZ,0)/1000")
    
    # Accelerations
    model.CreateExpressionWithArguments("Ex_ATX_CM", "ACCX(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_ATY_CM", "ACCY(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_ATZ_CM", "ACCZ(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_ARX_CM", "WDTX(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_ARY_CM", "WDTY(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_ARZ_CM", "WDTZ(1)", ["Cask.Marker_CaskCradleCM"])
    
    # Velocities
    model.CreateExpressionWithArguments("Ex_VTX_CM", "VX(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_VTY_CM", "VY(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_VTZ_CM", "VZ(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_VRX_CM", "WX(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_VRY_CM", "WY(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_VRZ_CM", "WZ(1)", ["Cask.Marker_CaskCradleCM"])
    
    # Displacements
    model.CreateExpressionWithArguments("Ex_DTX_CM", "DX(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_DTY_CM", "DY(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_DTZ_CM", "DZ(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_DRX_CM", "ROLL(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_DRY_CM", "PITCH(1)", ["Cask.Marker_CaskCradleCM"])
    model.CreateExpressionWithArguments("Ex_DRZ_CM", "YAW(1)", ["Cask.Marker_CaskCradleCM"])

def ExportSensorDisplacements():
    application.ClearMessage()
    SensorNum = [20, 51, 52, 53]
    TrailerBody = IBody(model.GetEntity("Trailer_6"))
    for number in SensorNum:
        SensorBody = IBody(model.GetEntity(f"Sensor_{number}"))
        X, Y, Z = SensorBody.GetReferenceFrameInfoOfCenterMarker().GetOrigin()
        SensorMarker = IMarker(SensorBody.GetEntity("CM"))
        refFrame_Sensor = model_document.CreateReferenceFrame()
        refFrame_Sensor.SetOrigin(X, Y, Z)
        refFrame_Sensor.SetEulerAngle(EulerAngle.EulerAngle_ZYX, 0, 0, 0)
        TrailerBody.CreateMarker(f"Marker_Sensor_{number}", refFrame_Sensor)
        TrailerMarker = IMarker(TrailerBody.GetEntity(f"Marker_Sensor_{number}"))
        model.CreateRequestStandard(f"Rq_Sensor_{number}", RequestStandardType.Displacement, SensorMarker, TrailerMarker, TrailerMarker)
    SingleRun("Case011_LocalDisp", EndTime=30, NumSteps=12000)

def CreateExpressionLoop():
    application.ClearMessage()
    application.CloseAllDocument()
    
    rdynList = []
    DataDirList = os.walk("D:\Research\Trailer2022\Sea_Tuning\Model_OtherScenarios2\\2. Sea")
    for root, subdirs, files in DataDirList:
        if 'Detrended' in root:
            # Open base rdyn
            model_document = application.OpenModelDocument("D:\Research\Trailer2022\Sea_Tuning\Model_OtherScenarios2\CaskCraddle_LMM_Blank.rdyn")
            model = model_document.Model
            # Case name
            caseName = root.split('\\')[-3]
            # Read A31 data
            for f in files:
                if 'A31' in f: break
            f = pd.read_csv(f"{root}\\{f}")
            # set PV
            IParametricValue(model.GetEntity("PV_NumSteps")).Value = f.shape[0] - 1
            IParametricValue(model.GetEntity("PV_EndTime")).Value = f['TIME'].iloc[-1]
            # Create splines & Force expressions
            CreateSplineExpressions(root)
            # Allocate force expressions
            TraForce = IForceTranslational(model.GetEntity("Translational_LMM"))
            RotForce = IForceRotational(model.GetEntity("Rotational_LMM"))
            TraForce.ExpressionFX = IExpression(model.GetEntity("Ex_F31AX"))
            TraForce.ExpressionFY = IExpression(model.GetEntity("Ex_F31AY"))
            TraForce.ExpressionFZ = IExpression(model.GetEntity("Ex_F31AZ"))
            RotForce.ExpressionTX = IExpression(model.GetEntity("Ex_F31GX"))
            RotForce.ExpressionTY = IExpression(model.GetEntity("Ex_F31GY"))
            RotForce.ExpressionTZ = IExpression(model.GetEntity("Ex_F31GZ"))
            # Save
            rdynName = f"D:\Research\Trailer2022\Sea_Tuning\Model_OtherScenarios2\CaskCraddle_LMM_{caseName}.rdyn"
            rdynList.append(rdynName)
            model_document.FileSave(rdynName, True)
            # Close
            application.CloseAllDocument()
    
    # Analysis
    for rdyn in rdynList:
        dir = os.path.dirname(rdyn)
        name = os.path.basename(rdyn).split('.')[0]
        model_document = application.OpenModelDocument(rdyn)
        model = model_document.Model
        model_document.ModelProperty.DynamicAnalysisProperty.MatchSolvingStepSize = True
        model_document.ModelProperty.DynamicAnalysisProperty.SimulationStep.Value = IParametricValue(model.GetEntity("PV_NumSteps")).Value
        model_document.ModelProperty.DynamicAnalysisProperty.SimulationTime.Value = IParametricValue(model.GetEntity("PV_EndTime")).Value
        model_document.OutputFileName = f"{name}\\{name}"
        model_document.Analysis(AnalysisMode.Dynamic)
        RPLT2CSV(f"{dir}\\{name}")



def ScenarioLoop():
    application.ClearMessage()


if __name__ == '__main__':
    application, model_document, plot_document, model = initialize()
    
    #
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    LoopRun(f"220816_DPCNN", EndTime=IParametricValue(model.GetEntity("PV_EndTime")).Value, NumSteps=IParametricValue(model.GetEntity("PV_NumSteps")).Value)
    # RPLT2CSV("D:\Research\DNN_TransientInput\DoublePendulumContact\\220814_LHCValidSet_BE")
    # RPLT2CSV(f"C:\\Users\LHB-MSLab\Documents\GitHub\KRISO-DNN\EDEM_RecurDyn_CoSim_211107\RPLT files")
    # CreateExpressionLoop()
    # CreateSplineExpressions()
    # SingleRun("220719_LMM_SmallKC",EndTime=299,NumSteps=149500)
    # ExportSensorDisplacements()
    # CreateExpressionLoop()
    #
    
    dispose()
