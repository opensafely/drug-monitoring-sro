## LIBRARIES

# cohort extractor
from cohortextractor import (StudyDefinition, patients, codelist_from_csv, codelist)

##CODE LIST


systolic_blood_pressure_codes = codelist(["2469."], system="ctv3")
diastolic_blood_pressure_codes = codelist(["246A."], system="ctv3")
creatinine_codes = codelist(["XE2q5"], system="ctv3")
weight_codes = codelist(["22A.."], system="ctv3")

doac_codes = codelist_from_csv("codelists/opensafely-direct-acting-oral-anticoagulants-doac.csv", system="snomed",column="id") 


## STUDY POPULATION
study = StudyDefinition(

    # define default dummy data behaviour
    # Configure the expectations framework
    default_expectations = {
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "exponential_increase",
        "incidence": 0.5,
        "float": {"distribution": "normal", "mean": 80, "stddev": 10}},
 
   
    # define the study index date
    index_date = "2020-01-01",

    # define the study population
    population = patients.all(),

    # define the study variables

    age = patients.age_as_of("2020-02-01",
                             return_expectations={"rate" : "universal", "int" : {"distribution" : "population_ages"}}),
   
    ## systolic blood pressure
   
    bp_sys = patients.mean_recorded_value(systolic_blood_pressure_codes,
                                        on_most_recent_day_of_measurement=True,
                                        between=["2017-02-01", "2020-01-31"],
                                        include_measurement_date=False,
                                        return_expectations={"float": {"distribution": "normal", "mean": 120, "stddev": 10},
                                                             "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                             "incidence": 0.95,}),
    
    bp_dys = patients.mean_recorded_value(diastolic_blood_pressure_codes, 
                                          on_most_recent_day_of_measurement=True,
                                          between=["2017-02-01", "2020-01-31"],
                                          include_measurement_date=False,
                                          return_expectations={"float": {"distribution": "normal", "mean": 80 , "stddev": 10},
                                                             "date": {"earliest": "2019-02-01", "latest": "2020-01-31"},
                                                             "incidence": 0.95}), 
    
    baseline_creatinine = patients.with_these_clinical_events(creatinine_codes, 
                                                              between = ["index_date - 1 year", "index_date"], 
                                                              returning = "numeric_value",
                                                              date_format = "YYYY-MM-DD",
                                                              include_date_of_match=True,
                                                              find_last_match_in_period = True, 
                                                              return_expectations = {
                                                                  "float": {"distribution": "normal","mean":100, "stddev": 20},
                                                                  "date": {"earliest": "1980-02-01",
                                                                           "latest": "2020-01-31"}}),
    
    weight = patients.with_these_clinical_events(weight_codes, 
                                                 between = ["index_date - 1 year", "index_date"], 
                                                              returning = "numeric_value",
                                                 date_format = "YYYY-MM-DD",
                                                 include_date_of_match=True,
                                                 find_last_match_in_period = True,
                                                 return_expectations = {
                                                     "incidence": 0.95,
                                                     "float": {"distribution": "normal","mean":100, "stddev": 20},
                                                     "date": {"earliest": "1980-02-01",
                                                              "latest": "2020-01-31"}}),
    
    # DOAC prescribed in the 12 months before the index date 
    doac_before_index = patients.with_these_medications(doac_codes, 
                                                  return_expectations={"incidence": 0.5},  
                                                  between= ["index_date - 12 months", "index_date - 1 day"], 
                                                  returning='binary_flag'),
    
    
    #find if patient has been prescribed doac in the 3 months from index date 
    doac_after_index = patients.with_these_medications(doac_codes,
                                           between= ["index_date", "index_date + 3 months"],
                                           date_format = "YYYY-MM-DD", 
                                           include_date_of_match = True, 
                                           find_first_match_in_period = True,
                                           returning= "binary_flag",
                                           return_expectations = {"incidence": 0.25,
                                                                  "date": {"earliest": "1980-02-01",
                                                                           "latest": "2020-01-31"}}),
    # Patients who have died 
    died = patients.satisfying("""dead_ONS OR dead_GP""",
                               dead_ONS = patients.died_from_any_cause(
                                   on_or_before = "index_date", 
                                   returning="binary_flag"),
                               dead_GP = patients.with_death_recorded_in_primary_care(
                                   on_or_before="index_date", 
                                   returning="binary_flag"),
                               return_expectations={"incidence": 0.1,
                                                    "date": {"earliest": "1980-02-01",
                                                             "latest": "2020-01-31"}}),
    
    #next creatinine test 
     next_creatinine = patients.with_these_clinical_events(creatinine_codes, 
                                                              between = ["index_date", "today"], 
                                                              returning = "numeric_value",
                                                              date_format = "YYYY-MM-DD",
                                                              include_date_of_match=True,
                                                              find_first_match_in_period = True, 
                                                              return_expectations = {
                                                                  "float": {"distribution": "normal","mean":100, "stddev": 20},
                                                                  "date": {"earliest": "1980-02-01",
                                                                           "latest": "2020-01-31"}}),

    sex=patients.sex(
    return_expectations={
        "rate": "universal",
        "category": {"ratios": {"M": 0.49, "F": 0.51}}}),
                                                            

    )
   
