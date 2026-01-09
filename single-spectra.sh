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
sauron -d 1157.0208 -g 4932.8 -p 1157.004 --param 1157 2 350 -0.1 10 --limit 1135 1175
sauron -d 2283.119 -g 3731 -p 1126.078 --param 1126 2 1000 -0.1 10 --limit 1120 1132
sauron -d 3357.29 -g 2037.9 -p 2200.1 --param 2200 2 100 -0.1 1 --limit 2190 2210
sauron -d 3661.527 -g 1141.1 -p 2504.39 --param 2504 2 100 -0.1 0 --limit 2500 2508
sauron -d 3661.527 -g 1839.7 -p 1777.973 --param 1778 2 100 -0.1 0 --limit 1678 1878      
sauron -d 3676.092 -g 1825.9 -p 1017.5 --param 1017 2 2e6 -0.1 0 --limit 1010 1022   
sauron -d 3676.092 -g 1420.2 -p 368.208 --param 368 2 1400 -0.1 0 --limit 361 378   
sauron -d 3676.092 -g 519.7 -p 368.208 --param 368 2 1000 -0.1 0 --limit 362 378  
sauron -d 3711.96 -g 1518.2 -p 2554.9 --param 2554 2 1000 -0.1 0 --limit 2546 2562          
sauron -d 3711.96 -g 1577.4 -p 667.3 --param 667 2 1000 -0.1 0 --limit 659 675            
sauron -d 3711.96 -g 1588.7 -p 667.3 --param 667 3 3500 -0.1 0 --limit 661 677
sauron -d 3711.96 -g 202.1 -p 667.3 --param 667.3 1 1000 -0.1 0 --limit 652 682          
sauron -d 3711.96 -g 202.1 -p 2554.9 --param 2554 1 1000 -0.1 0 --limit 2550 2558           
sauron -d 3711.96 -g 2063.2 -p 2554.9 --param 2554 1 50 -0.1 0 --limit 2548 2558     
sauron -d 3711.96 -g 211.3 -p 667.3 --param 667 3 3500 -0.1 0 --limit 661 677      
sauron -d 3711.96 -g 211.3 -p 404.26 --param 404 2 100 -0.1 0 --limit 398 414     
sauron -d 3711.96 -g 1836.6 -p 667.3 --param 667 1 1000 -0.1 0 --limit 657 674    
sauron -d 3711.96 -g 1836.6 -p 2554.9 --param 2554 1 1000 -0.1 0 --limit 2547 2562   
sauron -d 3711.96 -g 2499 -p 2554.9 --param 2554 1 40 -0.1 0 --limit 2534 2574
sauron -d 3711.96 -g 2957.6 -p 2554.9 --param 2554 1 40 -0.1 0 --limit 2534 2574
sauron -d 3711.96 -g 3138.4 -p 667.3 --limit 655 687
sauron -d 3711.96 -g 7418.8 -p 667.3 --param 667 2 100 -0.1 0 --limit 657 677    
sauron -d 3776.27 -g 1524.4 -p 1119.7 --param 1119 2 100 -0.1 0 --limit 1099 1124   
sauron -d 3776.27 -g 1816.3 -p 475.2 --param 475 1 100 -0.1 0 --limit 455 494
sauron -d 3776.27 -g 2896.7 -p 1119.7 --param 1119 2 100 -0.1 0 --limit 1099 1124   
sauron -d 3913.8 -g 1374.8 -p 869.47 --param 869 2 2000 -0.1 0 --limit 859 874    
sauron -d 3913.8 -g 651.07 -p 202.1 --param 202 1 100 -0.1 0 --limit 198 205
sauron -d 3913.8 -g 651.07 -p 1630.4 --param 1630 1 100 -0.1 0 --limit 1610 1640
sauron -d 4196.1 -g 1353.1 -p 894.2 --param 894 1 200 0.1 0.1 --limit 889 910 
sauron -d 4196.1 -g 1397.4 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 525
sauron -d 4196.1 -g 1397.4 -p 1912.18 --param 1912 1 200 0.1 0.1 --limit 1910 1919
sauron -d 4196.1 -g 1579.6 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 523
sauron -d 4196.1 -g 1579.6 -p 4196.1 --param 4196 1 20 0.1 0.1 --limit 4193 4200
sauron -d 4196.1 -g 2477.0 -p 894.2 --param 894 1 20 0.1 0.1 --limit 891 896
sauron -d 4196.1 -g 2477.0 -p 519.7 --param 519 1 200 0.1 0.1 --limit 515 523
sauron -d 4196.1 -g 6935.2 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 530
sauron -d 4196.1 -g 6935.2 -p 483.4 --param 483 1 200 0.1 0.1 --limit 480 487
sauron -d 4196.1 -g 900.8 -p 519.7 --param 519 1 200 0.1 0.1 --limit 516 521
sauron -d 4315.22 -g 1418.1 -p 1007.7 --param 1007 1 600 0.1 0.1 --limit 1005 1013
sauron -d 4358.44 -g 1142.9 -p 682.34 --param 682 1 100 0 1 --limit 677 685
sauron -d 4358.44 -g 1416.7 -p 646.5 --param 646 1 100 0 1 --limit 640 650
sauron -d 4358.44 -g 2313.6 -p 646.5 --param 646.5 1 100 0 1 --limit 634 655
sauron -d 4399.2 -g 1335.0 -p 686.9 --param 687 1 100 1 0 --limit 680 690
sauron -d 4399.2 -g 1335.0 -p 1091.1 --param 1091 2 350 -0.1 10 --limit 1082 1099
sauron -d 4409.176 -g 1183.5 -p 747.63 --param 747 2 350 -0.1 10 --limit 727 755
sauron -d 4409.176 -g 1183.5 -p 733.0 --param 733 2 350 -0.1 10 --limit 728 740
sauron -d 4409.176 -g 1183.5 -p 1107.98 --param 1107 2 350 -0.1 10 --limit 1090 1113
sauron -d 4409.176 -g 1324.0 -p 747.63 --param 747 1 100 1 0 --limit 737 758
sauron -d 4409.176 -g 6721 -p 747.63 --param 747 1 100 1 0 --limit 739 752
sauron -d 4479.9 -g 6651.3 -p 703.4 --param 703 2 50 0 0 --limit 701 706
sauron -d 4584.08 -g 704.5 -p 1226.9 --param 1226.9 1 100 0 0 --limit 1224 1231
sauron -d 4650.3 -g 898.0 -p 1349.4 --param 1349 3 300 1 0 --limit 1340 1357
sauron -d 4650.3 -g 898.0 -p 989.0 --param 988 3 300 1 0 --limit 980 992
sauron -d 4650.3 -g 898.0 -p 874.3 --param 874 1 500 1 0 --limit 871 879
sauron -d 4650.3 -g 6480.2 -p 989.0 --param 989 1 500 1 0 --limit 978 1000
sauron -d 4803.6 -g 6328.3 -p 1141.1 --param 1141 2 500 1 0 --limit 1130 1150
sauron -d 4803.6 -g 972.6 -p 1494.6 --param 1494 3 100 1 0 --limit 1474 1499
sauron -d 4803.6 -g 972.6 -p 2145.52 --param 2145 3 100 1 0 --limit 2125 2147
sauron -d 4803.6 -g 972.6 -p 1141.1 --param 1141 3 100 1 0 --limit 1130 1150
sauron -d 4884.02 -g 1050.9 -p 1222.5 --para 1222 2 100 1 0 --limi 1218 1242
sauron -d 5096.87 -g 1753.1 -p 1173.9 --param 1174 2 150 1 0 --limit 1165 1180
sauron -d 5096.87 -g 476.8 -p 697.6 --limit 690 701
sauron -d 5096.87 -g 476.8 -p 532.1 --limit 528 538
sauron -d 5096.87 -g 678.6 -p 1173.9 --limit 1170 1179
sauron -d 5230.33 -g 545.3 -p 1922.4 --limit 1917 1926
sauron -d 5289.25 -g 444.5 -p 1196.7 --param 1197 3 2000 1 0 --limit 1194 1202
sauron -d 5289.25 -g 444.5 -p 1366.1 --param 1366 3 2000 1 0 --limit 1360 1370
sauron -d 5289.25 -g 444.5 -p 2244.2 --limit 2241 2264
sauron -d 5300.5 -g 1549.0 -p 4143.8 --param 4144 2 100 1 0 --limit 4139 4149
sauron -d 5573.9 -g 5557.7 -p 1649.9 --limit 1629 1655
sauron -d 5573.9 -g 5557.7 -p 2264.6 --limit 2259 2285
sauron -d 5573.9 -g 5557.7 -p 476.8 --limit 472 481
sauron -d 5775.76 -g 5355.7 -p 678.6 --limit 658 682
sauron -d 5775.76 -g 5355.7 -p 545.3 --limit 540 552
sauron -d 5775.76 -g 5355.7 -p 1606.6 --limit 1602 1612
sauron -d 5775.76 -g 5355.7 -p 1209.6 --limit 1203 1216
sauron -d 5783.15 -g 5348.1 -p 1867.4 --limit 1863 1872
sauron -d 4196.1 -g 900.8 -p 519.7 --param 518 1 50 0.1 1 --limit 515 521
sauron -d 4584.08 -g 645.7 -p 1276.0 --limit 1274 1280
sauron -d 4584.08 -g 2088.20 -p 1276.0 --limit 1256 1280
sauron -d 4584.08 -g 1191.2 -p 1276.0 --limit 1256 1280
sauron -d 6093.8 -g 5037.5 -p 4932.8 --limit 4920 4943
sauron -d 6093.8 -g 5037.5 -p 3048.3 --limit 3043 3052
sauron -d 5892.5 -g 5238.8 -p 1878.7 --param 1879 1 100 0 1 --limit 1873 1885
sauron -d 5096.87 -g 6034.4 -p 1788.5 --limit 1785 1810
sauron -d 5096.87 -g 476.8 -p 1788.5 --limit 1784 1800
sauron -d 5096.87 -g 6034.4 -p 532.1 --limit 520 552
sauron -d 5995.68 -g 5135.8 -p 1064.1 --limit 1044 1071
sauron -d 4930.74 -g 1064.1 -p 1016.9 --limit 1008 1036
sauron -d 4930.74 -g 6199.9 -p 1016.9 --limit 1008 1036
sauron -d 4930.74 -g 6199.9 -p 1218.8 --limit 1212 1228
sauron --primary -d 11131.6 -gd 0.0 -g 4408.91 -p 6721.0 --param 6721 1 50 0 1 --limit 6700 6740
sauron -d 4196.1 -g 1101.3 -p 1912.18 --limit 1908 1917
sauron -d 4196.1 -g 1353.1 -p 519.7 --limit 514 521
sauron -d 3922.71 -g 1419.3 -p 878.25 --limit 873 895
sauron -d 3922.71 -g 1419.3 -p 637.68 --limit 632 650
sauron -d 5342.2 -g 5789.5 -p 1419.3 --limit 1400 1423
sauron -d 5775.76 -g 5355.7 -p 1852.3 --limit 1832 1857
sauron -d 6981.69 -g 4149.7 -p 3057.9 --limit 3036 3064
sauron -d 3913.8 -g 3066.9 -p 1630.4 --limit 1612 1645
sauron -d 3913.8 -g 1428.0 -p 1630.4 --limit 1625 1650
sauron -d 3913.8 -g 1658.8 -p 1630.4 --limit 1625 1650
sauron -d 3913.8 -g 1016.9 -p 1630.4 --limit 1626 1650
sauron -d 3913.8 -g 2758.5 -p 202.1 --limit 194 204
sauron -d 3913.8 -g 7215.8 -p 869.47 --limit 849 875
sauron -d 3913.8 -g 7215.8 -p 628.71 --limit 608 635
sauron -d 3913.8 -g 2178.6 -p 605.8 --limit 595 615
sauron -d 3913.8 -g 1016.9 -p 556.8 --limit 546 566
sauron -d 3913.8 -g 3066.9 -p 556.8 --limit 546 566
sauron -d 5289.25 -g 5841.9 -p 1374.8 --limit 1370 1394
sauron -d 5733.3 -g 5397.8 -p 1819.3 --limit 1813 1839
sauron -d 5935.8 -g 5195.5 -p 2158.5 --limit 2155 2178
sauron -d 3711.96 -g 686.9 -p 667.3 --limit 655 687
sauron -d 3711.96 -g 2499.0 -p 667.3 --limit 654 687
sauron -d 3307.872 -g 1007.7 -p 651.353 --limit 642 671
sauron -d 3307.872 -g 2193.2 -p 651.353 --limit 631 660
sauron -d 4884.02 -g 6247.2 -p 1582.8 --limit 1579 1602
