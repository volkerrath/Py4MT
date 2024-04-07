#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 07:29:58 2013

@author: Alison Kirkby

plots phase tensor ellipses as a map for a given frequency
"""

import mtpy.imaging.phase_tensor_maps as pptmaps
import os
import os.path as op

# change to your path to mtpy installation to ensure correct version is used
os.chdir(r'C:\mtpywin\mtpy')


# directory containing edis
edipath = r'C:\mtpywin\mtpy\examples\data\edi2'

# whether or not to save the figure to file
save = False

# full path to file to save to
savepath = r'C:/tmp'

# frequency to plot
plot_freq = 1e-2

# value to color ellipses by, options are phimin,phimax,skew
colorby = 'skew'
ellipse_range = [-9, 9]

image_fn = 'phase_tensor_map%1is_' % (int(1. / plot_freq)) + colorby + '.png'

# gets edi file names as a list
elst = [op.join(edipath, f) for f in os.listdir(edipath) if f.endswith('.edi')]


m = pptmaps.PlotPhaseTensorMaps(fn_list=elst,
                                plot_freq=plot_freq,
                                fig_size=(6, 4),
                                ftol=.1,
                                xpad=0.02,
                                plot_tipper='yr',
                                edgecolor='k',
                                lw=0.5,
                                minorticks_on=False,
                                ellipse_colorby=colorby,
                                ellipse_range=ellipse_range,
                                ellipse_size=0.01,
                                arrow_head_width=0.002,
                                arrow_head_length=0.002,
                                #                                ellipse_cmap='mt_seg_bl2wh2rd'
                                station_dict={'id': (5, 7)}
                                )


if save:
    m.save_figure(op.join(savepath, image_fn),
                  fig_dpi=400)  # change to your preferred file resolution
