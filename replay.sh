#!/bin/bash

# This program creates a unified output.txt file containing all the output.txt file contained in every /spectra subidrectory.
# If option -r | --redo-all-fit is passed then, the program will call ./sauron.py for all the gammarays of the spectra.
# Use -j N to specify the number of parallel process to use
#

REWRITE_OUTPUT=0

if [ -f output.txt ]; then
  echo "--> output.txt already existing\n --> deleting old one\n"
  rm output.txt
fi

for DIR in $(ls spectra); do
  if [ -d spectra/${DIR} ]; then
    for file in $(ls spectra/$DIR | grep ".out.txt"); do
      echo "writing ${DIR}/${file} to output.txt"
      cat ./spectra/${DIR}/${file} | tee -a ./output.txt >>/dev/null
    done
  fi
done

sed -e '2,${/Integral/d}' -i output.txt

wait
exit
