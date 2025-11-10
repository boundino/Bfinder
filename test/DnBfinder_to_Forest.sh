#!/bin/bash

PATHTOTEST=$CMSSW_BASE/src/HeavyIonsAnalysis/Configuration/test/
FORESTS=(forest_miniAOD_run3_DATA forest_miniAOD_run3_UPC_DATA forest_miniAOD_run3_MC)
RUNONMC=(False False True)
INFILES=(
    "/store/hidata/HIRun2024B/HIPhysicsRawPrime0/MINIAOD/PromptReco-v1/000/388/350/00000/60ad5c5a-8835-49c9-a031-77671c00b56e.root"
    "/store/hidata/HIRun2024B/HIForward0/MINIAOD/PromptReco-v2/000/388/468/00000/062e9301-3fac-495a-849c-fe6233892da1.root"
    "root://eoscms.cern.ch//store/group/phys_heavyions/jviinika/PythiaHydjetRun3_5p36TeV_dijet_ptHat15_100kEvents_miniAOD_2023_08_30/PythiaHydjetDijetRun3/PythiaHydjetRun3_dijet_ptHat15_5p36TeV_miniAOD/230830_165931/0000/pythiaHydjet_miniAOD_11.root"
)
MINIMUMTREES=0

cc=0
for FOREST in ${FORESTS[@]}
do
    ##
    cp ${PATHTOTEST}/${FOREST}.py ${PATHTOTEST}/${FOREST}_wDfinder.py

    echo '
#################### D finder #################
runOnMC = '${RUNONMC[cc]}'
VtxLabel = "offlineSlimmedPrimaryVertices"
TrkLabel = "packedPFCandidates"
TrkChi2Label = "packedPFCandidateTrackChi2"
GenLabel = "prunedGenParticles"
from Bfinder.finderMaker.finderMaker_75X_cff import finderMaker_75X,setCutForAllChannelsDfinder
finderMaker_75X(process, runOnMC, VtxLabel, TrkLabel, TrkChi2Label, GenLabel)
process.Dfinder.tkPtCut = cms.double(0.5) # before fit
process.Dfinder.tkEtaCut = cms.double(2.4) # before fit
process.Dfinder.Dchannel = cms.vint32(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
setCutForAllChannelsDfinder(process, dPtCut = 1, VtxChiProbCut = 0.05, svpvDistanceCut = 2.5, alphaCut = 999.)

process.dfinder = cms.Path(process.DfinderSequence)

' >> ${PATHTOTEST}/${FOREST}_wDfinder.py

    ##
    cp ${PATHTOTEST}/${FOREST}.py ${PATHTOTEST}/${FOREST}_wBfinder.py

    echo '
#################### B finder #################
runOnMC = '${RUNONMC[cc]}'
VtxLabel = "offlineSlimmedPrimaryVertices"
TrkLabel = "packedPFCandidates"
TrkChi2Label = "packedPFCandidateTrackChi2"
GenLabel = "prunedGenParticles"
from Bfinder.finderMaker.finderMaker_75X_cff import finderMaker_75X
finderMaker_75X(process, runOnMC, VtxLabel, TrkLabel, TrkChi2Label, GenLabel)
process.Bfinder.tkPtCut = cms.double(1.) # before fit
process.Bfinder.tkEtaCut = cms.double(2.4) # before fit
process.Bfinder.jpsiPtCut = cms.double(0.0) # before fit
process.Bfinder.bPtCut = cms.vdouble(3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 1.0) # before fit
process.Bfinder.Bchannel = cms.vint32(0, 0, 0, 0, 0, 0, 1)
process.Bfinder.VtxChiProbCut = cms.vdouble(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
process.Bfinder.svpvDistanceCut = cms.vdouble(2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0)
process.Bfinder.doTkPreCut = cms.bool(True)
process.Bfinder.doMuPreCut = cms.bool(True)
process.Bfinder.MuonTriggerMatchingPath = cms.vstring("")
process.Bfinder.MuonTriggerMatchingFilter = cms.vstring("")
process.BfinderSequence.insert(0, process.unpackedMuons)
process.BfinderSequence.insert(0, process.unpackedTracksAndVertices)
# process.unpackedMuons.muonSelectors = cms.vstring() # uncomment for pp

process.p = cms.Path(process.BfinderSequence)

#######################################################################################################################
# Muon filtering before running Bfinder to significantly speed up the processing
MUONCUT = "isTrackerMuon && ((abs(eta) <= 1.0 && pt > 3.4) || (1.0 < abs(eta) <= 2.4 && pt > 1.2)) && innerTrack.hitPattern.trackerLayersWithMeasurement > 5 && innerTrack.hitPattern.pixelLayersWithMeasurement > 0"
process.muonSelector = cms.EDFilter("PATMuonRefSelector",
                                    src = cms.InputTag("slimmedMuons"),
                                    cut = cms.string(MUONCUT),
                                    filter = cms.bool(True)
                                    )
process.atLeastTwoMuons = cms.EDFilter("MuonRefPatCount",
                                    src = cms.InputTag("slimmedMuons"),
                                    cut = cms.string(MUONCUT),
                                    minNumber = cms.uint32(2)
                                    )
# only process events containing at least one J/psi candidate
process.dimuonSelection = cms.EDProducer("CandViewShallowCloneCombiner",
                                    checkCharge = cms.bool(True),
                                    cut = cms.string("mass > 2.7 && mass < 3.4"),
                                    decay = cms.string("muonSelector@+ muonSelector@-")
                                    )

process.p.replace(process.BfinderSequence, process.muonSelector * process.atLeastTwoMuons * process.dimuonSelection * process.BfinderSequence)

' >> ${PATHTOTEST}/${FOREST}_wBfinder.py

    configfiles="${PATHTOTEST}/${FOREST}_wDfinder.py ${PATHTOTEST}/${FOREST}_wBfinder.py"
    #
    [[ $MINIMUMTREES -eq 1 ]] && {
        cp ${PATHTOTEST}/${FOREST}_wDfinder.py ${PATHTOTEST}/${FOREST}_onlyDfinder.py
        cp ${PATHTOTEST}/${FOREST}_wBfinder.py ${PATHTOTEST}/${FOREST}_onlyBfinder.py

        for ifile in ${PATHTOTEST}/${FOREST}_onlyBfinder.py ${PATHTOTEST}/${FOREST}_onlyDfinder.py
        do
            sed -i "/D\/B finder/i \\
process.ana_step = cms.Path( \\
    process.HiForest \\
    + \\
    process.particleFlowAnalyser \\
    ) \\
" $ifile
        done
        configfiles=$configfiles" ${PATHTOTEST}/${FOREST}_onlyDfinder.py ${PATHTOTEST}/${FOREST}_onlyBfinder.py"
    }

    #
    for ifile in $configfiles
    do
        echo '
###############################
import FWCore.ParameterSet.VarParsing as VarParsing
ivars = VarParsing.VarParsing('"'"'analysis'"'"')

ivars.maxEvents = -1
ivars.outputFile='"'"'HiForestMINIAOD.root'"'"'
ivars.inputFiles='"'${INFILES[cc]}'"'
ivars.parseArguments() # get and parse the command line arguments

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(ivars.inputFiles),
    # eventsToProcess = cms.untracked.VEventRange('"'"'1:236:29748033-1:236:29748033'"'"')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(ivars.maxEvents)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(ivars.outputFile))
' >> $ifile
    done
    ##
    cc=$((cc+1))
done
