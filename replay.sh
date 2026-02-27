#!/bin/zsh

# This program creates a unified output.txt file containing all the output.txt file contained in every /spectra subidrectory.
# If option -r | --redo-all-fit is passed then, the program will call ./sauron.py for all the gammarays of the spectra.
# Use -j N to specify the number of parallel process to use 
#

REWRITE_OUTPUT=0
#
while :; do
  case "$1" in
    -c|--clear-all-output)
      echo "Clearing all output.txt file"
      for DIR in $(ls spectra); do
        if [ -d spectra/${DIR} ]; then
          for file in $(ls spectra/${DIR} | grep ".out.txt");do
            echo "deleting file ${DIR}/${file}"
            rm ~/Desktop/Mordor/spectra/${DIR}/${file}
          done
        fi
      done

      break
      exit
      ;;

    -h|--help)
      echo "\n"
      echo "-h | --help                 print this help message"
      echo "-c | --clear-all-output     replay.sh will delete all output files"
      echo "\n"
      exit
      ;;

    *)
      echo "Creating unified output file: output.txt ..."
      REWRITE_OUTPUT=1
      break
      ;;
  esac
  shift
done

if [ $REWRITE_OUTPUT -eq 1 ]; then
  if [ -f output.txt ]; then
    echo "--> output.txt already existing\n --> deleting old one\n"
    rm output.txt
  fi
  
  for DIR in $(ls spectra); do 
    if [ -d spectra/${DIR} ];then 
      for file in $(ls spectra/$DIR | grep ".out.txt"); do
        echo "writing ${DIR}/${file} to output.txt"
        cat ~/Desktop/Mordor/spectra/${DIR}/${file} | tee -a ./output.txt >> /dev/null
      done
    fi
  done;
fi

sed -e '2,${/Integral/d}' -i output.txt

wait
exit
