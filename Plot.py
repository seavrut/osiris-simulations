from inspect import findsource
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

from tftb.processing.cohen import WignerVilleDistribution as WVD
from tftb.processing.cohen import Spectrogram

sys.path.append('/Users/avrutsky/College/Lab/pyVisOS/')
import osh5def
import osh5io
import osh5vis
import osh5utils

def x(ax:plt.Axes, filename:str, **kwargspassthrough):
    """Plot x plasma distribution.\n
    ax: axes to plot on
    filename: (e.g. 'x1-electrons-000000.h5')\n
    returns -> data read from file as H5Data object, imshow image"""

    #fig, ax = plt.subplots(1,1, figsize=(20,8), dpi=300)
    
    fnm_split = filename.split('-')
    fnm_split.insert(0, 'MS')
    if filename[0:3] != 'RAW':
        fnm_split.insert(1, 'PHA')
    fnm_split[-1] = filename
    path = '/'.join(fnm_split)
    data = osh5io.read_h5(path)
    if np.array_equal(data.view(np.ndarray), np.zeros_like(data.view(np.ndarray))):
        im = osh5vis.osplot(data, ax=ax, vmax=0.0, vmin=-0.5, **kwargspassthrough)
    else:
        im = osh5vis.osplot(data, ax=ax, **kwargspassthrough)
    #ax.grid()
    return data, im

def x_scatter(ax:plt.Axes, filename:str, **kwargspassthrough):
    """Plot x plasma distribution as scatter plot.\n
    ax: axes to plot on
    filename: (e.g. 'x1-electrons-000000.h5')
    returns -> data read from file as H5Data object, scatter plot"""

    #fig, ax = plt.subplots(1,1, figsize=(20,8), dpi=300)
    fnm_split = filename.split('-')
    fnm_split.insert(0, 'MS')
    fnm_split.insert(1, 'PHA')
    fnm_split[-1] = filename
    path = '/'.join(fnm_split)

    dim = int(filename[1]) # x1 or x2 or x3?

    data = osh5io.read_h5(path)
    x = np.linspace(data.run_attrs['XMIN'][dim-1], data.run_attrs['XMAX'][dim-1], int(data.run_attrs['NX'][dim-1]))
    ax.grid()
    im = ax.scatter(x,data, **kwargspassthrough)
    return data, im

def xt(ax:plt.Axes, pre:str, **kwargspassthrough):
    """Plot xt colormap plot.\n
    ax: axes to plot on
    pre: prefix of files (e.g. 'e2')\n
    returns -> 2d data array, imshow image"""

    mat = osh5utils.combine('MS/FLD/' + pre + '/', prefix=pre+'-')
    im = osh5vis.osimshow(mat.T, ax = ax, **kwargspassthrough)
    return mat, im

def wk(ax:plt.Axes, pre:str, **kwargspassthrough):
    """Plot wk matrix plot.\n
    ax: axes to plot on
    pre: prefix of files (e.g. 'e2')\n
    returns -> 2d data array, imshow image"""

    mat = osh5utils.combine('MS/FLD/' + pre + '/', prefix=pre+'-')
    im = osh5vis.osimshow(np.abs(osh5utils.fft2(mat)), ax = ax, **kwargspassthrough)
    return mat, im

def Ex(ax:plt.Axes, filename:str, dir:str = 'MS/FLD/', f=None, *args, **kwargspassthrough):
    """Plot E(x) (or B(x)) at a given time.\n
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')\n
    f: function to apply to data (e.g. lambda x : x**2)
    args: additional function parameters if necessary
    kwargspassthrough: additional graphing parameters\n
    returns -> data read from file as H5Data object, imshow image"""

    #fig, ax = plt.subplots(1,1, figsize=(20,8), dpi=300)
    e_ = filename[0:2]
    data = osh5io.read_h5(dir + e_ + '/' + filename)
    if f != None:
        data = f(data, *args)
    
    im = osh5vis.osplot(data, ax=ax, **kwargspassthrough)
    ax.grid()
    return data, im

def Efft(ax:plt.Axes, filename:str, dir:str = 'MS/FLD/', f=None, *args, **kwargspassthrough):
    """Plot K(x) at a given time using FFT.\n
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')
    f: function to apply beforehand (e.g. lambda x : x**2)
    args: additional function parameters if necessary
    kwargspassthrough: additional graphing parameters\n
    returns -> data read from file as H5Data object, imshow image"""

    e_ = filename[0:2]
    data = osh5io.read_h5(dir + e_ + '/' + filename)
    if f != None:
        data = f(data, *args)
    ax.grid()
    im = osh5vis.osplot(np.abs(osh5utils.fft(data)), xlim=[-4,4], **kwargspassthrough)
    return data, im

def Efft2(ax:plt.Axes, filename:str, dir:str = 'MS/FLD/', f=None, *args, **kwargspassthrough):
    """Plot K(x1) by K(x2) at a given time using FFT.\n
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')
    f: function to apply beforehand (e.g. lambda x : x**2)
    args: additional function parameters if necessary
    kwargspassthrough: additional graphing parameters\n
    returns -> data read from file as H5Data object, imshow image"""

    e_ = filename[0:2]
    data = osh5io.read_h5(dir + e_ + '/' + filename)
    if f != None:
        data = f(data, *args)
    ax.grid()
    im = osh5vis.osplot(np.abs(osh5utils.fft2(data)), ax=ax, **kwargspassthrough)
    return data, im

def find_stripe(filename:str, dir:str = 'MS/FLD/', xzoom:tuple=(0.4, 1.6), yzoom:tuple=(-0.75, 0.75)):
    """ Find stripes of maximum values on the fft2 graphs within a zoomed window.
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')\n
    xzoom: x-axis limits of zoomed window (default (0.4, 1.6))\n
    yzoom: y-axis limits of zoomed window (default (-0.75, 0.75))\n
    returns -> x coordinates, y coordinates, title
    """
    e_ = filename[0:2]
    data = osh5io.read_h5(dir + e_ + '/' + filename)
    dataFFT = np.abs(osh5utils.fft2(data))
    x = dataFFT.axes[1].ax
    y = dataFFT.axes[0].ax

    xlim = (np.argmax(x>=xzoom[0]), np.argmax(x>=xzoom[1]))
    ylim = (np.argmax(y>=yzoom[0]), np.argmax(y>=yzoom[1]))
    
    dataFFT_zoomed = dataFFT[ylim[0]:ylim[1],xlim[0]:xlim[1]]
    x2 = dataFFT_zoomed.axes[1].ax
    y2 = dataFFT_zoomed.axes[0].ax
    maxs =  np.expand_dims(np.argmax(dataFFT_zoomed, axis=0), axis=0)[0]
    return x2, y2[maxs], osh5vis.default_title(dataFFT)

def stripe(ax:plt.Axes, filename:str, dir:str = 'MS/FLD/', xzoom:tuple=(0.4, 1.6), yzoom:tuple=(-0.75, 0.75), **kwargpassthrough):
    """ Plots stripes of maximum values on the fft2 graphs.
    ax: axes to plot on
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')
    xzoom: x-axis limits of zoomed window (default (0.4, 1.6))
    yzoom: y-axis limits of zoomed window (default (-0.75, 0.75))
    """
    x, y, _= find_stripe(filename, dir, xzoom, yzoom)
    ax.scatter(x, y, **kwargpassthrough)

def stripe_angle(ax, filename:str, dir:str = 'MS/FLD/', xzoom:tuple=(0.4, 1.6), yzoom:tuple=(-0.75, 0.75), convert2degrees=False, **kwargpassthrough):
    """Plot θ vs |κ| for the stripes on the fft2 graphs
    ax: axes to plot on
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')
    xzoom: x-axis limits of zoomed window (default (0.4, 1.6))
    yzoom: y-axis limits of zoomed window (default (-0.75, 0.75))\n
    """
    x, y, title = find_stripe(filename, dir, xzoom, yzoom)
    om = np.sqrt(np.square(x) + np.square(y))
    theta = np.arctan2(y,x)
    ax.set(xlabel=r'$\left| k \right|$ [$c^{-1}\omega_p$]', ylabel=r'$\theta$ [rad]', title=title)
    if convert2degrees:
        ax.set_ylabel(r'$\theta$ [degrees]')
        theta = np.rad2deg(theta)
    ax.scatter(om, theta, **kwargpassthrough)
    ax.grid()
    return om, theta

def stripe_angle_theo(ax:plt.Axes, k:np.ndarray, N:float, a:float=np.pi/6, convert2degrees=False, **kwargpassthrough):
    """Plots theoretical θ vs |κ|

    ax: axes to plot on
    k: array of wavenumbers (e.g. np.linspace(0.5,1.5))
    N: relative plasma density (e.g. 0.3)
    a: prism halfangle (default pi/6)
    convert2degrees: whether to convert to degrees (default False)
    kwargpassthrough: additional plotting parameters

    returns -> k, θ"""

    def refr_index(omega:np.ndarray, N:float) -> np.ndarray:
        """For a given laser frequency omega [measured in omega_p]
        and relative plasma density N, returns refractive index
        in that plasma

        sqrt(1-N*omega^-2)"""
        return np.sqrt(1-N*np.power(omega, -2))

    n0 = np.sqrt(1-N)
    n = refr_index(k, N)
    b = n0*np.sin(a)

    theta = 2*a - np.arcsin(b) - np.arcsin(n*np.sin(2*a-np.arcsin(b/n)))

    if convert2degrees:
        theta = theta*180/np.pi

    ax.plot(k, theta, **kwargpassthrough)
    return k, theta

def cm_alpha(colormap:str):
    # get colormap
    ncolors = 256
    color_array = plt.get_cmap(colormap)(range(ncolors))

    # change alpha values
    color_array[:,-1] = np.linspace(0.9,0.0,ncolors)

    # create a colormap object
    map_object = LinearSegmentedColormap.from_list(name=colormap+'_alpha',colors=color_array)
    map_object.set_over('black', alpha=0.0)
    # register this new colormap with matplotlib
    plt.register_cmap(cmap=map_object)

def movie(dir:str, fps:int=15, res:int=1, out_name:str='out.mp4', overlay:bool=False, figsize:tuple=None, f=None, **kwargspassthrough):
    """generate animation showing E(x) over time (1D data)\n
    dir: diagnostics folder to plot (e.g. MS/FLD/e2/)
    fps: frames per second of generated video
    res: plot every __ file (default: 1)\n
    out_name: output filename (default: E.mp4)
    overlay: overlay plasma distribution (default: False)
    figsize: dimensions of movie
    f: function to apply to data
    kwargspassthrough: additional graphing parameters"""

    fnms = os.listdir(dir)
    fnms.sort()
    fnms = fnms[::res] # get every res-th file from directory

    
    if overlay:
        ps_fnms = []
        ps_fnms = os.listdir('MS/PHA/x2x1/electrons/')
        ps_fnms.sort()
        cm_alpha('autumn')

    data = osh5io.read_h5(fnms[0], dir)

    oneD = len(data.shape) == 1

    if oneD:
        x1_limits = [data.run_attrs.get('XMIN'), data.run_attrs.get('XMAX')]
    else:
        x1_limits = [data.run_attrs.get('XMIN')[0], data.run_attrs.get('XMAX')[0]]
        x2_limits = [data.run_attrs.get('XMIN')[1], data.run_attrs.get('XMAX')[1]]

    fig = plt.figure(dpi=300, figsize=figsize, constrained_layout=True)
    if oneD:
        ax = plt.axes(xlim=x1_limits)
    else:
        ax = plt.axes(xlim=x1_limits, ylim=x2_limits)
    ax.grid()

    im = osh5vis.osplot(data, **kwargspassthrough)[0]

    # initialization function: plot the background of each frame
    def init():
        print('init()')
        if oneD:
            return im,

        else:
            if overlay:
                for f in ps_fnms:
                    x(ax, f, colorbar=False, cmap='autumn_alpha', alpha=0.2);
            return [im]

    # animation function.  This is called sequentially
    def animate(i):
        if i%100==0:
            print('X')
        elif i%10==0:
            print('X', end=' ')
        else:
            print('X', end='')

        if oneD:
            filename = fnms[i]
            data = osh5io.read_h5(filename, dir)
            if f != None:
                data = f(data)
            im.set_data(data.axes[0].ax,data.view(np.ndarray))
            ax.set(title=osh5vis.default_title(data), xlim=[data.run_attrs.get('XMIN')[0], data.run_attrs.get('XMAX')[0]])
            #ax.set_xlim(left=data.run_attrs.get('XMIN')[0], right=data.run_attrs.get('XMAX')[0])
            return im,
        else:
            filename = fnms[i]
            data = osh5io.read_h5(filename, dir)
            if f != None:
                data = f(data)
            im.set_data(data.view(np.ndarray))
            im.set_extent([data.run_attrs.get('XMIN')[0], data.run_attrs.get('XMAX')[0],x2_limits[0], x2_limits[1]])
            ax.set_title(osh5vis.default_title(data))
            ax.set_xlim(left=data.run_attrs.get('XMIN')[0], right=data.run_attrs.get('XMAX')[0])
            #if overlay:
               # x(ax, ps_fnms[i], colorbar=False, cmap='autumn_alpha', alpha=0.2);
            return [im]

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=len(fnms), blit=True)

    anim.save('VIS/' + out_name, fps=fps, extra_args=['-vcodec', 'libx264'])
    print()


def wigner(ax:plt.Axes, filename:str, dir:str = 'MS/FLD/', **kwargspassthrough):
    """Plot Wigner-Ville transform of E(x) at a given time.\n
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')\n
    kwargspassthrough: additional graphing parameters\n
    returns -> data read from file as H5Data object, imshow image"""

    e_ = filename[0:2]
    data = osh5io.read_h5(dir + e_ + '/' + filename)

    ts = np.linspace(data.run_attrs.get('XMIN'), data.run_attrs.get('XMAX'), int(data.run_attrs.get('NX')))
    wig = WVD(data.view(np.ndarray), timestamps=ts)
    wig.run(True)
    wig.plot(ax=ax, show=False, cmap='turbo', **kwargspassthrough)
    ax.set(xlabel=r'$%s$ $[%s]$' % (data.axes[0].attrs.get('LONG_NAME'), data.axes[0].attrs.get('UNITS')),
            ylabel=r'Frequency [$\omega_p$]')
    
#ax.set_xlim(left=data.run_attrs.get('XMIN')[0], right=data.run_attrs.get('XMAX')[0])

def spectogram(ax:plt.Axes, filename:str, dir:str = 'MS/FLD/', **kwargspassthrough):
    """Plot spectogram of E(x) at a given time.\n
    filename: (e.g. 'e2-000035.h5')
    dir: directory to plot from (default 'MS/FLD/')\n
    kwargspassthrough: additional graphing parameters\n
    returns -> data read from file as H5Data object, imshow image"""

    e_ = filename[0:2]
    data = osh5io.read_h5(dir + e_ + '/' + filename)

    ts = np.linspace(data.run_attrs.get('XMIN'), data.run_attrs.get('XMAX'), int(data.run_attrs.get('NX')))
    spec = Spectrogram(data.view(np.ndarray))
    spec.run()
    im = spec.plot(ax=ax, show=False, cmap='turbo', **kwargspassthrough)

def wigner_movie(dir:str, fps:int=20, res:int=1, out_name:str='wigner out.mp4', figsize:tuple=None, **kwargspassthrough):
    """generate animation showing Wigner transform over time (1D data)\n
    dir: diagnostics folder to plot (e.g. MS/FLD/e2/)
    fps: frames per second of generated video
    res: plot every __ file (default: 1)\n
    out_name: output filename (default: E.mp4)
    figsize: dimensions of movie
    kwargspassthrough: additional graphing parameters"""

    fig = plt.figure(dpi=300, figsize=figsize, constrained_layout=True)
    ax = plt.axes(xlim=[0,100])

    fnms = os.listdir(dir)
    fnms.sort()
    fnms = fnms[::res] # get every res-th file from directory

    data = osh5io.read_h5(fnms[0], dir)
    ts = np.linspace(data.run_attrs.get('XMIN'), data.run_attrs.get('XMAX'), int(data.run_attrs.get('NX')))
    wig = WVD(data.view(np.ndarray), timestamps=ts)
    a, _, _ = wig.run(True)
    wig.plot(ax=ax, show=False, default_annotation=False, cmap='turbo', **kwargspassthrough)
    ax.set(xlabel=r'$%s$ $[%s]$' % (data.axes[0].attrs.get('LONG_NAME'), data.axes[0].attrs.get('UNITS')),
            ylabel=r'Frequency [$\omega_p$]',
            title="WIGNER-VILLE " + osh5vis.time_format(data.run_attrs['TIME'][0], data.run_attrs['TIME UNITS']))
    ax.set_xlim(left=data.run_attrs.get('XMIN')[0], right=data.run_attrs.get('XMAX')[0])
    ax.grid()

    im = ax.get_images()[0]

    # initialization function: plot the background of each frame
    def init():
        im.set_data(a)
        return [im]

    # animation function.  This is called sequentially
    def animate(i):
        filename = fnms[i]
        new_data = osh5io.read_h5(filename, dir)
        new_ts = np.linspace(new_data.run_attrs.get('XMIN'), new_data.run_attrs.get('XMAX'), int(new_data.run_attrs.get('NX')))
        new_wig = WVD(new_data.view(np.ndarray), timestamps=new_ts)
        a, _, _ = new_wig.run(True)
        new_wig.plot(ax=ax, show=False, default_annotation=False, cmap='turbo', **kwargspassthrough)
        im.set_data(a)
        #ax.set(xlabel=r'$%s$ $[%s]$' % (data.axes[0].attrs.get('LONG_NAME'), data.axes[0].attrs.get('UNITS')),
            #ylabel=r'Frequency [$\omega_p$]')
        ax.set_title("WIGNER-VILLE " + osh5vis.time_format(new_data.run_attrs['TIME'][0], new_data.run_attrs['TIME UNITS']))
        ax.set_xlim(left=new_data.run_attrs.get('XMIN')[0], right=new_data.run_attrs.get('XMAX')[0])
        return [im]

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=len(fnms), blit=True)

    anim.save(out_name, fps=fps, extra_args=['-vcodec', 'libx264'])

def fft2_movie(dir:str, fps:int=15, res:int=1, out_name:str='out.mp4', figsize:tuple=None, **kwargspassthrough):
    """generate animation showing E(x) over time (1D data)\n
    dir: diagnostics folder to plot (e.g. MS/FLD/e2/)
    fps: frames per second of generated video
    res: plot every __ file (default: 1)\n
    out_name: output filename (default: E.mp4)
    overlay: overlay plasma distribution (default: False)
    figsize: dimensions of movie
    kwargspassthrough: additional graphing parameters"""

    fnms = os.listdir(dir)
    fnms.sort()
    fnms = fnms[::res] # get every res-th file from directory

    data = osh5io.read_h5(fnms[0], dir)
    data_fft = np.abs(osh5utils.fft2(data))
    fig = plt.figure(dpi=300, figsize=figsize, constrained_layout=True)
    ax = plt.axes()#xlim=x1_limits)
    ax.grid()

    im = osh5vis.osplot(data_fft, **kwargspassthrough)[0]

    # animation function.  This is called sequentially
    def animate(i):
        if i%100==0:
            print('X')
        elif i%10==0:
            print('X', end=' ')
        else:
            print('X', end='')

        filename = fnms[i]
        data = osh5io.read_h5(filename, dir)
        data_fft = np.abs(osh5utils.fft2(data))
        im.set_data(data_fft.view(np.ndarray))
        #im.set_extent([data.run_attrs.get('XMIN')[0], data.run_attrs.get('XMAX')[0],x2_limits[0], x2_limits[1]])
        ax.set_title(osh5vis.default_title(data))
        #ax.set_xlim(left=data.run_attrs.get('XMIN')[0], right=data.run_attrs.get('XMAX')[0])
        return [im]

    anim = animation.FuncAnimation(fig, animate,
                                frames=len(fnms), blit=True)

    anim.save('VIS/' + out_name, fps=fps, extra_args=['-vcodec', 'libx264'])
    print()