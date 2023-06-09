import numpy as np
import scipy

def Grad(func_ddot, t, Y):  # dY
    x = Y[0]
    xDot = Y[1]
    
    dY = np.empty(2)
    dY[0] = xDot
    dY[1] = func_ddot(t)  # Acceleration spline function
    return dY

def RK4(func_ddot, h, t, Y):
    k1 = Grad(func_ddot, t, Y)
    k2 = Grad(func_ddot, t + h / 2, Y + h * k1 / 2)
    k3 = Grad(func_ddot, t + h / 2, Y + h * k2 / 2)
    k4 = Grad(func_ddot, t + h, Y + h * k3)
    dY = (k1 / 6 + k2 / 3 + k3 / 3 + k4 / 6)
    return dY

def RK5(func_ddot, h, t, Y):
    k1 = Grad(func_ddot, t, Y)
    k2 = Grad(func_ddot, t + h / 4, Y + h * k1 / 4)
    k3 = Grad(func_ddot, t + h / 4, Y + h * k1 / 8 + h * k2 / 8)
    k4 = Grad(func_ddot, t + h / 2, Y - h * k2 / 2 + h * k3)
    k5 = Grad(func_ddot, t + 3 * h / 4, Y + 3 * h * k1 / 16 + 9 * h * k4 / 16)
    k6 = Grad(func_ddot, t + h, Y - 3 * h * k1 / 7 + 2 * h * k2 / 7 + 12 * h * k3 / 7 - 12 * h * k4 / 7 + 8 * h * k5 / 7)
    dY = (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6) / 90
    return dY

def Integrate(func_ddot, t_0: float = 0, t_end: float = 1, h: float = 1e-2, v0: float = 0, p0: float = 0, method: str = 'rk4'):
    # Initial conditions
    t = t_0
    steps = int((t_end - t_0) / h)
    Y = np.array([p0, v0])
    dY = Grad(func_ddot, t, Y)
    
    # RK integrate
    rk_time = np.zeros(steps + 1)
    rk_Y = np.zeros((steps + 1, 2))  # pos and vel
    rk_dY = np.zeros_like(rk_Y)  # update gradients
    for idx in range(steps + 1):
        # save
        rk_time[idx] = t
        rk_Y[idx] = Y
        rk_dY[idx] = dY
        
        # calculate
        if method.lower() == 'rk4':
            dY = RK4(func_ddot, h, t, Y)
        elif method.lower() == 'rk5':
            dY = RK5(func_ddot, h, t, Y)
        
        # update
        Y = Y + h * dY
        t = t + h

        # print
        if (idx + 1) % 10000 == 0:
            print(f"Solving t={t:.5f} ({idx + 1}/{steps + 1})")
    
    return rk_time, rk_Y, rk_dY

def PolyFitCustomized(x, y, deg_start, deg_end):
    A = np.zeros((deg_end - deg_start + 1, deg_end - deg_start + 1))
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A[i, j] = np.sum(x ** (deg_start * 2 + i + j))
    B = np.zeros(deg_end - deg_start + 1)
    for i in range(B.shape[0]):
        B[i] = np.sum(np.power(x, deg_start + i) * y)
    coefficients = np.linalg.solve(A, B)  # low->high order
    # Add low order coefficients
    if deg_start > 0:
        coefficients = np.concatenate((np.zeros(deg_start), coefficients), axis=0)
    return coefficients

def Integrate_Detrend(func_ddot_uncorrected, t_0=0, t_end=1, h=1e-2, v0_assumed=0, p0_assumed=0, integration_method: str = 'rk4', correction_order: int = 4):
    # Save uncorrected integration
    rk_time_uncorrected, rk_Y_uncorrected, rk_dY_uncorrected = Integrate(func_ddot_uncorrected, t_0=t_0,
                                                                         t_end=t_end, h=h,
                                                                         v0=v0_assumed, p0=p0_assumed, method=integration_method)
    # STEP 1
    # Correct acceleration with velocity
    velocity_uncorrected = rk_Y_uncorrected[:, 1]
    acc_corrective1 = np.zeros(rk_time_uncorrected.shape)  # basis
    
    coefficients = PolyFitCustomized(rk_time_uncorrected, velocity_uncorrected, 1, correction_order + 1)  # init value=0
    for order, coeff in enumerate(coefficients):
        if coeff == 0:  # 상수차수의 미분항 무시 (=0)
            continue
        else:
            acc_corrective1 += order * coeff * rk_time_uncorrected ** (order - 1)
    acceleration_corrected1 = func_ddot_uncorrected(rk_time_uncorrected) - acc_corrective1
    akispl_ddot_corrected1 = scipy.interpolate.Akima1DInterpolator(rk_time_uncorrected, acceleration_corrected1)
    # Integrate velocity corrected acceleration
    rk_time_corrected1, rk_Y_corrected1, rk_dY_corrected1 = Integrate(akispl_ddot_corrected1,
                                                                      t_end=t_end, h=h, t_0=t_0,
                                                                      v0=v0_assumed, p0=p0_assumed, method=integration_method)
    
    # STEP 2
    # Correct acceleration with displacement from velocity-corrected acceleration
    acc_corrective2 = np.zeros(rk_time_corrected1.shape)
    displacement_corrected1 = rk_Y_corrected1[:, 0]
    coefficients = PolyFitCustomized(rk_time_corrected1, displacement_corrected1, 2, correction_order + 2)
    for order, coeff in enumerate(coefficients):
        if coeff == 0:
            continue
        else:
            acc_corrective2 += order * (order - 1) * coeff * rk_time_corrected1 ** (order - 2)
    acceleration_corrected2 = acceleration_corrected1 - acc_corrective2
    akispl_ddot_corrected2 = scipy.interpolate.Akima1DInterpolator(rk_time_corrected1, acceleration_corrected2)
    # Integrate displacement corrected acceleration
    rk_time_corrected2, rk_Y_corrected2, rk_dY_corrected2 = Integrate(akispl_ddot_corrected2,
                                                                      t_end=t_end, h=h, t_0=t_0,
                                                                      v0=v0_assumed, p0=p0_assumed, method=integration_method)
    
    return rk_time_corrected2, rk_Y_corrected2, rk_dY_corrected2
