"""
Analyse dark current maps (in normalised ADU/s) generated using the calibration functions.

Command line arguments:
    * `file`: the location of the dark current map to be analysed.
    This map should be an NPY file generated using ../calibration/dark_current.py.

Example:
    python analysis/dark_characterise_ADU.py ~/SPECTACLE_data/iPhone_SE/intermediaries/dark_current_iso23.npy
"""
from sys import argv
import numpy as np
from spectacle import io, analyse

# Get the data file from the command line
file = io.path_from_input(argv)
root = io.find_root_folder(file)

# Load Camera object
camera = io.load_camera(root)
print(f"Loaded Camera object: {camera}")

# Save locations
savefolder = camera.filename_analysis("dark_current", makefolders=True)
save_to_maps = savefolder/"dark_current_map_ADU.pdf"
save_to_histogram = savefolder/"dark_current_histogram_ADU.pdf"

# Load the data
dark_current = np.load(file)
print("Loaded data")

# Convolve the map with a Gaussian kernel and plot an image of the result
camera.plot_gauss_maps(dark_current, colorbar_label="Dark current (norm. ADU/s)", saveto=save_to_maps)
print(f"Saved Gauss map to '{save_to_maps}'")

# Range on the x axis for the histogram
xmin, xmax = analyse.symmetric_percentiles(dark_current, percent=0.001)

# Split the data into the RGBG2 filters and make histograms (aggregate and per
# filter)
camera.plot_histogram_RGB(dark_current, xmin=xmin, xmax=xmax, xlabel="Dark current (norm. ADU/s)", saveto=save_to_histogram)
print(f"Saved RGB histogram to '{save_to_histogram}'")

# Check how many pixels are over some threshold in dark current
threshold = 50
pixels_over_threshold = np.where(np.abs(dark_current) > threshold)
number_over_threshold = len(pixels_over_threshold[0])
print(f"There are {number_over_threshold} pixels with a dark current >{threshold} normalised ADU/s.")
