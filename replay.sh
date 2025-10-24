#!/bin/zsh

export N=4

for dir in $(ls spectra/); do
  ((i = i % N))
  ((i++ == 0)) && wait
  ./sauron.py $dir &
done
