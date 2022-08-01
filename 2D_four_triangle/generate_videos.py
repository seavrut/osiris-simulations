import sys
sys.path.append('../')
import Plot

print()
print('Making E field movie...')
Plot.movie('MS/FLD/e2/', fps=10, res=1, out_name='n 0-2.mp4', overlay=True, vmax=0.001, vmin=-0.001, figsize=(7,6), aspect='equal');


print()
print('Making FFT movie...')
Plot.fft2_movie('MS/FLD/e2/', out_name='n 0-2 FFT.mp4', xlim=[0.4,1.6], ylim=[-0.7,0.7]);


print()
print('Making E field squared movie...')
Plot.movie('MS/FLD/e2/', fps=10, res=1, out_name='n 0-2 squared.mp4', overlay=True, f=lambda x:x**2,vmax=5e-6, vmin=0, figsize=(7,6), aspect='equal', cmap='nipy_spectral');