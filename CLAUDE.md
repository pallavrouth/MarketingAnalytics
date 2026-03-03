# Project Setup

## On every session start, do the following automatically:

1. Run in terminal: python3 -m jupyter lab --port 8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.disable_check_xsrf=True
2. Run in terminal: mkdir -p analysis
3. Call setup_notebook(server_url="http://localhost:8888/lab", notebook_path="analysis/YYYYMMDD_session.ipynb")
4. List available .dta files in Data/ and ask the user which one to work with
5. Once confirmed, add and execute following in Cell 1:

import sys
sys.path.insert(0, '/Applications/Stata/utilities')
from pystata import config
config.init('se')
from pystata import stata
import os
print(os.getcwd())
import pandas as pd
import numpy as np
from plotnine import *

6. Add and execute following Cell 2:

stata.run('use "/full/path/to/Data/FILENAME.dta", clear', quietly=False, echo=True)
df = pd.read_stata('/full/path/to/Data/FILENAME.dta')

## Workflow
- All Stata work goes through PyStata using stata.run()
- Estimationing models and variable creation for estimating models use stata.run()
- Always use quietly=False, echo=True in every stata.run() call
- Everything else (exploration, summaries, plots, data manipulation) use pandas/numpy/plotnine
