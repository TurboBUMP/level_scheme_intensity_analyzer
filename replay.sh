#!/bin/zsh

# This program creates a unified output.txt file containing all the output.txt file contained in every /spectra subidrectory.
# If option -r | --redo-all-fit is passed then, the program will call ./sauron.py for all the gammarays of the spectra.
# Use -j N to specify the number of parallel process to use 
#

while :; do
  case "$1" in
    -r|--redo-all-fit)

      case "$2" in 
        -j)
          if [[ "$3" =~ "^[0-9]+$" ]]; then
            echo "Recalculating all Fit with ${3} parallel sessions"
            for dir in $(ls spectra/); do
              ((i = i % "$3"))
              ((i++ == 0)) && wait
              ./sauron.py $dir &
            done
          fi
          break
          ;;
        *)
          echo "Wrong input parameters! Quitting ..."
          exit
          ;;
      esac


      break
      ;;
    -h|--help)
      echo "Usage: ./replay.sh [OPTION]"
      echo "Example: ./replay.sh -r"
      echo "\n"
      echo "-h | --help                 print this help message"
      echo "-r | --redo-all-fit         replay.sh will recalculate all the fit calling sauron.py (default -j 1)"
      echo "-j N                        if -r is specified use -j N to run sauron.py on N parallel processes"
      echo "\n"
      exit
      ;;

    *)
      echo "Creating unified output file: output.txt ..."
      break
      ;;
  esac
  shift
done

if [ -f output.txt ]; then
  echo "--> output.txt already existing\n --> deleting old one\n"
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


