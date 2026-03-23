import pandas as pd
import numpy as np

from functions import LoadLevelScheme

lvl_scheme = LoadLevelScheme('intensities44Ca.ods')
multiplets=set()

with open('doublet.txt','w') as file:
    for ii in range(lvl_scheme.shape[0]):
        g1 = lvl_scheme['Egamma-LITERATURE'].iloc[ii]
        for jj in range(lvl_scheme.shape[0]):
            g2 = lvl_scheme['Egamma-LITERATURE'].iloc[jj]
            if ii!=jj:
                if (abs(g1-g2)<2):
                    multiplets.add(lvl_scheme['Egamma-LITERATURE'].iloc[jj])

    for elem in sorted(multiplets):
        print(elem,file=file)
