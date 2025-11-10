To setup Bfinder
=====

2024 pp and PbPb data/MC and Rereco of 2023 UPC PbPb data/MC from MINIAOD
Ref: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiForestSetup

```
cmsrel CMSSW_14_1_9 #
cd CMSSW_14_1_9/src
cmsenv
git cms-merge-topic CmsHI:forest_CMSSW_14_1_X
scram b -j4
```

To add D/Bfinder to forest:
=====

```
cd $CMSSW_BASE/src
cmsenv
git clone -b Dfinder_14XX_miniAOD https://github.com/boundino/Bfinder.git --depth 1
source Bfinder/test/DnBfinder_to_Forest.sh
scram b -j4
cp HeavyIonsAnalysis/Configuration/test/forest_miniAOD_run3_DATA_wDfinder.py . # taking data as an example
```

To run:
=====

```
cmsRun forest_miniAOD_run3_DATA_wDfinder.py
```
