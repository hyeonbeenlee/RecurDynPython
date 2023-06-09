import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt
from scipy.interpolate import Akima1DInterpolator as akispl
from scipy.stats import spearmanr

def corrcoef_async(time_ref, vec1, time2, vec2):
    interp = akispl(time2, vec2)
    new_vec2 = interp(time_ref)
    corr = np.corrcoef(np.stack([vec1, new_vec2], axis=1), rowvar=False)
    return np.abs(corr[0,1])

def spearmanr_async(time_ref, vec1, time2, vec2):
    interp = akispl(time2, vec2)
    new_vec2 = interp(time_ref)
    corr = spearmanr(np.stack([vec1, new_vec2], axis=1)).statistic
    return np.abs(corr)

def FiltButterworth(data_1darray, cutoff, timestep, order, mode: str = 'low'):
    f_sampling = 1 / timestep
    nyq = f_sampling * 0.5
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, btype=mode, analog=False, output='sos')
    data_1darray = sosfiltfilt(sos, data_1darray, axis=0)
    return data_1darray

def FFT(data_1D, timestep):
    n_samples = len(data_1D)
    Freq = np.fft.rfftfreq(n=n_samples, d=timestep)
    Amp = np.abs(np.fft.rfft(data_1D, n=n_samples, norm='forward')) * 2  # Drop imaginary and double amplitude
    return Freq, Amp

def FFT1(data, t: np.array = None, return_complex: bool = False):
    """
    @param data: Row-> temporal samples of signal, Column-> Different signals
    @type data: array_like (2D expected)
    @param t: time vector. Defaults to None. If given, returns frequency vector.
    @type t: array_like (1D expected)
    @return: Double sided 1D Fourier transformation with frequency vector if t is given.
    @rtype: array_like (2D)
    """
    n_samples = data.shape[0]
    # Compute FFT along temporal axis
    a_fft = np.fft.fft(data, axis=0)
    a_fft *= 2 / n_samples  # Normalize
    phase_angles = np.angle(a_fft) * 180 / np.pi
    if not return_complex:
        a_fft = np.abs(a_fft)
    # if time vector given
    if t is not None:
        t = t.flatten()
        Fs = 1 / (t[1] - t[0])  # Should be uniformly sampled in time...
        f_fft = np.arange(n_samples) * (Fs / n_samples)
        f_fft = f_fft[:n_samples // 2 + 1]
        f_fft_ = -np.flip(f_fft)  # Negative frequency terms
        f_fft = np.concatenate([f_fft, f_fft_], axis=0)[:n_samples]
        return a_fft, f_fft
    else:
        return a_fft

def IFFT1(data_fft1):
    """
    @param data_fft1: output of FFT1
    @type data_fft1: array_like
    @return: Inverse Fourier transformation of input
    @rtype: np.array
    """
    n_samples = data_fft1.shape[0]
    return np.fft.ifft(data_fft1, axis=0) / 2 * n_samples  # Divide by 2 for IFFT

def RFFT1(data, t: np.array = None, return_complex: bool = False):
    """
    @param data: REAL Row-> temporal samples of signal, Column-> Different signals
    @type data: array_like (2D expected)
    @param t: time vector. Defaults to None. If given, returns frequency vector.
    @type t: array_like (1D expected)
    @return: Double sided 1D Fourier transformation with frequency vector if t is given.
    @rtype: array_like (2D)
    """
    n_samples = data.shape[0]
    # Compute FFT along temporal axis
    a_fft = np.fft.rfft(data, axis=0)
    a_fft *= 2 / n_samples  # Normalize
    phase_angles = np.angle(a_fft) * 180 / np.pi
    if not return_complex:
        a_fft = np.abs(a_fft)
    # if time vector given
    if t is not None:
        t = t.flatten()
        Fs = 1 / (t[1] - t[0])  # Should be uniformly sampled in time...
        f_fft = np.arange(n_samples) * (Fs / n_samples)  # Normalize
        f_fft = f_fft[:n_samples // 2 + 1]  # One-sided
        return a_fft, f_fft
    else:
        return a_fft

def IRFFT1(data_rfft1):
    """
    @param data_rfft1: output of RFFT1
    @type data_rfft1: array_like
    @return: REAL Inverse Fourier transformation of input
    @rtype: np.array
    """
    n_samples = data_rfft1.shape[0]
    return np.fft.irfft(data_rfft1, axis=0) * n_samples  # Do not divide by 2 for IRFFT

def PCA(data_2D: np.array, n_components: int):
    """
    @param data_2D: Row->samples, Column->features
    @type data_2D: array_like
    @param n_components: Number of features to preserve
    @type n_components: int
    @return: reduced_data, restored_data, singular_values
    @rtype: array_like, array_like, array_1D
    """
    if n_components > data_2D.shape[1]:
        raise UserWarning(f"n_components cannot exceed the number of features ({data_2D.shape[1]}) of data array.")
    # Standardize
    mean = data_2D.mean(axis=0)
    std = data_2D.std(axis=0)
    data = (data_2D - mean) / std
    u, s, vh = np.linalg.svd(data)
    s = np.diag(s)
    u_t = u[:, :n_components]
    s_t = s[:n_components, :n_components]
    vh_t = vh[:n_components, :]
    reduced_data = u_t @ s_t
    restored_data = (u_t @ s_t @ vh_t) * std + mean
    singular_values = s.diagonal()
    return reduced_data, restored_data, singular_values
