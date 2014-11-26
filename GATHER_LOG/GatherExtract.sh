#!/bin/bash
#run on da VM
#ssh -p2204 da2.eecs.utk.edu
# righ now in this folder
#cd /home/audris/hpc

#below are the scripts used to get data/extract changes
#get openmpi
git clone --mirror https://github.com/open-mpi/ompi
github.com_open-mpi_ompi

#get lustre repos
cat lustre.list | while read i
do j=$(echo $i| sed 's"/"_"');
git clone --mirror http://git.whamcloud.com$i git.whamcloud.com$j
done

#Get clmagma/dplasma
for i in icl/clmagma bosilca/dplasma
do j=$(echo $i| sed 's"^/"";s"/"_"');
   hg clone -U https://audrism@bitbucket.org/i bitbucket.org_$j
done

#now extract delta (commit for each file)
for i in  icl/clmagma bosilca/dplasma
do j=$(echo $i| sed 's"^/"";s"/"_"')
   hg log -v --style ~/bin/multiline1 bitbucket.org_$j | gzip >
bitbucket.org_$j.log.gz
done
#hg log -v --style multiline1 | awk '{ print "'$REPLY';" $0}' |
i=github.com_open-mpi_ompi
git --git-dir=$i log --numstat -M -C --diff-filter=ACMR --full-history
--pretty=tformat:"STARTOFTHECOMMIT%n%H;%T;%P;%an;%ae;%at;%cn;%ce;%ct;%s"
| perl ~/bin/extrgit.perl | gzip > $i.delta.gz

cat lustre.list | while read i
do j=git.whamcloud.com$(echo $i| sed 's"/"_"');
k=$(echo $j| sed 's"/"_"g');
git --git-dir=$j log --numstat -M -C --diff-filter=ACMR --full-history
--pretty=tformat:"STARTOFTHECOMMIT%n%H;%T;%P;%an;%ae;%at;%cn;%ce;%ct;%s"
| perl ~/bin/extrgit.perl | gzip > $k.delta.gz
done &
