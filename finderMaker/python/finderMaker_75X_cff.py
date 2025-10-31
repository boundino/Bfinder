import FWCore.ParameterSet.Config as cms

# https://github.com/CMS-HIN-dilepton/cmssw/blob/Onia_AA_10_3_X/HiSkim/HiOnia2MuMu/python/onia2MuMuPAT_cff.py
# https://github.com/CMS-HIN-dilepton/cmssw/blob/Onia_AA_10_3_X/HiAnalysis/HiOnia/python/oniaTreeAnalyzer_cff.py
# https://github.com/CMS-HIN-dilepton/cmssw/blob/Onia_AA_10_3_X/HiAnalysis/HiOnia/test/hioniaanalyzer_PbPbPrompt_103X_DATA_cfg.py

def finderMaker_75X(process, runOnMC = True, VtxLabel = "hiSelectedVertex", TrkLabel = "hiGeneralTracks", TrkChi2Label = "packedPFCandidateTrackChi2", GenParticleLabel = "genParticles"):
        ### Set TransientTrackBuilder 
        process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
        process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
        process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")
        process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")

        ### Setup Pat
        process.load("PhysicsTools.PatAlgos.patSequences_cff")
        
        ## patMuonsWithTrigger
        process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
        from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import addMCinfo, useL1MatchingWindowForSinglets, changeTriggerProcessName, switchOffAmbiguityResolution, addHLTL1Passthrough, useL1Stage2Candidates

        if runOnMC:
                addMCinfo(process)
                process.muonMatch.maxDeltaR = cms.double(0.05)
                process.muonMatch.resolveByMatchQuality = True
                process.muonMatch.matched = "genMuons"
                process.muonMatch.src = "muons"

        changeTriggerProcessName(process, "HLT")
        switchOffAmbiguityResolution(process) # Switch off ambiguity resolution: allow multiple reco muons to match to the same trigger muon
        addHLTL1Passthrough(process)

        useL1Stage2Candidates(process)
        process.patTrigger.collections.append("hltGtStage2Digis:Muon") 
        process.muonMatchHLTL1.matchedCuts = cms.string('coll("hltGtStage2Digis:Muon")')
        process.muonMatchHLTL1.useMB2InOverlap = cms.bool(True)
        process.muonMatchHLTL1.useStage2L1 = cms.bool(True)
        process.muonMatchHLTL1.preselection = cms.string("")
        # process.muonL1Info.matched = cms.InputTag("gtStage2Digis:Muon:RECO")
        # process.muonL1Info.useStation2 = True

        if "hltIterL3MuonCandidatesPPOnAA" in process.patTrigger.collections:
                process.patTrigger.collections.remove("hltIterL3MuonCandidatesPPOnAA")
        process.patTrigger.collections.append("hltIterL3MuonCandidatesPPOnAA")
        if "hltL2MuonCandidatesPPOnAA" in process.patTrigger.collections:
                process.patTrigger.collections.remove("hltL2MuonCandidatesPPOnAA")
        process.patTrigger.collections.append("hltL2MuonCandidatesPPOnAA")
        process.muonMatchHLTL3.matchedCuts = cms.string('coll("hltIterL3MuonCandidatesPPOnAA")')
        process.muonMatchHLTL2.matchedCuts = cms.string('coll("hltL2MuonCandidatesPPOnAA")')

        from HLTrigger.Configuration.HLT_FULL_cff import fragment
        process.hltESPSteppingHelixPropagatorAlong = fragment.hltESPSteppingHelixPropagatorAlong
        process.hltESPSteppingHelixPropagatorOpposite = fragment.hltESPSteppingHelixPropagatorOpposite
        
        process.muonL1Info.maxDeltaR = 0.3
        process.muonL1Info.maxDeltaEta   = 0.2
        process.muonL1Info.fallbackToME1 = True
        process.muonL1Info.useStation2 = cms.bool(True)
        process.muonL1Info.cosmicPropagationHypothesis = cms.bool(False)
        process.muonL1Info.propagatorAlong = cms.ESInputTag('', 'hltESPSteppingHelixPropagatorAlong')
        process.muonL1Info.propagatorAny = cms.ESInputTag('', 'SteppingHelixPropagatorAny')
        process.muonL1Info.propagatorOpposite = cms.ESInputTag('', 'hltESPSteppingHelixPropagatorOpposite')
        process.muonMatchHLTL1.maxDeltaR = 0.3
        process.muonMatchHLTL1.maxDeltaEta   = 0.2
        process.muonMatchHLTL1.fallbackToME1 = True
        process.muonMatchHLTL1.useStation2 = cms.bool(True)
        process.muonMatchHLTL1.cosmicPropagationHypothesis = cms.bool(False)
        process.muonMatchHLTL1.propagatorAlong = cms.ESInputTag('', 'hltESPSteppingHelixPropagatorAlong')
        process.muonMatchHLTL1.propagatorAny = cms.ESInputTag('', 'SteppingHelixPropagatorAny')
        process.muonMatchHLTL1.propagatorOpposite = cms.ESInputTag('', 'hltESPSteppingHelixPropagatorOpposite')
        process.muonMatchHLTL2.maxDeltaR = 0.3
        process.muonMatchHLTL2.maxDPtRel = 10.0
        process.muonMatchHLTL3.maxDeltaR = 0.1
        process.muonMatchHLTL3.maxDPtRel = 10.0
        process.muonMatchHLTCtfTrack.maxDeltaR = 0.1
        process.muonMatchHLTCtfTrack.maxDPtRel = 10.0
        process.muonMatchHLTTrackMu.maxDeltaR = 0.1
        process.muonMatchHLTTrackMu.maxDPtRel = 10.0

        # Make a sequence
        process.patMuonSequence = cms.Sequence(process.patMuonsWithTriggerSequence)
        # if runOnMC:
        #         process.patMuonSequence.insert(0, process.genMuons)

        ### Set Bfinder option
        process.Bfinder = cms.EDAnalyzer('Bfinder',
                                         Bchannel = cms.vint32(
                                                 1,#RECONSTRUCTION: J/psi + K
                                                 0,#RECONSTRUCTION: J/psi + Pi
                                                 0,#RECONSTRUCTION: J/psi + Ks 
                                                 0,#RECONSTRUCTION: J/psi + K* (K+, Pi-)
                                                 0,#RECONSTRUCTION: J/psi + K* (K-, Pi+)
                                                 0,#RECONSTRUCTION: J/psi + phi
                                                 0,#RECONSTRUCTION: J/psi + pi pi <= psi', X(3872), Bs->J/psi f0
                                         ),
                                         detailMode = cms.bool(True),
                                         dropUnusedTracks = cms.bool(True),
                                         MuonTriggerMatchingPath = cms.vstring(""),
                                         MuonTriggerMatchingFilter = cms.vstring(""),
                                         HLTLabel = cms.InputTag('TriggerResults::HLT'),
                                         GenLabel = cms.InputTag(GenParticleLabel),
                                         MuonLabel = cms.InputTag('patMuonsWithTrigger'),
                                         TrackLabel = cms.InputTag(TrkLabel),
                                         TrackChi2Label = cms.InputTag(TrkChi2Label),
                                         TrackDedxLabel = cms.InputTag('dedxEstimator:dedxAllLikelihood'),
                                         BSLabel = cms.InputTag("offlineBeamSpot"),
                                         PVLabel = cms.InputTag(VtxLabel),
                                         tkPtCut = cms.double(1.0),#before fit
                                         tkEtaCut = cms.double(999.0),#before fit
                                         jpsiPtCut = cms.double(0.0),#before fit
                                         uj_VtxChiProbCut = cms.double(0.01),
                                         bPtCut = cms.vdouble(5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0),#before fit
                                         bEtaCut = cms.vdouble(2.4, 2.4, 2.4, 2.4, 2.4, 2.4, 2.4),#before fit, not used currently
                                         VtxChiProbCut = cms.vdouble(0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01),
                                         svpvDistanceCut = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                                         MaxDocaCut = cms.vdouble(999., 999., 999., 999., 999., 999., 999.),
                                         alphaCut = cms.vdouble(999., 999., 999., 999., 999., 999., 999.),
                                         doTkPreCut = cms.bool(True),
                                         doMuPreCut = cms.bool(True),
                                         makeBntuple = cms.bool(True),
                                         doBntupleSkim = cms.bool(False),
                                         printInfo = cms.bool(True),
                                         readDedx = cms.bool(True),
        )

        ### Set Dfinder option
        process.Dfinder = cms.EDAnalyzer('Dfinder',
                Dchannel                = cms.vint32(
                1,#RECONSTRUCTION: K+pi- : D0bar
                1,#RECONSTRUCTION: K-pi+ : D0
                0,#RECONSTRUCTION: K-pi+pi+ : D+
                0,#RECONSTRUCTION: K+pi-pi- : D-
                0,#RECONSTRUCTION: K-pi-pi+pi+ : D0
                0,#RECONSTRUCTION: K+pi+pi-pi- : D0bar
                0,#RECONSTRUCTION: K+K-(Phi)pi+ : Ds+
                0,#RECONSTRUCTION: K+K-(Phi)pi- : Ds-
                0,#RECONSTRUCTION: D0(K-pi+)pi+ : D+*
                0,#RECONSTRUCTION: D0bar(K+pi-)pi- : D-*
                0,#RECONSTRUCTION: D0(K-pi-pi+pi+)pi+ : D+*
                0,#RECONSTRUCTION: D0bar(K+pi+pi-pi-)pi- : D-*
                0,#RECONSTRUCTION: D0bar(K+pi+)pi+ : B+
                0,#RECONSTRUCTION: D0(K-pi+)pi- : B-
                0,#RECONSTRUCTION: p+k-pi+: lambdaC+
                0,#RECONSTRUCTION: p-k+pi-: lambdaCbar-
                0,#RECONSTRUCTION: pi+pi-(Kshort)p+ : lambdaC+
                0,#RECONSTRUCTION: pi+pi-(Kshort)p- : lambdaCbar-
        ),
        GenLabel = cms.InputTag(GenParticleLabel),
        # TrackLabel = cms.InputTag('patTrackCands'),
        TrackLabel = cms.InputTag(TrkLabel),
        TrackChi2Label = cms.InputTag(TrkChi2Label),
        TrackDedxLabel = cms.InputTag('dedxEstimator:dedxAllLikelihood'),
        BSLabel = cms.InputTag("offlineBeamSpot"),
        PVLabel = cms.InputTag(VtxLabel),
        tkPtCut = cms.double(0.), # before fit
        tkEtaCut = cms.double(10.0), # before fit
        dCutSeparating_PtVal = cms.vdouble(5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.),
        dPtCut = cms.vdouble(0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.), # before fit
        dRapidityCut = cms.vdouble(10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.),
        VtxChiProbCut = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        svpvDistanceCut_lowptD = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        svpvDistanceCut_highptD = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        alphaCut = cms.vdouble(999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999.),
        MaxDocaCut = cms.vdouble(999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999.),
        tktkRes_dCutSeparating_PtVal = cms.vdouble(0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.),
        tktkRes_dPtCut = cms.vdouble(0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.), # before fit
        tktkRes_VtxChiProbCut = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        tktkRes_svpvDistanceCut_lowptD = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        tktkRes_svpvDistanceCut_highptD = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        tktkRes_svpvDistanceToSVCut_lowptD = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        tktkRes_svpvDistanceToSVCut_highptD = cms.vdouble(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        tktkRes_alphaCut = cms.vdouble(999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999.),
        tktkRes_alphaToSVCut = cms.vdouble(999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999., 999.),
        ResToNonRes_PtAsym_max = cms.vdouble(1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.),
        ResToNonRes_PtAsym_min = cms.vdouble(-1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1.),
        readDedx = cms.bool(True),
        makeDntuple = cms.bool(True),
        doDntupleSkim = cms.bool(False),
        printInfo = cms.bool(True),
        dropUnusedTracks = cms.bool(True),
        )
        
        process.BfinderSequence = cms.Sequence(process.patMuonSequence*process.Bfinder)
        process.DfinderSequence = cms.Sequence(process.Dfinder)
        process.finderSequence = cms.Sequence(process.patMuonSequence*process.Bfinder*process.Dfinder)

        changeToMiniAODforMuon(process)

def setCutForAllChannelsDfinder(process, dPtCut = -1, dRapidityCut = -1, VtxChiProbCut = -1, svpvDistanceCut = -1, alphaCut = -1):
        for i in range(len(process.Dfinder.Dchannel)):
                if dPtCut >= 0:
                        process.Dfinder.dPtCut[i] = dPtCut
                if dRapidityCut >= 0:
                        process.Dfinder.dRapidityCut[i] = dRapidityCut
                if VtxChiProbCut >= 0:
                        process.Dfinder.VtxChiProbCut[i] = VtxChiProbCut
                if svpvDistanceCut >= 0:
                        process.Dfinder.svpvDistanceCut_lowptD[i] = svpvDistanceCut
                        process.Dfinder.svpvDistanceCut_highptD[i] = svpvDistanceCut
                if alphaCut >= 0:
                        process.Dfinder.alphaCut[i] = alphaCut

def changeToMiniAODforMuon(process, newtag = "unpackedMuons"):

    if hasattr(process, "patMuonsWithTrigger"):
        from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import useExistingPATMuons
        useExistingPATMuons(process, newPatMuonTag = cms.InputTag(newtag), addL1Info = False)
        # useExistingPATMuons(process, newPatMuonTag = cms.InputTag("slimmedMuons"), addL1Info = False)

        process.patTriggerFull = cms.EDProducer("PATTriggerObjectStandAloneUnpacker",
            patTriggerObjectsStandAlone = cms.InputTag('slimmedPatTrigger'),
            triggerResults              = cms.InputTag('TriggerResults::HLT'),
            unpackFilterLabels          = cms.bool(True)
        )

    # from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
    # process = MassReplaceInputTag(process, "offlinePrimaryVertices", "unpackedTracksAndVertices")
    # process = MassReplaceInputTag(process, "generalTracks", "unpackedTracksAndVertices")
