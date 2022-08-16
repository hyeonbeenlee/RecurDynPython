Key = 'trailer2021'

# # Trailer2022
if Key == 'trailer2022_sea':
    DataExportTargets = ["TIME",
                         "Bodies/Sensor_A24/Acc_TX",
                         "Bodies/Sensor_A24/Acc_TY",
                         "Bodies/Sensor_A24/Acc_TZ",
                         
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
                         "Expression/Ex_ARZ_CM",
                         ]

elif Key == 'trailer2021':
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

elif Key == 'KRISO2021':
    DataExportTargets = [
        "Joints/RevJoint2/FX_Reaction_Force",
        "Joints/RevJoint2/FY_Reaction_Force",
        "Joints/RevJoint2/TZ_Reaction_Force",
    ]

elif Key=='doublependulum':
    DataExportTargets=[
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