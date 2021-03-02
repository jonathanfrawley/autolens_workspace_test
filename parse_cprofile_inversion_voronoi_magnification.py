import pstats
from pstats import SortKey
p = pstats.Stats('profile_slow.prof')
#p.strip_dirs().sort_stats(-1).print_stats()
#p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()
#p.strip_dirs().sort_stats('tottime').print_stats()

# TODO Get total time


#    fit = al.FitImaging(masked_imaging=masked_imaging, tracer=tracer)
#    fit.log_evidence

#p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats('FitImaging')
#p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats('log_evidence')

def print_stats(section_name, stat_list):
    print(f'##### {section_name}:')
    for stat in stat_list:
        p.sort_stats(SortKey.CUMULATIVE).print_stats(rf'\b{stat}\b')

print_stats('Fit time', ['FitImaging', 'log_evidence'])
print_stats('Lens Light', ['image_from_grid'])
print_stats('Lens Light Convolution', ['convolved_image_from_image_and_blurring_image'])
print_stats('Ray Tracing', ['deflections_from_grid', 'traced_grids_of_planes_from_grid'])
print_stats('Image-plane Pixelization (Gridding)', ['from_grid_and_unmasked_2d_grid_shape'])
print_stats('Border Relocation', ['relocated_grid_from_grid'])
print_stats('Border Relocation Pixelization', ['relocated_pixelization_grid_from_pixelization_grid'])
print_stats('Voronoi Mesh', ['Grid2DVoronoi'])
print_stats('Image-Source Pairing', ['pixelization_index_for_sub_slim_index'])
print_stats('Mapping Matrix (f)', ['mapping_matrix_from'])
print_stats('Blurred Mapping Matrix (f_blur)', ['convolve_mapping_matrix'])
print_stats('Data Vector (D)', ['data_vector_via_blurred_mapping_matrix_from'])
print_stats('Curvature Matrix (F)', ['curvature_matrix_via_mapping_matrix_from'])
print_stats('Regularization Matrix (H)', ['constant_regularization_matrix_from'])
print_stats('F + Lambda H', ['add'])
print_stats('Source Reconstruction (S)', ['solve'])
print_stats('Log Det', ['sum', 'log', 'diag', 'cholesky'])
print_stats('Image Reconstruction', ['mapped_reconstructed_data_from'])
