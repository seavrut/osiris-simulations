import sys
sys.path.append('../')
import Plot

print()
print('Making E2 field movie...')
Plot.movie('MS/FLD/e2/', fps=15, res=1, out_name='e2 trial 1.mp4', figsize=(15,5));


print()
print('Making E1 field movie...')
Plot.movie('MS/FLD/e1/', fps=15, res=1, out_name='e1 trial 1.mp4', figsize=(15,5));

#print()
#print('Making FFT movie...')
#Plot.fft2_movie('MS/FLD/e2/', out_name='out FFT.mp4', xlim=[0.4,1.6], ylim=[-0.7,0.7]);


#print()
#print('Making E field squared movie...')
#Plot.movie('MS/FLD/e2/', fps=15, res=1, out_name='out squared.mp4', overlay=True, f=lambda x:x**2,vmax=5e-4, vmin=0, figsize=(25,3), aspect='equal', cmap='nipy_spectral');