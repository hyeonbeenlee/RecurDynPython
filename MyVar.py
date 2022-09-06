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
                        # Input
                         "Force/Translational Force/Translational_Driving/FX_Translational",
                         "Force/Translational Force/Translational_Driving/FY_Translational",
                         # Trailer6 CM
                         "Bodies/Sensor_A27/Pos_TX",
                         "Bodies/Sensor_A27/Pos_TY",
                         "Bodies/Sensor_A27/Pos_TZ",
                         "Bodies/Sensor_A27/Vel_TX",
                         "Bodies/Sensor_A27/Vel_TY",
                         "Bodies/Sensor_A27/Vel_TZ",
                         "Bodies/Sensor_A27/Acc_TX",
                         "Bodies/Sensor_A27/Acc_TY",
                         "Bodies/Sensor_A27/Acc_TZ",

                         # Trailer
                         "Bodies/Sensor_A23/Pos_TX",
                         "Bodies/Sensor_A23/Pos_TY",
                         "Bodies/Sensor_A23/Pos_TZ",
                         "Bodies/Sensor_A23/Vel_TX",
                         "Bodies/Sensor_A23/Vel_TY",
                         "Bodies/Sensor_A23/Vel_TZ",
                         "Bodies/Sensor_A23/Acc_TX",
                         "Bodies/Sensor_A23/Acc_TY",
                         "Bodies/Sensor_A23/Acc_TZ",

                         # Trunnion sensor
                         "Bodies/Sensor_A20/Pos_TX",
                         "Bodies/Sensor_A20/Pos_TY",
                         "Bodies/Sensor_A20/Pos_TZ",
                         "Bodies/Sensor_A20/Vel_TX",
                         "Bodies/Sensor_A20/Vel_TY",
                         "Bodies/Sensor_A20/Vel_TZ",
                         "Bodies/Sensor_A20/Acc_TX",
                         "Bodies/Sensor_A20/Acc_TY",
                         "Bodies/Sensor_A20/Acc_TZ",
                         
                         "Bodies/Sensor_GPS/Vel_TX",
                         "Bodies/Sensor_GPS/Vel_TY",
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
