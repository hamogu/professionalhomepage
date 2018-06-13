# -*- coding: utf-8 -*-
from __future__ import print_function
'''Compile professional homepage

This script compiles my professional homepage.
It uses Jinja2 templates. There is a general template in /templates
The individual files are made with template inheritance in the /src directory.
So far, no actual python code is required to fill values in the templates.
The navigation bar is defined in templates/basic.html and it is assumed that
the number of files in /src matches what is defined in basic.html.

This script needs to be executed in the exact directory where it is now,
because it copies pdfs from posters and talks and the path to all those
is given relative to the current directory.

Call as:

python homepage.py

The output will be written to the /html folder that can be removed later.
'''

from glob import glob
import os
import shutil

from jinja2 import Environment, FileSystemLoader

# Generate html
env = Environment(loader=FileSystemLoader('.'))

pagelist = glob('src/*html')
''' Not foolproof!
The navigation bar is defined in templates/basic.html
and I need to sync that with the content of the src directory by hand
'''

outpath = 'html'

if not os.path.exists(outpath):
    os.makedirs(outpath)

for page in pagelist:
    print("Working on {0}".format(page))
    template = env.get_template(page)
    with open(os.path.join(outpath, os.path.basename(page)), "w") as html_out:
        html_out.write(template.render())

# copy style sheet
shutil.copy('moritz.css', outpath)

# copy public PGP key
datapath = os.path.join(outpath, 'data')
if not os.path.exists(datapath):
    os.makedirs(datapath)
shutil.copy(os.path.join('data', 'hansmoritzguenther_public_key.asc'),
            datapath)

# copy images
impath = os.path.join(outpath, 'images')
if not os.path.exists(impath):
    os.makedirs(impath)

imlist = [glob(os.path.join('images', '*.{}'.format(ext)))
          for ext in ['gif', 'png', 'jpg', 'jpeg']]
imlist = [item for sublist in imlist for item in sublist]
for im in imlist:
    shutil.copy(im, impath)

# copy pdfs
pdfpath = os.path.join(outpath, 'pdfs')
if not os.path.exists(pdfpath):
    os.makedirs(pdfpath)

copyshell = '''
# Copy talks and posters
cp ../../my_talks/10_Bonn/guenther.pdf {0}/10_Bonn.pdf
cp ../../my_talks/10_Utrecht/Hetriplets_guenther.pdf {0}/10_Utrecht.pdf
cp ../../my_talks/12_CS17/GuentherCS17.pdf {0}/CS17.pdf
cp ../../my_talks/Accretion*disks*and*Coronae*/guenther.pdf {0}/06_Bonn.pdf
cp ../../my_talks/CS14/Splinter_coronae_moira.pdf {0}/CS14_splinter.pdf
cp ../../my_talks/X-rayuniverse2008/guenther.pdf {0}/08_Granada.pdf

cp ../../my_poster/13_PPVI/poster_guenther.pdf {0}/13_PPVI.pdf
cp ../../my_poster/11_AAS218_Boston/11_AAS218_guenther.pdf {0}/11_AAS218_poster.pdf
cp ../../my_poster/12_Crete/guenther.pdf {0}/12_Crete_poster.pdf
cp ../../my_poster/12_jets_NRAO/poster_guenther.pdf {0}/12_NRAO_poster.pdf
cp ../../my_poster/Bonn06/Bonn06_1.pdf {0}/06_Bonn_poster.pdf
cp ../../my_poster/CS14/CS14_mg_accretionmodel.pdf {0}/CS14_poster.pdf
cp ../../my_poster/CS16/CS16_guenther.pdf {0}/CS16_poster.pdf
cp ../../my_poster/IAUS243/IAUS243.pdf {0}/IAUS243_poster.pdf
cp ../../my_poster/IAUS243/iaus243poster.pdf {0}/IAUS243_proc.pdf
cp ../../my_poster/rodos2008/proceedings/guenther.pdf {0}/08_rhodes_proc.pdf
cp ../../my_poster/rodos2008/poster1.pdf {0}/08_rhodes_poster.pdf
cp ../../my_poster/14_AAS224_Boston/poster_guenther.pdf {0}/14_AAS224.pdf
cp ../../my_poster/14_cs18/poster_guenther.pdf {0}/14_CS18.pdf
cp ../../my_talks/14_AAS223/guenther_AAS223.pdf {0}/14_AAS223.pdf
cp ../../my_talks/14_Chandra/guenther_moritz.pdf {0}/14_Chandra.pdf
cp ../../my_talks/15_AAS225/guenther.pdf {0}/15_AAS225.pdf
cp ../../my_talks/15_HarvardHeidelberg/guenther_poster.pdf {0}/15_HarvardHeidelberg.pdf
cp ../../my_talks/15_ESTEC/GuentherHM.pdf {0}/15_ESTEC.pdf
cp ../../my_poster/16_SPIE/poster.pdf {0}/16_SPIE_poster.pdf
cp ../../my_poster/16_SPIE/article.pdf {0}/16_SPIE_article.pdf
cp ../../my_poster/18_SPIE_Arcus/poster.pdf {0}/18_SPIE_poster.pdf

# Copy Dimplomarbeit und Doktorarbeit
cp ../../my_articles/diplomarbeit/diplom.pdf {0}/
cp ../../my_articles/phd/phd.pdf {0}/

# copy work of students
cp ../../my_minions/M_Wilson.pdf {0}/

# copy cv and list of pub
cp ../../my_proposals/applications/cv.pdf {0}/
cp ../../my_proposals/applications/listofpub.pdf {0}/
'''.format(pdfpath)
for command in copyshell.split('\n'):
    os.system(command)

# copy pdfs
prespath = os.path.join(outpath, 'presentations')
if not os.path.exists(prespath):
    os.makedirs(prespath)

copyshell = '''
# Copy talks and posters
cp -r ../../my_talks/17_SPIE_ARCUS/talk-Arcus-SPIE17 {0}/ARCUS_SPIE17
cp -r ../../my_talks/17_SPIE_REDSoX/talk-REDSOX-SPIE17 {0}/REDSoX_SPIE17
cp -r ../../my_talks/18_SPIE_Lynx/talk-lynxXGS-SPIE18 {0}/Lynx_SPIE18
'''.format(prespath)
for command in copyshell.split('\n'):
    os.system(command)


# copy some content verbatim
# This is mostly interactive content that I e.g. link to from a poster
# with a URL or QR code.
# (That's why that directory is called qr)
# So, this directory might accumulate an unorganized collection of stuff.
# but in the interest of linking, I want to keep that URLs short
qrpath = os.path.join(outpath, 'qr')
if not os.path.exists(qrpath):
    os.makedirs(qrpath)

filelist = glob(os.path.join('qr', '*'))
for f in filelist:
    shutil.copy(f, qrpath)
