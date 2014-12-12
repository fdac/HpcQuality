# Plotting the data of file with points and non-continuous lines

set term postscript eps enhanced color 
set output "bb_parsec_ds.eps"

set size square .66

set title " Delta and Size per Commit - PARSEC"

#define axis
set style line 2 lc rgb '#000000' lt 1 lw 2   # ---black
set border  back ls 2

# set color and size of points and lines, and pointslinesinterval
#set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 pi -1 ps 1 #----blue
#set style line 1 lc rgb '#8a2be2' lt 1 lw 2 pt 7 pi -1 ps 1.5 #----blueviolet

#set style line 1 lc rgb '#ff0000' lt 1 lw 1.5 pt 7 pi -1 ps 1.5 #----red
#set pointintervalbox 2

# define grid
set style line 12 lc rgb '#7f7f7f' lt 0 lw 1 # -----gray
set grid back ls 12


set style line 3 lc rgb "#000000" lt 2 lw 2
set style line 4 lc rgb "#0060ad" lt 1 lw 2 pt 1
set style line 5 lc rgb "#8a2be2" lt 1 lw 2 pt 2
set style line 6 lc rgb "#000000" lt 1 lw 2 pt 3


####set pointsize 1
##set style fill transparent solid 0.2 noborder

# set position of title in the plotted image
set key top right  

set xlabel "Year"
set ylabel "Size/nTC"
set y2label "Delta/nTC"

#set logscal_Barrier y
#set logscal_Barrier x
set xtics ( "2009" 1, "2010" 2, "2011" 3, "2012" 4, "2013" 5, "2014" 6)
set ytics 50 
set xrange [0.5:6.5]
set yr [0:350]
set y2r[0:7]
set y2tics 1 

set key left bottom

overhead(x, y)=x/y
#error(x, dx, y, dy)=(x/y) * sqrt( (dx/x)**2.0 + (dy/y)**2.0 )

   plot "bb_parsec.txt" using 1:8 title "Size/nTC" with linespoints ls 4 axes x1y1,\
        "" using 1:9 title "Delta/nTC" with linespoints ls 6 axes x1y2


!epstopdf bb_parsec_ds.eps && rm bb_parsec_ds.eps