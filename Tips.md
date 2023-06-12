# Force
## Force를 생성하고 Expression으로 거동 부여하기
```
TraForce = IForceTranslational(model.GetEntity("Name_Force"))
TraForce.ExpressionFX = IExpression(model.GetEntity("Ex_F31AX"))
TraForce.ExpressionFY = IExpression(model.GetEntity("Ex_F31AY"))
TraForce.ExpressionFZ = IExpression(model.GetEntity("Ex_F31AZ"))

RotForce = IForceRotational(model.GetEntity("Rotational_LMM"))
RotForce.ExpressionTX = IExpression(model.GetEntity("Ex_F31GX"))
RotForce.ExpressionTY = IExpression(model.GetEntity("Ex_F31GY"))
RotForce.ExpressionTZ = IExpression(model.GetEntity("Ex_F31GZ"))
```

# Marker
## Body1에서 좌표를 가져오고 Body2에서 마커 생성하기
```
Body1 = IBody(model.GetEntity("Name_Body1"))
Body2 = IBody(model.GetEntity("Name_Body2"))
Marker=IMarker(Body1.GetEntity("CM"))
refFrame = model_document.CreateReferenceFrame()
refFrame.SetOrigin(X, Y, Z)
refFrame.SetEulerAngle(EulerAngle.EulerAngle_ZYX, 0, 0, 0)
Body2.CreateMarker(f"Name_Marker2", refFrame)
```

## Body를 지정하고 CM marker의 원점 좌표 얻기
```
Body = IBody(model.GetEntity(f"{name_body}"))
X, Y, Z = Body.GetReferenceFrameInfoOfCenterMarker().GetOrigin()
```

# Expression

## Argument 포함된 expression 만들기
```
# 이름, 내용, arguments (리스트 순서대로 넘버링)
model.CreateExpressionWithArguments("Ex_ATX_CM", "ACCX(1)", ["Cask.Marker_CaskCradleCM"])
```

## 외부 시계열 데이터로 Expression 만들기
```
file_spline='*.csv' # (N,2) without headers
name_spline='Sp_test'
name_expression='Ex_test'
model.CreateSplineWithFile(name_spline, file_spline)
model.CreateExpression(name_expression, f"AKISPL(TIME,0,{name_spline},0)")
```


# Parametric Value
## Parametric Value 변경 방법

```
from utils.modeling import ChangePVvalue
ChangePVvalue()
```

## Parametric Value 를 Python 변수로 가져오는 법

```
value=IParametricValue(model.GetEntity('PV_test')).Value
```

# GRoad

## GTireGroup에 GRoad 설정하는법

```
for roadName in Roads:
    for i in range(40):
        Tire.ITireGroupGeneric(model.GetEntity(f"GTireGroup{i+1}")).Road=f"Ground.{roadName}"
    ExportSolverFiles(SolverFilesFolderName, f"Case{c}_{roadName.split('_')[-1]}", EndTime=EndTime, NumSteps=NumSteps)
    Counter += 1
```


# Misc.

## 사용 코어 수 변경

```
application.Settings.CoreNumber=8
```

## Tips

* 여러개 모델 다룰 시에 `model` 변수에 주의, `utils.modeling.ChangePVvalue`가 제대로 작동하지 않을 수 있음.
* 리커다인 플롯 창 켜놓고 DOE 코드 실행할 경우 실행 안되니 주의.
