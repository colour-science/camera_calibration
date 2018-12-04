import numpy as np
from sys import argv
from phonecal import io, raw
from matplotlib import pyplot as plt

folder, wvl = io.path_from_input(argv)
wvl = wvl.stem
root, images, stacks, products, results = io.folders(folder)
phone = io.read_json(root/"info.json")

colours     = io.load_colour(stacks)

m = np.load(folder/f"{wvl}_mean.npy")
s = np.load(folder/f"{wvl}_stds.npy")

s[s < 0.001] = -1  # prevent infinities

SNR = m/s

m_RGBG, offsets = raw.pull_apart(m, colours)
s_RGBG, offsets = raw.pull_apart(s, colours)
SNR_RGBG, offsets = raw.pull_apart(SNR, colours)

mean_stack = m_RGBG.mean(axis=(1,2))
std_stack  = m_RGBG.std (axis=(1,2))
SNR_stack = mean_stack / std_stack

for j,c in enumerate("RGBG"):
    SNR_here = SNR_RGBG[j].ravel()
    mean_here = m_RGBG[j].ravel()
    plt.figure(figsize=(10,3))
    plt.hist(SNR_here, bins=np.arange(0,100,1), color=c)
    plt.xlabel("SNR")
    plt.axvline(3, c='k', ls="--")
    plt.xlim(0,100)
    plt.show()
    plt.close()

    print(f"{c}: SNR: {np.percentile(SNR_here, 5):.2f} -- {np.percentile(SNR_here, 95):.2f}")
    print(f"{c}: Mean: {np.percentile(mean_here, 5):.2f} -- {np.percentile(mean_here, 95):.2f}")
