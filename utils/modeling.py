from recurdyn import *
import os
import sys

from recurdyn import *
from GlobalVariables import GlobVar
from . import initialize, dispose


def Import(importfile: str):
    application, model_document, plot_document, model = initialize()
    modelPath = model_document.GetPath(PathType.WorkingFolder)
    print(f"Imported file: {importfile}")
    model_document.FileImport(importfile)


def ChangePVvalue(model_document: ISubSystem, PVname: str, PVvalue: float):
    PV = IParametricValue(model.GetEntity(PVname))
    # print(PV._get_Value()) # before
    PV._set_Value(PVvalue)
    # print(PV._get_Value()) # after
    
