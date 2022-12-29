from recurdyn import *
# from recurdyn import Chart
# from recurdyn import MTT2D
# from recurdyn import FFlex
# from recurdyn import RFlex
from recurdyn import Tire
from datetime import datetime
import numpy as np
import DataProcessing as DP
import re, shutil, time, subprocess, os, glob, joblib, MyVar, threading, random
import pandas as pd
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

def ChangePVvalue(model, PVname: str, PVvalue: float):
    PV = IParametricValue(model.GetEntity(PVname))
    PV.Value = PVvalue

def Import(importfile: str):
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    print(f"Imported file: {importfile}")
    model_document.FileImport(importfile)

def ExportSolverFiles(OutputFolderName: str, OutputFileName: str, EndTime: int = 1, NumSteps: int = 101, PlotMultiplierStepFactor: int = 1):
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
    model_document = application.ActiveModelDocument
    model = model_document.Model
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

# def WriteBatch(SolverFilesFolderName: str, parallelBatches: 1):
#     global rdSolverDir
#     application.ClearMessage()
#     model_document = application.ActiveModelDocument
#     model = model_document.Model
#     modelPath = model_document.GetPath(PathType.WorkingFolder)
#     RMDlist = glob.glob(f"{modelPath}{SolverFilesFolderName}\\**\\*.rmd", recursive=True)
#     batfiles=[]
#     for i in range(parallelBatches):
#         BatchFileName = f"{SolverFilesFolderName}_{i + 1}.bat"
#         interval = round(len(RMDlist) / parallelBatches)
#         bat = open(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}", 'w')
#         if i == parallelBatches - 1:  # Last index
#             idx_start = i * interval
#             idx_end = len(RMDlist)
#         else:
#             idx_start = i * interval
#             idx_end = (i + 1) * interval
#         for rmdName in RMDlist[idx_start: idx_end]:
#             solverfilename = os.path.basename(rmdName).split('.')[:-1]
#             if len(os.path.basename(rmdName).split('.')) > 2:
#                 solverfilename = '.'.join(os.path.basename(rmdName).split('.')[:-1])
#             else:
#                 solverfilename = ''.join(solverfilename)
#             BATcontent = []
#             BATcontent.append(modelPath[:2])  # Drive Name
#             BATcontent.append(f"cd {os.path.dirname(rmdName)}")  # cd RMD path
#             BATcontent.append(f"{rdSolverDir} {solverfilename} {solverfilename}")  #
#             bat.writelines(line + "\n" for line in BATcontent)
#         bat.close()
#         application.PrintMessage(f"Created batch executable {modelPath}{SolverFilesFolderName}\\{BatchFileName}")
#         print(f"Created batch executable {modelPath}{SolverFilesFolderName}\\{BatchFileName}")
#         batfiles.append(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}")
#     return batfiles

def WriteBatch(SolverFilesFolderName: str, parallelBatches: 1):
    """
    Write *.bat execution files for batch solving.
    :param SolverFilesFolderName:
    :param parallelBatches:
    :return:
    """
    global rdSolverDir
    application.ClearMessage()
    model_document = application.ActiveModelDocument
    model = model_document.Model
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    RMDlist = glob.glob(f"{modelPath}{SolverFilesFolderName}\\**\\*.rmd", recursive=True)
    batfilespath = []
    for i in range(parallelBatches):
        BatchFileName = f"{SolverFilesFolderName}_{i + 1}.bat"
        interval = round(len(RMDlist) / parallelBatches)
        bat = open(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}", 'w')
        if i == parallelBatches - 1:  # Last index
            idx_start = i * interval
            idx_end = len(RMDlist)
        else:
            idx_start = i * interval
            idx_end = (i + 1) * interval
        for rmdName in RMDlist[idx_start: idx_end]:
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
        print(f"Created batch executable {modelPath}{SolverFilesFolderName}\\{BatchFileName}")
        batfilespath.append(f"{modelPath}{SolverFilesFolderName}\\{BatchFileName}")
    return batfilespath

def RPLT2CSV(SolverFilesPath: str):
    """
    Scans and reads all *.rplt files in the SolverFilesAbsPath (recursively scanned).
    Then export values from Var.DataExportTargets in *.csv format.
    :param SolverFilesPath: rplt files directory
    :return:
    """
    application.CloseAllPlotDocument()
    CSVExportDir = os.path.abspath(SolverFilesPath)
    DP.CreateDir(CSVExportDir)
    RPLTlist = glob.glob(f"{CSVExportDir}\\**\\*.rplt", recursive=True)
    datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
    AnalysisStartTime = time.time()
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
        application.PrintMessage(f"Data exported {CSVpath} ({idx_rplt + 1}/{len(RPLTlist)})")
        print(f"Data exported({idx_rplt + 1}/{len(RPLTlist)}) {CSVpath} ")
    AnalysisEndTime = time.time()
    h, m, s = DP.Sec2Time(AnalysisEndTime - AnalysisStartTime)
    print(f"Analysis finished within {h}hr {m}min {s}sec.")


def RunDOE_Batch(TopFolderName: str, NumParallelBatches: int = 3, NumCPUCores: int = 8, NumBatRunsOnThisPC: int = 2):
    application.ClearMessage()
    CaseNo = ["011", "015"]  # ,"012"
    datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
    AnalysisStartTime = time.time()
    for idx_case, c in enumerate(CaseNo):
        Counter = 1
        #################################################################### FIX #################################################################
        model_document = application.OpenModelDocument(f"D:\Research\Trailer2022\Ground_Model\\Trailer_{c}.rdyn")
        # model_document = application.OpenModelDocument(f"D:\Research\Trailer2021\SimFiles\DNN\\Trailer_{c}.rdyn")
        modelPath = model_document.GetPath(PathType.WorkingFolder)
        model = model_document.Model
        EndTime = IParametricValue(model.GetEntity("PV_EndTime")).Value
        NumSteps = IParametricValue(model.GetEntity("PV_NumSteps")).Value
        if NumCPUCores:
            application.Settings.AutoCoreNumber = False
            application.Settings.CoreNumber = NumCPUCores
        else:
            application.Settings.AutoCoreNumber = True
        #################################################################### FIX #################################################################
        # Roads = [f"GRoad_Uneven_R4p00_ModGeo{i + 1:02d}" for i in range(11)]
        # deltaW = np.linspace(-250, 250, 11, endpoint=True, dtype=int)
        # TireKscales = np.logspace(-2, 2, 2)
        # TireKscales = DP.LHCSampler(500, 4, seed=0) * 3 - 1  # E-1 ~ E+2
        # SusKCscales = DP.LHCSampler(500, 4, seed=0) * 2 - 1  # E-1 ~ E+1
        # for idx, s in enumerate(TireKscales):
        # TireParamScaler(modelPath,
        #                 radialK=np.power(10, s[0]),
        #                 longtitudinalK=np.power(10, s[1]),
        #                 lateralK=np.power(10, s[2]),
        #                 camberK=np.power(10, s[3]))
        # ChangePVvalue(model, "PV_Spring_K_4", 23770 * np.power(10, SusKCscales[idx, 0]))
        # ChangePVvalue(model, "PV_Spring_K_6", 71310 * np.power(10, SusKCscales[idx, 1]))
        # ChangePVvalue(model, "PV_Spring_C_4", 1000 * np.power(10, SusKCscales[idx, 2]))
        # ChangePVvalue(model, "PV_Spring_C_6", 500 * np.power(10, SusKCscales[idx, 3]))
        # if c == "011":
        #     roadName=random.choice(Roads)
        #     for i in range(40):
        #         Tire.ITireGroupGeneric(model.GetEntity(f"GTireGroup{i + 1}")).Road = f"Ground.{roadName}"
        # if c == "011":
        # roadName = random.choice(Roads)
        #     for i in range(40):
        #         Tire.ITireGroupGeneric(model.GetEntity(f"GTireGroup{i + 1}")).Road = f"Ground.{roadName}"
        scales=np.logspace(-2,2,4,endpoint=True)
        for scale in scales:
            TireParamScaler(modelPath, radialK=2077, longtitudinalK=5165, lateralK=698985, camberK=68, mode='sub')
            ChangePVvalue(model, "PV_Spring_K_4", 23299*scale) #23299
            ChangePVvalue(model, "PV_Spring_C_4", 3975)
            ChangePVvalue(model, "PV_Spring_K_6", 8864)
            ChangePVvalue(model, "PV_Spring_C_6", 136)
            if c == "011":
                roadName = "GRoad_Uneven_R4p00_ModGeo10"
                for i in range(40):
                    Tire.ITireGroupGeneric(model.GetEntity(f"GTireGroup{i + 1}")).Road = f"Ground.{roadName}"
            
            SubFolderName = f"{Counter:03d}_Case{c}"
            ExportSolverFiles(TopFolderName, SubFolderName, EndTime=EndTime, NumSteps=NumSteps)
            Counter += 1
    batfilespath = WriteBatch(TopFolderName, NumParallelBatches)
    run = joblib.Parallel(n_jobs=NumBatRunsOnThisPC)(joblib.delayed(RunSubprocess)(bat) for bat in batfilespath[:NumBatRunsOnThisPC])
    AnalysisEndTime = time.time()
    h, m, s = DP.Sec2Time(AnalysisEndTime - AnalysisStartTime)
    print(f"Analysis finished within {h}hr {m}min {s}sec.")

def RunSubprocess(single_batfilepath):
    subprocess.run(single_batfilepath, creationflags=subprocess.CREATE_NEW_CONSOLE)

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

def CreateGRoadWith1DSplineData():
    """
    Ground
    :return:
    """
    application.ClearMessage()
    CaseNums = [11]
    for CaseNo in CaseNums:
        rdynPath = f"D:\Research\Trailer2022\Ground_Model\Trailer_{CaseNo:03d}.rdyn"
        application.OpenModelDocument(rdynPath)
        model_document = application.ActiveModelDocument
        model = model_document.Model
        ground = IBody(model.GetEntity("Ground"))
        
        Profiles = os.walk(f"C:\\Users\LHB-MSLab\Documents\GitHub\KAERI-2022\RoadTest_2022\Case0{CaseNo}")
        for dir, subdirs, files in Profiles:
            if files and "R=" in dir and 'ModGeo' in dir:
                Roughness = 'p'.join(dir.split('\\')[-1].replace('=', '').split('.'))
                multiCurve = []
                
                idx_file = 0
                for file in files:
                    if 'csv' in file:
                        RoadOutline = ground.CreateOutlineGeometryWithFile(f"Outline_Uneven{idx_file + 1}_{Roughness}", f"{dir}\\{file}")
                        multiCurve.append(RoadOutline)
                        print(f"Outline_Uneven{idx_file + 1}_{Roughness} from {dir}\\{file}")
                        idx_file += 1
                
                print(f"Surface_Uneven_{Roughness}")
                RoadProfileSheet = IGeometrySheet(ground.CreateSplineSurfaceGeometry(f"Surface_Uneven_{Roughness}", multiCurve))
                
                data_raw = pd.read_csv(f"{dir}\\{file}")
                NumFaces = data_raw.shape[0] - 1
                FaceList = []
                for i in range(NumFaces):
                    FaceList.append(ground.GetEntity(f"Surface_Uneven_{Roughness}.Face{NumFaces - i}"))
                
                roadRefFrame = IReferenceFrame(model_document.CreateReferenceFrame())
                roadRefFrame.SetMasterPoint(AxisType.PlusZ, 0, 0, 1)
                roadRefFrame.SetSlavePoint(AxisType.PlusX, 1, 0, 0)
                ground.CreateGRoadWithFace(f"GRoad_Uneven_{Roughness}", FaceList, roadRefFrame, f"GRoad_Uneven_Case0{CaseNo}_{Roughness}.rdf")

def TireParamScaler(modelPath, TireFileName="UATire_MMKS_Trailer_Comb_Bump", radialK=1, longtitudinalK=1, lateralK=1, camberK=1, mode: str = 'scale'):
    with open(f"{modelPath}\\{TireFileName}.tir", 'r') as f:
        lines = f.readlines()
        newlines = []
        for idx, l in enumerate(lines):
            if 'stiffness' in l.lower() and '=' in l.lower():
                # Backup Comb_bump.tir
                Backups = {"RADIAL": 4645, "LONGITUDINAL": 37160, "LATERAL": 27870, "CAMBER": 141}
                Scales = {"RADIAL": radialK, "LONGITUDINAL": longtitudinalK, "LATERAL": lateralK, "CAMBER": camberK}
                l = l[:l.find('=') + 1]  # '='까지만 남기고 이후 문자열 삭제
                for key, val in Backups.items():
                    if key in l:
                        if mode == 'scale':
                            l += f" {val * Scales[key]}\n"  # 앞에 띄어쓰기 필수임?
                        elif mode == 'sub':
                            l += f" {Scales[key]}\n"  # 앞에 띄어쓰기 필수임?
            newlines.append(l)
    
    with open(f"{modelPath}\\{TireFileName}.tir", 'w') as f:
        f.writelines(newlines)

def ApplyAdaptiveSuspension():
    suspensions = []
    axis_nums = [6, 4]
    dirs = ['L', 'R']
    for n_ax in axis_nums:
        for i in range(n_ax):
            suspensions.append(f"Sus_{n_ax}_{dirs[0]}{i + 1}")
            suspensions.append(f"Sus_{n_ax}_{dirs[1]}{i + 1}")
    for sus in suspensions:
        subsys_sus = ISubSystem(model.GetEntity(sus))
        spring = IForceSpring(subsys_sus.GetEntity("Spring_Sus"))
        spring.Stiffness.UseSpline = True

def CreateSensor20RelativeDisplacements():
    CaseNo = ["011", "015"]  # ,"012"
    for idx_case, c in enumerate(CaseNo):
        Counter = 1
        #################################################################### FIX #################################################################
        model_document = application.OpenModelDocument(f"D:\Research\Trailer2022\Ground_Model\\Trailer_{c}.rdyn")
        modelPath = model_document.GetPath(PathType.WorkingFolder)
        model = model_document.Model
        direction = ['DX', 'DY', 'DZ', "ROLL", "PITCH", "YAW"]
        
        refFrame_s20 = IMarker(model.GetEntity("Sensor_20.CM"))
        refFrame_s20.RefFrame.SetEulerAngleDegree(EulerAngle.EulerAngle_ZYX,0,0,0)
        
        refFrame_init = model.GetEntity("Trailer_6.Initial")
        if refFrame_init==None:
            initialpoint=IReferenceFrame(model_document.CreateReferenceFrame())
            initialpoint.SetEulerAngleDegree(EulerAngle.EulerAngle_ZYX,0,0,0)
            initialpoint.SetOrigin(-5729., 1436.44951453657, 2697.7828)
            baseBody=IBody(model.GetEntity("Trailer_6"))
            model.CreateMarker("Initial",baseBody,initialpoint)
            refFrame_init=IMarker(model.GetEntity("Trailer_6.Initial"))
        refFrame_init=IMarker(refFrame_init)
        refFrame_init.RefFrame.SetEulerAngleDegree(EulerAngle.EulerAngle_ZYX,0,0,0)
        
        
        for dir in direction:
            model.CreateExpressionWithArguments(f"Ex_{dir}_Sensor_20", f"{dir}(1,2)", ["Sensor_20.CM", "Trailer_6.Initial"])
        model_document.FileSave(f"D:\Research\Trailer2022\Ground_Model\\Trailer_{c}.rdyn",True)



if __name__ == '__main__':
    application, model_document, plot_document, model = initialize()
    # application.Settings.CoreNumber = 8
    #
    #
    # CreateSensor20RelativeDisplacements()
    
    AnalysisFolderName = "221206_Test1"
    RunDOE_Batch(AnalysisFolderName, NumCPUCores=0, NumParallelBatches=5, NumBatRunsOnThisPC=2)
    RPLT2CSV(f"D:\Research\Trailer2022\Ground_Model\\{AnalysisFolderName}")
    
    
    
    # ApplyAdaptiveSuspension()
    # AnalysisStartTime=time.time()
    # batfilespath = WriteBatch(f"221202_RandomFuck", 7)
    # run = joblib.Parallel(n_jobs=2)(joblib.delayed(RunSubprocess)(bat) for bat in batfilespath[:2])
    # AnalysisEndTime = time.time()
    # h, m, s = DP.Sec2Time(AnalysisEndTime - AnalysisStartTime)
    # print(f"Analysis finished within {h}hr {m}min {s}sec.")    # CreateGRoadWith1DSplineData()
    #
    
    dispose()
    
    """
    GTireGroup에 GRoad 설정하는법
    for roadName in Roads:
        for i in range(40):
            Tire.ITireGroupGeneric(model.GetEntity(f"GTireGroup{i+1}")).Road=f"Ground.{roadName}"
        ExportSolverFiles(SolverFilesFolderName, f"Case{c}_{roadName.split('_')[-1]}", EndTime=EndTime, NumSteps=NumSteps)
        Counter += 1
    
    사용 코어 수 변경
    application.Settings.CoreNumber=8
    
    여러개 모델 다룰 시에 'model'변수에 주의...ChangePVvalue가 제대로 작동하지 않을 수 있음.
    """
