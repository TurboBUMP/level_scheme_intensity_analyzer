#!/bin/bash

for dir in $(ls spectra); do
  for file in $(ls spectra/$dir | grep .out.txt); do
    rm spectra/${dir}/${file}
  done
done
