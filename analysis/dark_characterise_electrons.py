"""
Analyse dark current maps (in normalised ADU/s) generated using the calibration functions.
The dark current is converted from normalised ADU/s to electrons/s using a gain map.

Command line arguments:
    * `file`: the location of the dark current map to be analysed.
    This map should be an NPY file generated using ../calibration/dark_current.py.

Example:
    python analysis/dark_characterise_electrons.py ~/SPECTACLE_data/iPhone_SE/intermediaries/dark_current_iso23.npy
"""
from sys import argv
import numpy as np
from spectacle import io

# Get the data file from the command line
file = io.path_from_input(argv)
root = io.find_root_folder(file)

# Load Camera object
camera = io.load_camera(root)
print(f"Loaded Camera object: {camera}")

# Save locations
savefolder = camera.filename_analysis("dark_current", makefolders=True)
save_to_maps = savefolder/"dark_current_map_electrons.pdf"
save_to_histogram = savefolder/"dark_current_histogram_electrons.pdf"

# Load the data
dark_current_normADU = np.load(file)
print("Loaded data")

# Convert the data to photoelectrons per second
dark_current_electrons = camera.convert_to_photoelectrons(dark_current_normADU)

# Convolve the map with a Gaussian kernel and plot an image of the result
camera.plot_gauss_maps(dark_current_electrons, colorbar_label="Dark current (e-/s)", saveto=save_to_maps)
print(f"Saved Gauss map to '{save_to_maps}'")

# Split the data into the RGBG2 filters and make histograms (aggregate and per
# filter)
camera.plot_histogram_RGB(dark_current_electrons, xlabel="Dark current (e-/s)", saveto=save_to_histogram)
print(f"Saved RGB histogram to '{save_to_histogram}'")
