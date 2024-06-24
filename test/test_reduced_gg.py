import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pygrib
import pytest
from cartopy.util import add_cyclic_point

from . import sample_dir


@pytest.mark.skip
@pytest.mark.mpl_image_compare(tolerance=20, remove_text=True)
def test_reduced_gg():
    grbs = pygrib.open(sample_dir("ecmwf_tigge.grb"))
    grb = grbs.select(parameterName="Soil moisture")[0]
    fld = grb.values
    lats, lons = grb.latlons()

    # test redtoreg function
    grb.expand_grid(False)
    fld_tst = pygrib.redtoreg(grb.values, grb.pl, missval=grb.missingValue)
    assert np.allclose(fld, fld_tst)

    lons1 = lons[0, :]
    lats1 = lats[:, 0]
    # add cyclic (wrap-around) point to global grid
    fld, lons1 = add_cyclic_point(fld, coord=lons1)
    lons, lats = np.meshgrid(lons1, lats1)
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    cs = ax.contourf(lons, lats, fld, 15, cmap=plt.cm.jet)
    plt.colorbar(cs, shrink=0.6)
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    gl.right_labels = False
    gl.top_labels = False
    plt.title(grb.parameterName + " on ECMWF Reduced Gaussian Grid")
    return fig


# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != "agg":
    test_reduced_gg()
    plt.show()
