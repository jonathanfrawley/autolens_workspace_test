"""
__Transdimensional Pipelines__

This transdimensional pipeline runner loads a strong lens dataset and analyses it using a transdimensional lens
modeling pipeline.

Using a pipeline composed of three phases this runner fits `Interferometer` data of a strong lens system, where in
the final phase of the pipeline:
.
 - The lens `Galaxy`'s light is omitted from the data and model.
 - The lens `Galaxy`'s total mass distribution is modeled as an `EllipticalPowerLaw`.
 - The source galaxy is modeled using an `Inversion`.

This uses the pipeline (Check it out full description of the pipeline):

 `autolens_workspace/transdimensional/interferometer/pipelines/mass_power_law__source_inversion.py`.
"""
from os import path
import autolens as al
import autolens.plot as aplt
import numpy as np

dataset_name = "mass_sie__source_sersic"
pixel_scales = 0.2

# dataset_path = path.join("dataset", "interferometer", dataset_name)
dataset_path = path.join("dataset", "instruments", "sma")

"""Using the dataset path, load the data (image, noise-map, PSF) as an `Interferometer` object from .fits files."""

interferometer = al.Interferometer.from_fits(
    visibilities_path=path.join(dataset_path, "visibilities.fits"),
    noise_map_path=path.join(dataset_path, "noise_map.fits"),
    uv_wavelengths_path=path.join(dataset_path, "uv_wavelengths.fits"),
)

interferometer_plotter = aplt.InterferometerPlotter(interferometer=interferometer)
interferometer_plotter.subplot_interferometer()

"""
The perform a fit, we need two masks, firstly a ‘real-space mask’ which defines the grid the image of the lensed 
source galaxy is evaluated using.
"""

real_space_mask = al.Mask2D.circular(
    shape_native=(200, 200), pixel_scales=0.2, radius=3.0
)

"""We also need a ‘visibilities mask’ which defining which visibilities are omitted from the chi-squared evaluation."""

visibilities_mask = np.full(fill_value=False, shape=interferometer.visibilities.shape)

"""
__Settings__

The `SettingsPhaseInterferometer` describe how the model is fitted to the data in the log likelihood function.

These settings are used and described throughout the `autolens_workspace/examples/model` example scripts, with a 
complete description of all settings given in `autolens_workspace/examples/model/customize/settings.py`.

The settings chosen here are applied to all phases in the pipeline.
"""

settings_masked_interferometer = al.SettingsMaskedInterferometer(
    grid_class=al.Grid2D, sub_size=2, transformer_class=al.TransformerNUFFT
)

"""
We also specify the *SettingsInversion*, which describes how the `Inversion` fits the source `Pixelization` and 
with `Regularization`. 

This can perform the linear algebra calculation that performs the `Inversion` using two options: 

 - As matrices: this is numerically more accurate and does not approximate the `log_evidence` of the `Inversion`. For
  datasets of < 100 0000 visibilities we recommend that you use this option. However, for > 100 000 visibilities this
  approach requires excessive amounts of memory on your computer (> 16 GB) and thus becomes unfeasible. 

 - As linear operators: this numerically less accurate and approximates the `log_evidence` of the `Inversioon`. However,
 it is the only viable options for large visibility datasets. It does not represent the linear algebra as matrices in
 memory and thus makes the analysis of > 10 million visibilities feasible.

By default we use the linear operators approach.  
"""

settings_inversion = al.SettingsInversion(use_linear_operators=True)

"""
`Inversion`'s may infer unphysical solution where the source reconstruction is a demagnified reconstruction of the 
lensed source (see **HowToLens** chapter 4). 

To prevent this, auto-positioning is used, which uses the lens mass model of earlier phases to automatically set 
positions and a threshold that resample inaccurate mass models (see `examples/model/positions.py`).

The `auto_positions_factor` is a factor that the threshold of the inferred positions using the previous mass model are 
multiplied by to set the threshold in the next phase. The *auto_positions_minimum_threshold* is the minimum value this
threshold can go to, even after multiplication.
"""

settings_lens = al.SettingsLens(
    auto_positions_factor=3.0, auto_positions_minimum_threshold=0.8
)

settings = al.SettingsPhaseInterferometer(
    settings_masked_interferometer=settings_masked_interferometer,
    settings_inversion=settings_inversion,
    settings_lens=settings_lens,
)

"""
__Pipeline_Setup__:

Pipelines use `Setup` objects to customize how different aspects of the model are fitted. 

First, we create a `SetupMassTotal`, which customizes:

 - The `MassProfile` used to fit the lens's total mass distribution.
 - If there is an `ExternalShear` in the mass model or not.
"""

setup_mass = al.SetupMassTotal(with_shear=True)

"""
Next, we create a `SetupSourceInversion` which customizes:

 - The `Pixelization` used by the `Inversion` in phase 3 onwards in the pipeline.
 - The `Regularization` scheme used by the `Inversion` in phase 3 onwards in the pipeline.
"""

setup_source = al.SetupSourceInversion(
    pixelization_prior_model=al.pix.VoronoiMagnification,
    regularization_prior_model=al.reg.Constant,
)

"""
_Pipeline Tagging_

The `Setup` objects are input into a `SetupPipeline` object, which is passed into the pipeline and used to customize
the analysis depending on the setup. This includes tagging the output path of a pipeline. For example, if `with_shear` 
is True, the pipeline`s output paths are `tagged` with the string `with_shear`.

This means you can run the same pipeline on the same data twice (e.g. with and without shear) and the results will go
to different output folders and thus not clash with one another!

The `path_prefix` below specifies the path the pipeline results are written to, which is:

 `autolens_workspace/output/transdimensional/dataset_type/dataset_name` 
 `autolens_workspace/output/transdimensional/interferometer/mass_sie__source_sersic`
 
The redshift of the lens and source galaxies are also input (see `examples/model/customize/redshift.py`) for a 
description of what inputting redshifts into **PyAutoLens** does.
"""

setup = al.SetupPipeline(
    path_prefix=path.join("transdimensional", dataset_name),
    redshift_lens=0.5,
    redshift_source=1.0,
    setup_mass=setup_mass,
    setup_source=setup_source,
)

"""
__Pipeline Creation__

To create a pipeline we import it from the pipelines folder and run its `make_pipeline` function, inputting the 
`Setup` and `SettingsPhase` above.
"""

from pipelines import mass_total__source_inversion

pipeline = mass_total__source_inversion.make_pipeline(
    setup=setup, settings=settings, real_space_mask=real_space_mask
)

"""
__Pipeline Run__

Running a pipeline is the same as running a phase, we simply pass it our lens dataset and mask to its run function.
"""

pipeline.run(dataset=interferometer, mask=visibilities_mask)
