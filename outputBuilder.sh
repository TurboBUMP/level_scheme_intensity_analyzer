#!/bin/zsh

# This file is just a replica of the second part of ./replay.sh
# I need it just in case I want to resume all the oif [ -f output.txt ]
then
  echo "\n"
  echo "output.txt already existing --> deleting old one\n"
  rm output.txt
fi

for DIR in $(ls spectra); do 
if [ -d spectra/${DIR} ]
then 
  echo "writing ${DIR} to output.txt"
  cat ~/Desktop/Mordor/spectra/${DIR}/${DIR}.out.txt | tee -a ./output.txt >> /dev/null
fi
done;

sed -e '2,${/Integral/d}' -i output.txt
