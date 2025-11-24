#!/bin/zsh

#./sauron.py 1157.0208 -g 4932.8 -p 1157.004 --param -0.1 10 1157 2 350
#./sauron.py 2283.119 --gate 3731 --peak 1126.078 --param -0.1 10 1126 2 1000
#./sauron.py 3357.29 -g 2037.9 -p 2200.1 --param -1 0 2200 2 100 -w 10
#./sauron.py 3661.527 -g 1141.1 -p 2504.39 --param -1 0 2504 2 100 -w 4
#./sauron.py 3661.527 -g 1839.7 -p 1777.973 --param -1 0 1778 2 100 -w 100
#./sauron.py 3676.092 -g 1825.9 -p 1017.5 --param -1 0 1017 2 2e6 --limit 7 5
#./sauron.py 3676.092 -g 519.7 -p 368.208 --param -1 0 368 2 1000 --limit 6 10 
#./sauron.py 3711.96 -g 1518.2 -p 2554.9 --param -1 0 2554 2 1000 -w 8
#./sauron.py 3711.96 -g 1577.4 -p 667.3 --param -1 0 667 2 1000 -w 8
#./sauron.py 3711.96 -g 202.1 -p 667.3 --param -1 0 667.3 1 1000 -w 15
#./sauron.py 3711.96 -g 202.1 -p 2554.9 --param -1 0 2554 1 1000 -w 4
#./sauron.py 3711.96 -g 2063.2 -p 2554.9 --param -1 0 2554 1 50 --limit 6 4
#./sauron.py 3711.96 -g 211.3 -p 667.3 --param -1 0 667 2 100 --limit 6 10
#./sauron.py 3711.96 -g 211.3 -p 404.26 --param -1 0 404 2 100 --limit 6 10
#./sauron.py 3711.96 -g 1836.6 -p 667.3 --param -1 0 667 1 1000 --limit 10 7
#./sauron.py 3711.96 -g 1836.6 -p 2554.9 --param -1 0 2554 1 1000 --limit 7 8
#./sauron.py 3711.96 -g 7418.8 -p 667.3 --param -1 0 667 2 100 --limit 10 10
#./sauron.py 3776.27 -g 1524.4 -p 1119.7 --param -1 0 1119 2 100 --limit 20 5
#./sauron.py 3676.092 -g 1420.2 -p 368.208 --param -1 0 368 1400 --limit 7 10
#./sauron.py 3776.27 -g 2896.7 -p 1119.7 --param -1 0 1119 2 100 --limit 20 5
#./sauron.py 3913.8 -g 1374.8 -p 869.47 --param -1 0 869 2 2000 --limit 10 5

# 2.0 version of previous commands
./sauron.py -d 1157.0208 -g 4932.8 -p 1157.004 --param 1157 2 350 -0.1 10 --limit 1135 1175
./sauron.py -d 2283.119 -g 3731 -p 1126.078 --param 1126 2 1000 -0.1 10 --limit 1120 1132
./sauron.py -d 3357.29 -g 2037.9 -p 2200.1 --param 2200 2 100 -0.1 1 --limit 2190 2210
./sauron.py -d 3661.527 -g 1141.1 -p 2504.39 --param 2504 2 100 -0.1 0 --limit 2500 2508
./sauron.py -d 3661.527 -g 1839.7 -p 1777.973 --param 1778 2 100 -0.1 0 --limit 1678 1878      
./sauron.py -d 3676.092 -g 1825.9 -p 1017.5 --param 1017 2 2e6 -0.1 0 --limit 1010 1022   
./sauron.py -d 3676.092 -g 1420.2 -p 368.208 --param 368 2 1400 -0.1 0 --limit 361 378   
./sauron.py -d 3676.092 -g 519.7 -p 368.208 --param 368 2 1000 -0.1 0 --limit 362 378  
./sauron.py -d 3711.96 -g 1518.2 -p 2554.9 --param 2554 2 1000 -0.1 0 --limit 2546 2562          
./sauron.py -d 3711.96 -g 1577.4 -p 667.3 --param 667 2 1000 -0.1 0 --limit 659 675            
./sauron.py -d 3711.96 -g 1588.7 -p 667.3 --param 667 3 3500 -0.1 0 --limit 661 677
./sauron.py -d 3711.96 -g 202.1 -p 667.3 --param 667.3 1 1000 -0.1 0 --limit 652 682          
./sauron.py -d 3711.96 -g 202.1 -p 2554.9 --param 2554 1 1000 -0.1 0 --limit 2550 2558           
./sauron.py -d 3711.96 -g 2063.2 -p 2554.9 --param 2554 1 50 -0.1 0 --limit 2548 2558     
./sauron.py -d 3711.96 -g 211.3 -p 667.3 --param 667 3 3500 -0.1 0 --limit 661 677      
./sauron.py -d 3711.96 -g 211.3 -p 404.26 --param 404 2 100 -0.1 0 --limit 398 414     
./sauron.py -d 3711.96 -g 1836.6 -p 667.3 --param 667 1 1000 -0.1 0 --limit 657 674    
./sauron.py -d 3711.96 -g 1836.6 -p 2554.9 --param 2554 1 1000 -0.1 0 --limit 2547 2562   
./sauron.py -d 3711.96 -g 2499 -p 2554.9 --param 2554 1 40 -0.1 0 --limit 2534 2574
./sauron.py -d 3711.96 -g 2957.6 -p 2554.9 --param 2554 1 40 -0.1 0 --limit 2534 2574
./sauron.py -d 3711.96 -g 3138.4 -p 667.3 --param 667 1 70 -0.1 0 --limit 645 686
./sauron.py -d 3711.96 -g 7418.8 -p 667.3 --param 667 2 100 -0.1 0 --limit 657 677    
./sauron.py -d 3776.27 -g 1524.4 -p 1119.7 --param 1119 2 100 -0.1 0 --limit 1099 1124   
./sauron.py -d 3776.27 -g 1816.3 -p 475.2 --param 475 1 100 -0.1 0 --limit 455 494
./sauron.py -d 3776.27 -g 2896.7 -p 1119.7 --param 1119 2 100 -0.1 0 --limit 1099 1124   
./sauron.py -d 3913.8 -g 1374.8 -p 869.47 --param 869 2 2000 -0.1 0 --limit 859 874    
./sauron.py -d 3913.8 -g 2758.5 -p 202.1 --param 202 1 100 -0.1 0 --limit 198 205
./sauron.py -d 3913.8 -g 651.07 -p 202.1 --param 202 1 100 -0.1 0 --limit 198 205
./sauron.py -d 3913.8 -g 651.07 -p 1630.4 --param 1630 1 100 -0.1 0 --limit 1610 1640
./sauron.py -d 4196.1 -g 1353.1 -p 894.2 --param 894 1 200 0.1 0.1 --limit 889 910 
./sauron.py -d 4196.1 -g 1397.4 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 525
./sauron.py -d 4196.1 -g 1397.4 -p 1912.18 --param 1912 1 200 0.1 0.1 --limit 1910 1919
./sauron.py -d 4196.1 -g 1579.6 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 523
./sauron.py -d 4196.1 -g 1579.6 -p 4196.1 --param 4196 1 20 0.1 0.1 --limit 4193 4200
./sauron.py -d 4196.1 -g 2477.0 -p 894.2 --param 894 1 20 0.1 0.1 --limit 891 896
./sauron.py -d 4196.1 -g 2477.0 -p 519.7 --param 519 1 200 0.1 0.1 --limit 515 523
./sauron.py -d 4196.1 -g 6935.2 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 530
./sauron.py -d 4196.1 -g 6935.2 -p 483.4 --param 483 1 200 0.1 0.1 --limit 480 487
./sauron.py -d 4196.1 -g 900.8 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 521
./sauron.py -d 4315.22 -g 1418.1 -p 1007.7 --param 1007 1 600 0.1 0.1 --limit 1005 1013
./sauron.py -d 4358.44 -g 1142.9 -p 682.34 --param 682 1 100 0 1 --limit 677 685
./sauron.py -d 4358.44 -g 1416.7 -p 646.5 --param 646 1 100 0 1 --limit 640 650
./sauron.py -d 4358.44 -g 2313.6 -p 646.5 --param 646.5 1 100 0 1 --limit 634 655
./sauron.py -d 4399.2 -g 1335.0 -p 686.9 --param 687 1 100 1 0 --limit 680 690
./sauron.py -d 4399.2 -g 1335.0 -p 1091.1 --param 1091 2 350 -0.1 10 --limit 1082 1099
./sauron.py -d 4409.176 -g 1183.5 -p 747.63 --param 747 2 350 -0.1 10 --limit 727 755
./sauron.py -d 4409.176 -g 1183.5 -p 733.0 --param 733 2 350 -0.1 10 --limit 728 740
./sauron.py -d 4409.176 -g 1183.5 -p 1107.98 --param 1107 2 350 -0.1 10 --limit 1090 1113
