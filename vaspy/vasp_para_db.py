#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Golabel  Variables Descriptions (Most Frequently Used INCAR Parameters)
===============================================================================
  Attribute                 Description
  ======================    ===================================================
  COMMSIGN                  comment sign in INCAR file
  PARAFORMAT                format of parameter in INCAR
  INCAR_PARAMETERS          a dictionary of INCAR parameters
  INCAR_PARACATEGORIES      different groups of INCAR parameters
  BUILTIN_PARASETS          built-in parameter groups for quick-generation 
  ======================    ===================================================
"""

COMMSIGN = '#'

PARAFORMAT = "  {:<12s}  =  {:<24s}  {:<s}\n"

INCAR_PARAMETERS = {
        # paraname   defaultvalue paracomm
        # GENERAL
        "SYSTEM"        :  ["example"      , (),
            "system name"],
        "NWRITE"        :  ["2"            , (0, 1, 2, 3, 4),
            "verbosity flag, 0|1|*2|3|4"],
        "ISTART"        :  ["0"            , (0, 1),
            "0 New | 1 Restart"],
        "ICHARG"        :  ["2"            , (0, 1, 2, 4),
            "0 orbital | 1 CHGCAR | *2 superposition | 4 POT"],
        # parallel
        "NPAR"          :  ["6"            , (),
                "NCORE=ncores/NPAR"],
        "NCORE"         :  ["8"            , (),
                "cores/orbital, Better use NPAR"],
        # MAGNETIC
        "ISPIN"         :  ["2"            , (1, 2),
            "*1 no | 2 yes"],
        "MAGMOM"        :  [" "            , (),
            "array, spin per atom"],
        # WAVEFUNC
        "INIWAV"        :  ["1"            , (0, 1),
            "0 jellium | *1 random"],
        # CHARGE
        # Writing
        "LCHARG"        :  [".FALSE."      , (".TRUE.", ".FALSE."),
            "if write CHGCAR"],
        "LWAVE"         :  [".FALSE."      , (".TRUE.", ".FALSE."),
            "if write WAVECAR"],
        # ELECTRONIC
        "ENCUT"         :  ["450"          , (),
            "energy cutoff"],
        "PREC"          :  ["Accurate"     ,
                ("Low", "Medium", "High", "Normal", "Accurate", "Single"),
            "precision"],
        "EDIFF"         :  ["1.0E-5"       , (),
            "stopping criterion for electronic updates"],
        "NELM"          :  ["300"          , (),
            "maximium number of ionic updates"],
        "NELMIN"        :  ["6"            , (),
            "minimium number of ionic updates"],
        # dipole correction
        "IDIPOL"        :  ["3"            , (),
            "surface 3"],
        # hole/electron
        "NELECT"        :  ["0"            , (),
            "number of electrons"],
        # IONIC
        "EDIFFG"        :  ["-0.05"        , (),
            "stopping criterion for ionic updates"],
        "NSW"           :  ["1000"         , (),  
            "number of steps for ionic updates"],
        "IBRION"        :  ["2"            , (0,1,2,3,5),
            "0 MD | 1 quasi-Newton | 2 CG | 3 damped-MD | 5 FC"],
        "ISIF"          :  ["2"       , (0, 1, 2, 3, 4, 5, 6),
            "0 MD | *2 | 3 lat opt"],
        "POTIM"         :  ["0.2"          , (),
            "ionic step size / MD time step"],
        # Molecular Dynamics
        "TEBEG"         :  ["300"          , (),
            "begin temperature"],
        "TEEND"         :  ["300"          , (),
            "end temperature"],
        "SMASS"         :  ["3"            , (-3, -2, -1, 0, 3),
            "controls velocities in MD, -3 | -2 | -1 | >=0 Nosé"],
        "NBLOCK"        :  ["10"           , (),
            "update XDATCAR every NBLOCK fs"],
        # Advanced Molecualr Dynamics
        "MDALGO"        :  ["21"           , (0, 1, 2, 3, 11, 21, 13),
            "0 standard MD | 21 meta Nose-Hoover"],
        "LBLUEOUT"      :  [".FALSE."      , (".TRUE.", ".FALSE."),
                "print out free-energy gradient"],
        # US
        "HILLS_BIN"     :  ["15000"        , (),
                "bias potential update interval"],
        # slow-grownth
        "INCREM"        :  ["0"            , (),
                "increment in slow-grownth algo"],
        # Smearing
        "ISMEAR"        :  ["0"            , (-5, 0, 1),
            "-5 DOS | 0 large cell | 1 metal"],
        "SIGMA"         :  ["0.05"         , (),
            "smearing parameter"],
        # ALGO
        "ALGO"          :  ["Fast"         , ("ALL", "Normal", "Fast", "Very Fast"),
                "algorithms for electronic self-consistent"],
        "IALGO"         :  ["48"           , (),
                "8 CG | 48 RMM-DIIS"],
        "LREAL"         :  ["Auto"         , ("Auto", ".TRUE.", ".FALSE."),
                "if calculation done in real spcae"],
        "ISYM"          :  ["2"            , (0, 1, 2, 3),
                "0 off | 1 on | 2 charge | 3 no charge"],
        "NSIM"          :  ["4"            , (),
                "blocked band update"],
        # ALGO-Mixing
        "IMIX"          :  ["4"            , (),
                "0 no mix | 1 Kerker | 2 Tchebycheff | 4 Broyden2"],
        "AMIX"          :  ["0.4"          , (),
                "linear mixing parameter"],
        "AMIN"
        "BMIX"          :  ["1.0"          , (),
                "cutoff wave vector for Kerker mixing scheme"],
        "AMIX_MAG"      :  ["1.6"          , (),
                "linear mixing parameter for magnetization"],
        "BMIX_MAG"      :  ["1.0"          , (),
                ""],
        "WC"            :  ["1000"             , (),
                "weight factor in each step in Broyden"],
        "INIMIX"        :  ["1"            , (),
                "initial mixing in Broyden"],
        "MIXPRE"        :  ["1"            , (),
                "preconditioning in Broyden"],
        "MAXMIX"        :  ["-45"          , (),
                "maximum number steps stored in Broyden mixer"],
        # BAND
        "LORBIT"        :  ["11"           , (),
                "PAW radii for projected DOS"],
        "NEDOS"         :  ["2001"         , (),
                "DOSCAR points"],
        # vdW
        "IVDW"          :  ["11"           , (),
                "DFT-D3 without BJ damping"],
        "VDW_s6"        :  ["1.0"          , (),
                "s6-scaling parameter (kept fix at 1.0)"],
        "VDW_s8"        :  ["0.7875"       , (),
                "s8 for PBE"],
        "VDW_a1"        :  ["0.4289"       , (),
                "a1 damping parameter for PBE"],
        "VDW_a2"        :  ["4.4407"       , (),
                "a2 damping parameter for PBE"],
        # DFT+U(J)
        "LDAU"          :  [".TRUE."       , (".TRUE.", ".FALSE."),
                "Enable DFTU calculation"],
        "LDAUTYPE"      :  ["2"            , (1, 2, 4),
                "1 Liechtenstein | *2 Dudarev | 4"], 
        "LDAUL"         :  [""             , (),
                "-1 off | 1 p | 2 d | 3 f"],
        "LDAUU"         :  [""             , (),
                "coulomb interaction"],
        "LDAUJ"         :  [""             , (),
                "exchange interaction"],
        "LDAUPRINT"     :  ["2"            , (0, 1, 2),
                "*0 silent | 1 occupancy | 2 idem"],
        "LMAXMIX"       :  ["4"            , (2, 4, 6), 
                "twice the max l-quantum number"],
        # Hybrid Functional
        "LHFCALC"       :  [".TRUE."       , (),
                "Enable HF calculation"],
        "AEXX"          :  ["0.25"         , (),
                "Hartree-Fock percentage"],
        "PREFOCK"       :  ["Accurate"     , (),
                ""],
        "LMAXFOCK"      :  ["4"            , (4, 6),
                "4 s/p | 6 f"],
        "HFSCREEN"      :  ["0.2"          , (),
                "HSE06"],
        "TIME"          :  ["0.4"          , (),
                ""],
        # POTCAR related
        "POMASS"        :  [""             , (),
                "mass each atomic species in a.u."],
        "ZVAL"          :  [""             , (),
                "valence for each atomic species"],
        "RWIGS"         :  [""             , (),
                "Wigner-Seitz radius"],
        }

INCAR_PARACATEGORIES = {
        # catname paranames
        "GENERAL"   :  ["SYSTEM", "NWRITE", "ISTART"],
        "WRITING"   :  ["LCHARG", "LWAVE"],
        "PARALLEL"  :  ["NPAR"],
        "WAVEFUNC"  :  ["INIWAV"],
        "MAGNETIC"  :  ["ISPIN"],
        "ELECTRONIC":  ["ENCUT", "PREC", "EDIFF", "NELM", "NELMIN"],
        "IONIC"     :  ["EDIFFG", "NSW", "IBRION", "ISIF", "POTIM"],
        "MD"        :  ["TEBEG", "TEEND", "SMASS", "NBLOCK"],
        "SMEARING"  :  ["ISMEAR", "SIGMA"],
        "VDW"       :  ["IVDW"],
        "VDWBJ"     :  ["IVDW", "VDW_s6", "VDW_s8", "VDW_a1", "VDW_a2"],
        "ALGO"      :  ["ALGO", "LREAL", "ISYM"],
        "UJ"        :  ["LDAU", "LDAUTYPE", "LDAUL", "LDAUU", "LDAUJ", "LDAUPRINT", "LMAXMIX"],
        "HF"        :  ["LHFCALC", "AEXX", "PREFOCK", "LMAXFOCK", "HFSCREEN", "TIME"],
        }

BASIC_PARAS = ["GENERAL", "WRITING", "PARALLEL", "ELECTRONIC", "MAGNETIC", \
                "SMEARING", "ALGO", "IONIC"]
BUILTIN_PARASETS = {
        # task           paras          specail settings
        'SC'       :    [BASIC_PARAS    , 
            []],
        'MD'       :    [["MD"]         , 
            [('IBRION', 0), ('ISIF', 0), ('POTIM', 1.0), ('NSW', 15000), 
             ('PREC', 'Normal'), ('EDIFFG', -0.01), 
             ('ALGO', 'Very Fast'), ('ISYM', 0), 
             ('NELM', '120')]],
        'BAND'     :    [["BAND"]       , []],
        'VDW'      :    [["VDW"]        , []],
        'VDWBJ'    :    [["VDWBJ"]      , []],
        'UJ'       :    [["UJ"]         , []],
        'HF'       :    [["HF"]         , 
            [('ISYM', 3), ('ALGO', 'ALL')]],
        }

