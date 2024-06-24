import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pygrib
import pytest
from cartopy.util import add_cyclic_point

try:
    import spharm

except ImportError:
    spharm = None
    # print("skipping test that requires pyspharm (python spherical harmonic module) from http://code.google.com/p/pyspharm")
    # raise SystemExit(0)
from . import sample_dir

grbs = pygrib.open(sample_dir("spherical_pressure_level.grib1"))
g = grbs[1]
fld = g.values

# ECMWF normalizes the spherical harmonic coeffs differently than NCEP.
# (m=0,n=0 is global mean, instead of sqrt(2)/2 times global mean)


@pytest.mark.skipif(spharm is None, reason="spharm is not installed")
@pytest.mark.mpl_image_compare(tolerance=20, remove_text=True)
def test_spectral():
    fld = 2.0 * fld / np.sqrt(2.0)
    fldr = fld[0::2]
    fldi = fld[1::2]
    fld = np.zeros(fldr.shape, "F")
    fld.real = fldr
    fld.imag = fldi
    nlons = 360
    nlats = 181
    s = spharm.Spharmt(nlons, nlats)
    data = s.spectogrd(fld)
    lons = (360.0 / nlons) * np.arange(nlons)
    lats = 90.0 - (180.0 / (nlats - 1)) * np.arange(nlats)
    # add cyclic (wrap-around) point to global grid
    data, lons = add_cyclic_point(data, coord=lons)
    lons, lats = np.meshgrid(lons, lats)
    # setup mercator map projection.
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator(central_longitude=0))
    cs = ax.contourf(
        lons, lats, data, 15, cmap=plt.cm.jet, transform=ccrs.PlateCarree()
    )
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    gl.right_labels = False
    gl.top_labels = False
    plt.colorbar(cs, shrink=0.9)
    plt.title(
        repr(g.level)
        + " "
        + g.typeOfLevel
        + " "
        + g.name
        + " from Spherical Harmonic Coeffs",
        fontsize=9,
    )
    return fig


# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != "agg":
    test_spectral()
    plt.show()
