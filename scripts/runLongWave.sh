#!/bin/bash 

source /usr/local/anaconda2/bin/activate /scripts/radiacao/anaconda/env-radiacao 
python /scripts/radiacao/longWaveModel/scripts/rodaLongWave.py
source /usr/local/anaconda2/bin/deactivate
