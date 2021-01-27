from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to customize the Matplotlib legend of a PyAutoLens figures and subplot.

First, lets load an example Hubble Space Telescope image of a real strong lens as an `Array2D`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array2D.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can customize the legend using the `Legend` matplotlib wrapper object which wraps the following method(s):

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.legend.html
"""

legend = aplt.Legend(include_2d=True, loc="upper left", fontsize=10, ncol=2)

mat_plot_2d = aplt.MatPlot2D(legend=legend)

array_plotter = aplt.Array2DPlotter(array=image, mat_plot_2d=mat_plot_2d)
array_plotter.figure()