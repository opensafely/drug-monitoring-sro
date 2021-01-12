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
codes_af = codelist(['G573.',
                     'G5730',
                     'G5731',
                     'G573z',
                     'X202R',
                     'X202S',
                     'Xa2E8',
                     'Xa7nI',
                     'XaEga',
                     'XaOfa',
                     'XaOft',
                     'XaaUH',
                     'XaeUP',
                     'XaeUQ',
                     'XaeUR'], system="ctv3")

# tests

codes_inr = codelist(["42QE."], system="ctv3")

codes_renal_function_test = codelist(["451..",
                                      "44J3.",
                                      "44J3z",
                                      "4I37.",
                                      "X771Q",
                                      "X80D7",
                                      "XE26a",
                                      "XE2q5",
                                      "XaERX",
                                      "XaERc",
                                      "XaETQ",
                                      "XacUK"], system="ctv3")

