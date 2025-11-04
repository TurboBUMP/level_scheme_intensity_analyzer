#!/bin/zsh

# This program creates a unified output.txt file containing all the output.txt file contained in every /spectra subidrectory.
# If option -r | --redo-all-fit is passed then, the program will call ./sauron.py for all the gammarays of the spectra.
# Use -j N to specify the number of parallel process to use 
#

REWRITE_OUTPUT=0

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

      REWRITE_OUTPUT=1

      break
      ;;

    -sf|--single-folder)

      if [ -d spectra/"$2" ]; then
        ./sauron.py $2
        REWRITE_OUTPUT=1
      else
        echo "${2} is not a valid directory --> Exit"
        break 
        exit
      fi

      break
      ;;

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
      echo "Usage: ./replay.sh [OPTION]"
      echo "Example: ./replay.sh -r"
      echo "Example 2: ./replay.sh -s 1157.0208"
      echo "\n"
      echo "-h | --help                 print this help message"
      echo "-sf|--single-folder         replay.sh will recalculate the fit calling sauron.py on all the spectra of the specified sub-folder"
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
