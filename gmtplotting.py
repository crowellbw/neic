#!/usr/bin/python
import math
import numpy
import os
from os.path import expanduser
home = expanduser("~")
###########################################################
###########################################################
gmtpath='/opt/gmt/gmt/bin'
def plottimeseries(fname,site,eventid,datafile,t,e,n,u):
        maxe = numpy.nanmax(e*100)
        mine = numpy.nanmin(e*100)
        maxn = numpy.nanmax(n*100)
        minn = numpy.nanmin(n*100)
        maxu = numpy.nanmax(u*100)
        minu = numpy.nanmin(u*100)
        maxt = numpy.nanmax(t)
        mint = numpy.nanmin(t)
        plotfile = home+'/plot_timeseries'
        f1 = open(plotfile,'w')
        f1.write('#!/bin/bash'+'\n')
        f1.write('export PATH='+gmtpath+':$PATH'+'\n')
        f1.write('  NAME='+fname+'\n')
        f1.write('rm $NAME'+'\n')
        f1.write('gmt set FONT_ANNOT_PRIMARY 16p,Helvetica,black'+'\n')
        f1.write('gmt set PS_PAGE_ORIENTATION landscape'+'\n')
        f1.write('gmt set PS_MEDIA A2'+'\n')
        f1.write('gmt set IO_NAN_RECORDS skip'+'\n')
        f1.write('gmt set MAP_TITLE_OFFSET 0.25c'+'\n')
        f1.write('gmt set FONT_LABEL 16p,Helvetica,black'+'\n')
        f1.write('gmt set FONT_TITLE 16p,Helvetica'+'\n')


        f1.write('psbasemap -R'+str(mint)+'/'+str(maxt)+'/'+str(mine)+'/'+str(maxe)+' -JX10i/3i -Bxafg+l"Time (s)" -Byafg+l"East (cm)" -BWeSn+t"'+site+', '+eventid+'" -Y13i -K > $NAME'+'\n')
        f1.write('awk \'{if ($3 != "nan") print $2, $3*100}\' '+ datafile + ' |psxy -W3 -R -J -O -K >> $NAME'+'\n')
        f1.write('awk \'{if ($3 == "nan") print $2, 0}\' '+ datafile + ' |psxy -Sx0.3 -Wred -R -J -O -K >> $NAME'+'\n')
        f1.write('awk \'{if ($3 != "nan") print $2, $4*100}\' '+ datafile + ' |psxy -W3 -R'+str(mint)+'/'+str(maxt)+'/'+str(minn)+'/'+str(maxn)+' -JX10i/3i -Bxafg+l"Time (s)" -Byafg+l"North (cm)" -BWeSn -O -K -Y-4.25i >> $NAME'+'\n')
        f1.write('awk \'{if ($3 == "nan") print $2, 0}\' '+ datafile + ' |psxy -Sx0.3 -Wred -R -J -O -K >> $NAME'+'\n')
        f1.write('awk \'{if ($3 != "nan") print $2, $5*100}\' '+ datafile + ' |psxy -W3 -R'+str(mint)+'/'+str(maxt)+'/'+str(minu)+'/'+str(maxu)+' -JX10i/3i -Bxafg+l"Time (s)" -Byafg+l"Up (cm)" -BWeSn -O -K -Y-4.25i >> $NAME'+'\n')
        f1.write('awk \'{if ($3 == "nan") print $2, 0}\' '+ datafile + ' |psxy -Sx0.3 -Wred -R -J -O >> $NAME'+'\n')
        f1.write('gmt psconvert $NAME -Tj -A -E450'+'\n')
        f1.write('exit 0'+'\n')
        f1.close()
        os.system('chmod 777' + ' ' + plotfile)
        os.system(plotfile)
        return

def plotpgd(fname,eventid,datafile,eqlon,eqlat,ti,dm,mag,stdmag):
        plotfile = home+'/plot_pgd'
        f1 = open(plotfile,'w')
        f1.write('#!/bin/bash'+'\n')
        f1.write('export PATH='+gmtpath+':$PATH'+'\n')
        f1.write('  NAME='+fname+'\n')
        f1.write('rm $NAME'+'\n')
        f1.write('gmt set FONT_ANNOT_PRIMARY 16p,Helvetica,black'+'\n')
        f1.write('gmt set PS_PAGE_ORIENTATION landscape'+'\n')
        f1.write('gmt set PS_MEDIA A2'+'\n')
        f1.write('gmt set MAP_TITLE_OFFSET 0.25c'+'\n')
        f1.write('gmt set FONT_LABEL 16p,Helvetica,black'+'\n')
        f1.write('gmt set FONT_TITLE 16p,Helvetica'+'\n')
        f1.write('gmt set MAP_FRAME_TYPE plain'+'\n')
        f1.write('gmt set FORMAT_GEO_OUT D'+'\n')
        f1.write('gmt set FORMAT_FLOAT_OUT %.5lg'+'\n')
        f1.write('makecpt -Cmmi -T5/9.5/0.5 -D > tmp.cpt'+'\n')
        f1.write('psbasemap -R1/500/0.5/500 -JX8il/8il -Ba1f3p:"Hypocentral Distance (km)":/a1f3p:"PGD (cm)"::."'+eventid+'":WeSn -Y5i -K > $NAME'+'\n')
        f1.write('awk \'{if ($1 != "#") print $4, $6, (log($6)/log(10)+6.687)/(1.5-0.214*log($4)/log(10))}\' '+ datafile + ' |psxy -R -J -O -K -Wblack -Sc0.25 -Ctmp.cpt >> $NAME'+'\n')
        #f1.write('awk \'{if ($1 != "#") print $4, $5, (log($5)/log(10)+6.687)/(1.5-0.214*log($4)/log(10))}\' '+ datafile + ' |psxy -R -J -O -K -Wblack -Ss0.25 -Ctmp.cpt >> $NAME'+'\n')
        f1.write('echo "1.2 1.0 14,1,black 0 LM M@-pgd@- = '+mag+' , @~s@~ = '+stdmag+'" | pstext -R -J -O -K -F+f+a+j >> $NAME'+'\n')
        f1.write('echo "1.2 0.8 14,1,black 0 LM windows: '+str(ti)+' s , '+str(dm)+' km" | pstext -R -J -O -K -F+f+a+j >> $NAME'+'\n')
        f1.write('echo "1.2 0.65 12,1,black 0 LM Regression lines from Crowell et al. [2016]" | pstext -R -J -O -K -F+f+a+j >> $NAME'+'\n')
        f1.write('echo "1.2 0.55 12,1,black 0 LM log(PGD)=-6.687+1.500*M-0.214*M*log(R)" | pstext -R -J -O -K -F+f+a+j >> $NAME'+'\n')
        f1.write('awk \'{print $1,$2}\' disp_eq_pgd_crowell.txt | psxy -Wblack -R -J -Sqd6c:+l\'Mw 9.0\'  -O -K >>  $NAME'+'\n')
        f1.write('awk \'{print $1,$3}\' disp_eq_pgd_crowell.txt | psxy -Wblack -R -J -Sqd6c:+l\'Mw 8.0\'  -O -K >>  $NAME'+'\n')
        f1.write('awk \'{print $1,$4}\' disp_eq_pgd_crowell.txt | psxy -Wblack -R -J -Sqd6c:+l\'Mw 7.0\'  -O -K >>  $NAME'+'\n')
        f1.write('awk \'{print $1,$5}\' disp_eq_pgd_crowell.txt | psxy -Wblack -R -J -Sqd6c:+l\'Mw 6.0\'  -O -K >>  $NAME'+'\n')
        #f1.write('awk \'{print $1,$2}\' critical_pgd.txt | psxy -W3,red -R -J  -O -K >>  $NAME'+'\n')        
        f1.write('pscoast -R'+str(eqlon-3)+'/'+str(eqlon+3)+'/'+str(eqlat-3)+'/'+str(eqlat+3)+' -JM6.5i -Bxaf -Byaf -BWeSn -O -K -Df -Na -Sblue -W -X9i >> $NAME'+'\n')
        f1.write('awk \'{if ($1 != "#") print $2, $3,(log($6)/log(10)+6.687)/(1.5-0.214*log($4)/log(10))}\' '+ datafile + ' |psxy -R -J -O -K -Wblack -Sc0.25 -Ctmp.cpt >> $NAME'+'\n')
        f1.write('echo "'+str(eqlon)+' '+str(eqlat)+'" | psxy -R -J -O -K -Sa0.5 -Wblack -Gred >> $NAME'+'\n')
        f1.write('psscale  -O -D3.25i/-0.5i/6.5i/0.5ih  -B1f0.25:"PGD Magnitude":/:: -Ctmp.cpt >> $NAME'+'\n')
        f1.write('exit 0'+'\n')
        f1.close()
        os.system('chmod 777' + ' ' + plotfile)
        os.system(plotfile)
        return
