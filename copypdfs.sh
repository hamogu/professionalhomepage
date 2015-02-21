#!/bin/bash
# to be run in base directory of homepage
mkdir pdfs/

# Copy papers where I (or Costa) are first author
cp ../../my_articles/HD163296_jet/jet.pdf pdfs/HD163296_jet.pdf
cp ../../my_articles/MNLup/MNLup.pdf pdfs/
cp ../../my_talks/12_CS17/proceedings/guenther_CS17.pdf pdfs/review_CS17.pdf
cp ../../my_proposals/applications/cv.pdf pdfs/
cp ../../my_articles/acc_model/acc_model7.pdf pdfs/acc_model.pdf
cp ../../my_articles/betaPic/betaPic.pdf pdfs/
cp ../../my_articles/Costa/UUSgeAAmain_normal.pdf pdfs/UUSge.pdf
cp ../../my_articles/costa_geom/15d_1.pdf pdfs/15d.pdf
cp ../../my_articles/DG_Tau_soft/dgtau6.pdf pdfs/dgtau.pdf
cp ../../my_articles/HD163296/HD163296_2.pdf pdfs/HD163296.pdf
cp ../../my_articles/IM_Lup/IM_Lup.pdf pdfs/
cp ../../my_articles/Iras20050/IRAS20050_emulateapj.pdf pdfs/IRAS20050.pdf
cp ../../my_articles/TW_Hya_lc/TW_Hya_lc2.pdf pdfs/CTTSlc.pdf
cp ../../my_articles/TW_Hya_uv_lineform/lineforms4.pdf pdfs/UVlines.pdf
cp ../../my_articles/V4046sgrletter/v4046_3.pdf pdfs/V4046Sgr.pdf
cp ../../my_talks/10_Bonn/proceedings/AGBonn_guenther.pdf pdfs/CTTS.pdf

# Copy talks and posters
cp ../../my_talks/10_Bonn/guenther.pdf pdfs/10_Bonn.pdf
cp ../../my_talks/10_Utrecht/Hetriplets_guenther.pdf pdfs/10_Utrecht.pdf
cp ../../my_talks/12_CS17/GuentherCS17.pdf pdfs/CS17.pdf
cp ../../my_talks/Accretion*disks*and*Coronae*/guenther.pdf pdfs/06_Bonn.pdf
cp ../../my_talks/CS14/Splinter_coronae_moira.pdf pdfs/CS14_splinter.pdf
cp ../../my_talks/X-rayuniverse2008/guenther.pdf pdfs/08_Granada.pdf

cp ../../my_poster/13_PPVI/poster_guenther.pdf pdfs/13_PPVI.pdf
cp ../../my_poster/11_AAS218_Boston/11_AAS218_guenther.pdf pdfs/11_AAS218_poster.pdf
cp ../../my_poster/12_Crete/guenther.pdf pdfs/12_Crete_poster.pdf
cp ../../my_poster/12_jets_NRAO/poster_guenther.pdf pdfs/12_NRAO_poster.pdf
cp ../../my_poster/Bonn06/Bonn06_1.pdf pdfs/06_Bonn_poster.pdf
cp ../../my_poster/CS14/CS14_mg_accretionmodel.pdf pdfs/CS14_poster.pdf
cp ../../my_poster/CS16/CS16_guenther.pdf pdfs/CS16_poster.pdf
cp ../../my_poster/IAUS243/IAUS243.pdf pdfs/IAUS243_poster.pdf
cp ../../my_poster/IAUS243/iaus243poster.pdf pdfs/IAUS243_proc.pdf
cp ../../my_poster/rodos2008/proceedings/guenther.pdf pdfs/08_rhodes_proc.pdf
cp ../../my_poster/rodos2008/poster1.pdf pdfs/08_rhodes_poster.pdf

# Copy Dimplomarbeit und Doktorarbeit
cp ../../my_articles/diplomarbeit/diplom.pdf pdfs/
cp ../../my_articles/phd/phd.pdf pdfs/

# copy work of students
cp ../../my_minions/M_Wilson.pdf pdfs/

# There is no need to keep a copy of all pdfs with the hompage itself.
# This script can be use to quickly remake that directory.

# TBD: For strict XHTML compatibility all tags should be in lower case letter. That is not the case where I copied things over from the old homepage. -> fix that!

cp -r * /data/wdocs/guenther/
rm /data/wdocs/guenther/copypdfs*
rm /data/wdocs/guenther/*~
rm /data/wdocs/guenther/images/front.xcf

rm -r pdfs/
