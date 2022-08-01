import sys
sys.path.append('../')
import Plot


print()
print('Making E field squared movie...')
Plot.movie('MS/FLD/e2/', fps=10, res=1, out_name='brewster angle reflection.mp4', overlay=True, f=lambda x:x**2,vmax=5e-8, vmin=0, figsize=(7,6), aspect='equal', cmap='nipy_spectral');