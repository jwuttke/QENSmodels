import numpy as np
import QENSmodels


def hwhmJumpTranslationalDiffusion(q, D=2.3, resTime=1.25):
    """
    Returns some characteristics of `JumpTranslationalDiffusion`

    Parameters
    ----------
    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer

    D: float
        diffusion coefficient. Default to 2.3.

    resTime: float
        to be added. Default to 1.25.

    Returns
    -------
    hwhm: :class:`~numpy:numpy.ndarray`
        half-width half maximum

    eisf: :class:`~numpy:numpy.ndarray`
        elastic incoherent structure factor

    qisf: :class:`~numpy:numpy.ndarray`
        quasi-elastic incoherent structure factor


     Notes
    -----
    The default values for the fitting parameters come from the values
    for water at 298K and 1 atm, water has D=2.30 10^{-5} cm^2/s and
    ResTime=1.25 ps.

    """
    eisf = np.zeros(q.size)
    qisf = np.ones(q.size)
    hwhm = D * q ** 2 / (1.0 + resTime * D * q ** 2)
    # Force hwhm to be numpy array, even if single value
    hwhm = np.asarray(hwhm, dtype=np.float32)
    hwhm = np.reshape(hwhm, hwhm.size)
    return hwhm, eisf, qisf


def sqwJumpTranslationalDiffusion(w, q, scale=1, center=0, D=2.3, resTime=1.25):
    """ Lorentzian model with half width half maximum equal to :math: \frac{Dq^2}{1+ \text{resTime}Dq^2}

    Parameters
    ----------
    w: float, list or :class:`~numpy:numpy.ndarray`
        energy transfer in hbar units

    q: float, list or :class:`~numpy:numpy.ndarray`
        momentum transfer (non-fitting, in 1/Angstrom).

    scale: float
        scale factor. Default to 1.

    center: float
        center of peak. Default to 0.

    D: float
        diffusion coefficient (in 10^{-5} cm^2/s). Default to 2.3

    resTime: float
        residence time (in picoseconds). Default to 1.25

    Return
    ------
    :class:`~numpy:numpy.ndarray`
        output array

    Examples
    --------
    >>> QENSmodels.sqwJumpTranslationalDiffusion([1,2,3], 1, 1, 0, 1, 1)
    array([ 0.12732396,  0.03744822,  0.01720594])


    >>> QENSmodels.sqwJumpTranslationalDiffusion(1, 1, 1, 0, 1, 1)
    array([ 0.12732395])

    Notes
    -----

    * The `sqwJumpTranslationalDiffusion` is expressed as

      .. math::

          S(\omega, q) = \text{Lorentzian}(\omega, \text{scale}, \text{center},
          \frac{D q^2}{ 1 + \text{resTime} D q^2})

    * The default values for the fitting parameters come from the values
    for water at 298K and 1 atm, water has D=2.30 10^{-5} cm^2/s and
    ResTime=1.25 ps.


    Reference
    ----------

    J. Teixeira, M.-C. Bellissent-Funel, S.H. Chen, and A.J, Dianoux,
    **Phys. Rev. A** *31*, 1913-1917 (1985)
    `link <https://journals.aps.org/pra/abstract/10.1103/PhysRevA.31.1913>`_


    """
    # Input validation
    w = np.asarray(w, dtype=np.float32)

    q = np.asarray(q, dtype=np.float32)

    # Create output array
    sqw = np.zeros((q.size, w.size))

    # Get widths, EISFs and QISFs of model
    hwhm, eisf, qisf = hwhmJumpTranslationalDiffusion(q, D, resTime)

    # Model
    for i in range(q.size):
        sqw[i, :] = QENSmodels.lorentzian(w, scale, center, hwhm[i])

    # For Bumps use (needed for final plotting)
    # Using a 'Curve' in bumps for each Q --> needs vector array
    if q.size == 1:
        sqw = np.reshape(sqw, w.size)

    return sqw
