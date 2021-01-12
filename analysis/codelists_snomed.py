# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:21:20 2020

@author: hcurtis
"""

from cohortextractor import (
    codelist,
    codelist_from_csv,
)


## medication codes


codes_warfarin = codelist_from_csv(
    "codelists/opensafely-warfarin.csv", system="snomed", column="id",
)

codes_doac = codelist_from_csv(
    "codelists/opensafely-direct-acting-oral-anticoagulants-doac.csv", system="snomed", column="id",
)

## diagnoses
codes_af = codelist(['120041000119109',
                     '15964901000119107',
                     '195080001',
                     '233910005',
                     '233911009',
                     '282825002',
                     '300996004',
                     '314208002',
                     '425615007',
                     '426749004',
                     '427665004',
                     '440028005',
                     '440059007',
                     '49436004',
                     '5370000',
                     ], system="snomed")

# tests

codes_inr = codelist(["165581004"], system="snomed")

codes_renal_function_test = codelist(["1000731000000107",
                                      "1000981000000109",
                                      "1000991000000106",
                                      "1001011000000107",
                                      "1010391000000109",
                                      "1011481000000105",
                                      "1015971000000100",
                                      "1032061000000108",
                                      "113075003","15373003","168154007","275792000"], system="snomed")

