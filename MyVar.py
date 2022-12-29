Key = 'trailer2022_ground'

# # Trailer2022
if Key == 'trailer2022_sea':
    DataExportTargets = ["TIME",
                         "Force/Translational Force/Translational_LMM/FX_Translational",
                         "Force/Translational Force/Translational_LMM/FY_Translational",
                         "Force/Translational Force/Translational_LMM/FZ_Translational",
                         "Force/Rotational Force/Rotational_LMM/TX_Rotational",
                         "Force/Rotational Force/Rotational_LMM/TY_Rotational",
                         "Force/Rotational Force/Rotational_LMM/TZ_Rotational",
                         
                         "Bodies/Sensor_A24/Pos_TX",
                         "Bodies/Sensor_A24/Pos_TY",
                         "Bodies/Sensor_A24/Pos_TZ",
                         "Bodies/Sensor_A24/Vel_TX",
                         "Bodies/Sensor_A24/Vel_TY",
                         "Bodies/Sensor_A24/Vel_TZ",
                         "Bodies/Sensor_A24/Acc_TX",
                         "Bodies/Sensor_A24/Acc_TY",
                         "Bodies/Sensor_A24/Acc_TZ",
                         ]
if Key == 'trailer2022_ground':
    DataExportTargets = ["TIME",
                         "Expression/Ex_Scale_VX",
                         "Expression/Ex_Scale_VY",
                        # Input
                         "Force/Translational Force/Translational_Driving/FX_Translational",
                         "Force/Translational Force/Translational_Driving/FY_Translational",
                         # Trailer6 CM
                         "Bodies/Trailer_6/Pos_TX",
                         "Bodies/Trailer_6/Pos_TY",
                         "Bodies/Trailer_6/Pos_TZ",
                         "Bodies/Trailer_6/Vel_TX",
                         "Bodies/Trailer_6/Vel_TY",
                         "Bodies/Trailer_6/Vel_TZ",
                         "Bodies/Trailer_6/Acc_TX",
                         "Bodies/Trailer_6/Acc_TY",
                         "Bodies/Trailer_6/Acc_TZ",

                         # Trailer
                         "Bodies/Sensor_23/Pos_TX",
                         "Bodies/Sensor_23/Pos_TY",
                         "Bodies/Sensor_23/Pos_TZ",
                         "Bodies/Sensor_23/Vel_TX",
                         "Bodies/Sensor_23/Vel_TY",
                         "Bodies/Sensor_23/Vel_TZ",
                         "Bodies/Sensor_23/Acc_TX",
                         "Bodies/Sensor_23/Acc_TY",
                         "Bodies/Sensor_23/Acc_TZ",

                         # Trunnion sensor
                         "Bodies/Sensor_20/Pos_TX",
                         "Bodies/Sensor_20/Pos_TY",
                         "Bodies/Sensor_20/Pos_TZ",
                         "Bodies/Sensor_20/Vel_TX",
                         "Bodies/Sensor_20/Vel_TY",
                         "Bodies/Sensor_20/Vel_TZ",
                         "Bodies/Sensor_20/Acc_TX",
                         "Bodies/Sensor_20/Acc_TY",
                         "Bodies/Sensor_20/Acc_TZ",

                         # GPS Velocity
                         "Bodies/Sensor_GPS/Vel_TX",
                         "Bodies/Sensor_GPS/Vel_TY",
                         
                         # Suspension displacements
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_L1/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_R1/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_L2/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_R2/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_L3/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_R3/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_L4/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_R4/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_L5/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_R5/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_L6/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_6_R6/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_L1/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_R1/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_L2/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_R2/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_L3/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_R3/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_L4/DEFL_TSDA",
                         # "Force/Translational Spring Damper/Spring_Sus@Sus_4_R4/DEFL_TSDA",
                         
                         # Sensor_20 relative displacements
                         "Expression/Ex_DX_Sensor_20",
                         "Expression/Ex_DY_Sensor_20",
                         "Expression/Ex_DZ_Sensor_20",
                         "Expression/Ex_ROLL_Sensor_20",
                         "Expression/Ex_PITCH_Sensor_20",
                         "Expression/Ex_YAW_Sensor_20",
                         ]

if Key == 'trailer2022_sea_send2kaeri':
    DataExportTargets = ["TIME",
                         "Expression/Ex_DTX_CM",
                         "Expression/Ex_DTY_CM",
                         "Expression/Ex_DTZ_CM",
                         "Expression/Ex_DRX_CM",
                         "Expression/Ex_DRY_CM",
                         "Expression/Ex_DRZ_CM",
    
                         "Expression/Ex_VTX_CM",
                         "Expression/Ex_VTY_CM",
                         "Expression/Ex_VTZ_CM",
                         "Expression/Ex_VRX_CM",
                         "Expression/Ex_VRY_CM",
                         "Expression/Ex_VRZ_CM",
    
                         "Expression/Ex_ATX_CM",
                         "Expression/Ex_ATY_CM",
                         "Expression/Ex_ATZ_CM",
                         "Expression/Ex_ARX_CM",
                         "Expression/Ex_ARY_CM",
                         "Expression/Ex_ARZ_CM", ]

elif Key == 'trailer2021dnn':
    DataExportTargets = ["TIME",
                         "Expression/Ex_Scale_VX",
                         "Expression/Ex_Scale_VY",
    
                         # "Bodies/Sensor_20/Pos_TX",
                         # "Bodies/Sensor_20/Pos_TY",
                         # "Bodies/Sensor_20/Pos_TZ",
                         # "Bodies/Sensor_20/Vel_TX",
                         # "Bodies/Sensor_20/Vel_TY",
                         # "Bodies/Sensor_20/Vel_TZ",
                         # "Bodies/Sensor_20/Acc_TX",
                         # "Bodies/Sensor_20/Acc_TY",
                         # "Bodies/Sensor_20/Acc_TZ",
                         #
                         #
                         # "Bodies/Sensor_51/Pos_TX",
                         # "Bodies/Sensor_51/Pos_TY",
                         # "Bodies/Sensor_51/Pos_TZ",
                         # "Bodies/Sensor_51/Vel_TX",
                         # "Bodies/Sensor_51/Vel_TY",
                         # "Bodies/Sensor_51/Vel_TZ",
                         # "Bodies/Sensor_51/Acc_TX",
                         # "Bodies/Sensor_51/Acc_TY",
                         # "Bodies/Sensor_51/Acc_TZ",
                         #
                         #
                         # "Bodies/Sensor_52/Pos_TX",
                         # "Bodies/Sensor_52/Pos_TY",
                         # "Bodies/Sensor_52/Pos_TZ",
                         # "Bodies/Sensor_52/Vel_TX",
                         # "Bodies/Sensor_52/Vel_TY",
                         # "Bodies/Sensor_52/Vel_TZ",
                         # "Bodies/Sensor_52/Acc_TX",
                         # "Bodies/Sensor_52/Acc_TY",
                         # "Bodies/Sensor_52/Acc_TZ",
    
    
                         "Bodies/Sensor_53/Pos_TX",
                         "Bodies/Sensor_53/Pos_TY",
                         "Bodies/Sensor_53/Pos_TZ",
                         "Bodies/Sensor_53/Vel_TX",
                         "Bodies/Sensor_53/Vel_TY",
                         "Bodies/Sensor_53/Vel_TZ",
                         "Bodies/Sensor_53/Acc_TX",
                         "Bodies/Sensor_53/Acc_TY",
                         "Bodies/Sensor_53/Acc_TZ",
                         ]

elif Key == 'trailer2021':
    DataExportTargets = ["TIME",
    
                         # "Bodies/Sensor_20/Pos_TX",
                         # "Bodies/Sensor_20/Pos_TY",
                         # "Bodies/Sensor_20/Pos_TZ",
                         # "Bodies/Sensor_20/Vel_TX",
                         # "Bodies/Sensor_20/Vel_TY",
                         # "Bodies/Sensor_20/Vel_TZ",
                         "Bodies/Sensor_20/Acc_TX",
                         "Bodies/Sensor_20/Acc_TY",
                         "Bodies/Sensor_20/Acc_TZ",
                         #
                         #
                         # "Bodies/Sensor_51/Pos_TX",
                         # "Bodies/Sensor_51/Pos_TY",
                         # "Bodies/Sensor_51/Pos_TZ",
                         # "Bodies/Sensor_51/Vel_TX",
                         # "Bodies/Sensor_51/Vel_TY",
                         # "Bodies/Sensor_51/Vel_TZ",
                         # "Bodies/Sensor_51/Acc_TX",
                         # "Bodies/Sensor_51/Acc_TY",
                         # "Bodies/Sensor_51/Acc_TZ",
                         #
                         #
                         # "Bodies/Sensor_52/Pos_TX",
                         # "Bodies/Sensor_52/Pos_TY",
                         # "Bodies/Sensor_52/Pos_TZ",
                         # "Bodies/Sensor_52/Vel_TX",
                         # "Bodies/Sensor_52/Vel_TY",
                         # "Bodies/Sensor_52/Vel_TZ",
                         # "Bodies/Sensor_52/Acc_TX",
                         # "Bodies/Sensor_52/Acc_TY",
                         # "Bodies/Sensor_52/Acc_TZ",
    
    
                         # "Bodies/Sensor_53/Pos_TX",
                         # "Bodies/Sensor_53/Pos_TY",
                         # "Bodies/Sensor_53/Pos_TZ",
                         # "Bodies/Sensor_53/Vel_TX",
                         # "Bodies/Sensor_53/Vel_TY",
                         # "Bodies/Sensor_53/Vel_TZ",
                         # "Bodies/Sensor_53/Acc_TX",
                         # "Bodies/Sensor_53/Acc_TY",
                         # "Bodies/Sensor_53/Acc_TZ",
                         ]

elif Key == 'KRISO2021':
    DataExportTargets = [
        "Joints/RevJoint2/FX_Reaction_Force",
        "Joints/RevJoint2/FY_Reaction_Force",
        "Joints/RevJoint2/TZ_Reaction_Force",
    ]

elif Key == 'doublependulum':
    DataExportTargets = [
        'TIME',
        # 'Expression/Ex_L1',
        'Expression/Ex_L2',
        'Expression/Ex_TH0_2',
        'Bodies/Rod1/Pos_YAW',
        'Bodies/Rod2/Pos_YAW',
        'Bodies/Rod1/Vel_RZ',
        'Bodies/Rod2/Vel_RZ',
        'Bodies/Rod1/Acc_RZ',
        'Bodies/Rod2/Acc_RZ',
    ]


"""
22.11.01
def GenerateDOE(TopFolderName: str, NumParallelBatches: int = 3, NumCPUCores: int = 16):
    application.ClearMessage()
    Counter = 0
    #################################################################### FIX #################################################################
    CaseNo = ["015"]  # ,"012"
    for idx_case,c in enumerate(CaseNo):
        if NumCPUCores:
            application.Settings.AutoCoreNumber = False
            application.Settings.CoreNumber = NumCPUCores
        else:
            application.Settings.AutoCoreNumber = True
        model_document = application.OpenModelDocument(f"D:\Research\Trailer2022\Ground_Model\\Trailer_{c}.rdyn")
        modelPath = model_document.GetPath(PathType.WorkingFolder)
        model = model_document.Model
        EndTime = IParametricValue(model.GetEntity("PV_EndTime")).Value
        NumSteps = IParametricValue(model.GetEntity("PV_NumSteps")).Value
        
            # ExportSolverFiles(TopFolderName, f"Case{c}_{roadname.split('_')[-1]}", EndTime=EndTime, NumSteps=NumSteps)
        Roads = [f"Ground.GRoad_Uneven_R4p00"]  # , f"Ground.GRoad_Uneven_R2p00", f"Ground.GRoad_Uneven_R4p00", f"Ground.GRoad_Uneven_R8p00", f"Ground.GRoad_Uneven_R16p00"]
        TireKScales = [0.48] #0.7 / 0.48
        SusKScales = [2] #5.00
        # SusCscales = np.linspace(-1, 1, 6, endpoint=True)
        SusCscales = [0.5] #1
        BushingKTZscales=[1]
        ScaleVXs=np.linspace(0.8,1.2,5,endpoint=True)
        ScaleVYs=np.linspace(0.8,1.2,5,endpoint=True)
        for i in range(len(TireKScales)):
            for j in range(len(SusKScales)):
                for k in range(len(SusCscales)):
                    for roadname in Roads:
                        for svx in ScaleVXs:
                            for svy in ScaleVYs:
                                for m in range(40):
                                    Tire.ITireGroupGeneric(model.GetEntity(f"GTireGroup{m + 1}")).Road = roadname
                                EditTire(modelPath, "UATire_MMKS_Trailer_Comb_Bump", TireKScales[i])
                                ChangePVvalue(model, "PV_Spring_K_6", 4754 * 5) #5
                                ChangePVvalue(model, "PV_Spring_K_4", 4754 * 15) #5
                                ChangePVvalue(model, "PV_Spring_C_6", 1000 * 0.5) #0.5
                                ChangePVvalue(model, "PV_Spring_C_4", 1000 * 1) #1
                                #################################################################### FIX #################################################################
                                ChangePVvalue(model,"PV_Scale_VX",svx)
                                ChangePVvalue(model,"PV_Scale_VY",svy)
                                SubFolderName = f"Case{c}_Train_Sx{svx:.1f}_Sy{svy:.1f}"
                                # SubFolderName = f"Case{c}_{roadname.split('_')[-1]}"
                                ExportSolverFiles(TopFolderName, SubFolderName, EndTime=EndTime, NumSteps=NumSteps)
                                
        RandomSamples=DP.LHCSampler(3,2,seed=idx_case)*0.4+0.8
        for randsample in RandomSamples:
            rand_sx,rand_sy=randsample
            ChangePVvalue(model,"PV_Scale_VX",rand_sx)
            ChangePVvalue(model,"PV_Scale_VY",rand_sy)
            SubFolderName = f"Case{c}_Test_Sx{rand_sx:.4f}_Sy{rand_sy:.4f}"
            ExportSolverFiles(TopFolderName, SubFolderName, EndTime=EndTime, NumSteps=NumSteps)
    WriteBatch(TopFolderName, NumParallelBatches)
    
    # batFiles = glob.glob(f"{TopFolderName}/*.bat")
    # for bat in batFiles:
    #     subprocess.call(r"{bat}".format(bat=bat))
    # RunBatch(SolverFilesFolderName)
    # RPLT2CSV(f"{modelPath}{TopFolderName}")
"""