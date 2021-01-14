## cohort extractor
from cohortextractor import (
    StudyDefinition, 
    Measure,
    patients, 
    codelist_from_csv, 
    codelist
)

# import dictionary of measures
from measures_dict import measures_dict

# Import codelists
from codelists_tpp import *
from codelists_snomed import *

index_date="2020-01-01"

# Specifiy study defeinition

study = StudyDefinition(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "index_date", "latest": "index_date + 1 month"},
        "rate": "exponential_increase",},
            
    index_date = index_date,
    
    # This line defines the study population - patients with newly prescribed rivaroxaban 
    population=patients.satisfying(
        """(rivaroxaban_prescribed) AND
        (NOT rivaroxaban_prescribed_previously) AND 
        (NOT died) AND 
        (NOT died_during_follow_up_3m) AND
        (NOT died_during_follow_up_6m) AND
        (registered)
        """),

    # Important covariates 
    allpatients = patients.satisfying("""age>=0""", return_expectations={"incidence": 1}),
    
    # Rivaroxaban prescribed in the 12 months before the index date 
    rivaroxaban_prescribed_previously = patients.with_these_medications(rivaroxaban_codelist, 
                                                  return_expectations={"incidence": 0.5},  
                                                  between= ["index_date - 12 months", "index_date - 1 day"], 
                                                  returning='binary_flag'),
    
    # Rivaroxaban prescribed on or after the index date 
    rivaroxaban_prescribed = patients.with_these_medications(rivaroxaban_codelist, 
                                                             return_expectations = {"incidence": 0.5}, 
                                                             on_or_after = "index_date",
                                                             returning = "binary_flag", 
                                                             return_expectations={"incidence": 0.80}),
    
    # Date of rivaroxaban initiation
    rivaroxaban_initiation_date = patients.with_these_medications(rivaroxaban_codelist,
                                                                  on_or_after = ["index_date"],
                                                                  return_first_date_in_period = True, 
                                                                  returning = "date", 
                                                                  date_format = "YYYY-MM-DD", 
                                                                  return_expectations = {
                                                                      "date": {"earliest"; "index", "latest": "2020-02-29"}}),
                                                                    
    # Patients who have died 
    died = patients.satisfying("""dead_ONS OR dead_GP""",
                               dead_ONS = patients.died_from_any_cause(
                                   on_or_before = index_date,
                                   returning="binary_flag"),
                               dead_GP = patients.with_death_recorded_in_primary_care(
                                   on_or_before=index_date,
                                   returning="binary_flag"),
                               return_expectations={"incidence": 0.01}),
 
    
    # Died within 3 months of starting rivaroxaban 
    died_after_3_months_rivaroxaban = patients.satisfying("""dead_ONS OR dead_GP""",
                               dead_ONS = patients.died_from_any_cause(
                               between = ['rivaroxaban_initiation_date', 'rivaroxaban_initiation_date + 3 months'], 
                               returning="binary_flag"),
                               dead_GP = patients.with_death_recorded_in_primary_care(
                                   between = ['index_date + 1 day', 'today'],
                                   returning="binary_flag"),
                               return_expectations={"incidence": 0.01}),
    
    # Died within 6 months of starting rivaroxaban 
    died_after_6_months_rivaroxaban = patients.satisfying("""dead_ONS OR dead_GP""",
                               dead_ONS = patients.died_from_any_cause(
                               between = ['rivaroxaban_initiation_date', 'rivaroxaban_initiation_date + 6 months'], 
                               returning="binary_flag"),
                               dead_GP = patients.with_death_recorded_in_primary_care(
                                   between = ['index_date + 1 day', 'today'],
                                   returning="binary_flag"),
                               return_expectations={"incidence": 0.01}),
    
    
    # Registered at GP practice 
    registered = patients.registered_as_of(index_date,
                                           return_expectations={"incidence": 0.99}),
    
    # Age 
    age = patients.age_as_of("index_date",
                             return_expectations={"rate" : "universal",
                                                  "int" : {"distribution" : "population_ages"}}),
    
    # Baseline renal function 
    baseline_coded_crcl = patients.with_these_clinical_events(creatinine_clearance_codelist, 
                                                                 between = ["rivaroxaban_initiation_date - 3 months", "rivaroxaban_initiation_date - 1 day"],
                                                                 returning = "numeric_value",
                                                                 return_expectations = {"float": {"distribution": "normal", "mean": 100, "stddev": 20}}),
                                                                                        
    baseline_coded_crcl_yn = patients.with_these_clinical_events(creatinine_clearance_codelist, 
                                                                 between = ["rivaroxaban_initiation_date - 3 months", "rivaroxaban_initiation_date - 1 day"],
                                                                 returning = "binary_flag", 
                                                                 return_expectations={"incidence": 0.80}),
                                                              
                                                                                        
    baseline_creatinine = patients.with_these_clinical_events(creatinine_codelist, 
                                                              between = ["rivaroxaban_initiation_date - 3 months", "rivaroxaban_initiation_date - 1 day"], 
                                                              returning = "numeric_value", 
                                                              find_last_match_in_period = False, 
                                                              return_expectations = {"float": {"distribution": "normal", "mean": 100, "stddev": 20}}),
                                                                                        
    # Cockroft-Gault Creatinine Clearance 
    baseline_crcl_cockroft_gault = patients.cockroft_gault_crcl(between = ["index - 3 months", "rivaroxaban_initiation_date - 1 day"],
                                                               return_expectations = "float": {"distribution": "normal", "mean": 100, "stddev": 20}),                                                                                
                                                                                     
                            
    # CrCl Categorisation (<15, 15-30, 30-60, >60)
    crcl_categories = patients.categorised_as(
        {"<15": """baseline_crcl_cockroft_gault < 15""", 
         "15-30": """baseline_crcl_cockroft_gault >= 15 AND baseline_crcl_cockroft_gault < 30"""
         "30-60": """baseline_crcl_cockroft_gault >= 30 AND baseline_crcl_cockroft_gault < 60"""
         ">60": """baseline_crcl_cockroft_gault >=60"""},
        return_expectations={
            "rate":"universal",
            "category": {"ratios": {"<15": 0.1, "15-30": 0.2, "30-60": 0.2, ">60":0.5}}}),                                                                                    
                                                                                        
    # Patients who died during follow-up
    died_during_follow_up_3m = patients.satisfying(
        """baseline_crcl_cockroft_gault < 30 AND died_after_3_months_rivaroxaban""", 
        return_expectations={"incidence": 0.01}),
        
    died_during_follow_up_6m = patients.satisfying(
        """baseline_crcl_cockroft_gault < 60 AND baseline_crcl_cockroft_gault >= 30 AND died_after_6_months_rivaroxaban""", 
        return_expectations={"incidence": 0.01}),
     
    
    # For renal monitoring of DOACs there are 3 different strategies depending on baseline CrCl:  
    # Group 1 - require renal function to be checked in 3 months (CrCl < 30)
    # Group 2 - require renal function to be checked in 6 months (CrCl 30 - 60)
    # Group 3 - require renal function to be checked in 12 months (CrCl > 60)
                                                                                        
    # Required monitoring - this is the denominator for measures
    # This tests if there has been over three months elapsed since starting rivaroxaban - if this is the case, a test should have been carried out 
    group_1_required_monitoring = patients.satisfying(
        """baseline_crcl_cockroft_gault < 30 AND rivaroxaban_initiation_date <= DATEADD(m, -3, GETDATE())""",
        return_expectations={"incidence": 0.80}),
                                                            
    # This tests if there has been over six months elapsed since starting rivaroxaban - if this is the case, a test should have been carried out 
    group_2_required_monitoring = patients.satisfying(
        """baseline_crcl_cockroft_gault >= 30 AND baseline_crcl_cockroft_gault < 60 AND rivaroxaban_initiation_date <= DATEADD(m, -6, GETDATE())""",
        return_expectations={"incidence": 0.80}),
    
    # This tests if there has been over 12 months elapsed since starting rivaroxaban - if this is the case, a test should have been carried out 
    group_3_required_monitoring = patients.satisfying(
        """baseline_crcl_cockroft_gault >= 60 AND rivaroxaban_initiation_date <= DATEADD(m, -12, GETDATE())""",
        return_expectations={"incidence": 0.80}),
    
    # Pool together all the patients who required monitoring 
    required_monitoring = patients.satisfying(
    """group_1_required_monitoring OR group_2_required_monitoring OR group_3_required_monitoring""", 
        returning = "binary_flag",
        return_expectations={"incidence": 0.40}),
                                                   
    
    # Appropriate monitoring - this is the number of patients who should have monitoring done within a certain timeframe according to their baseline renal function 
    # This is the numerator for the measures metric 
    # Note window for any blood test is +/- 1 month 
    # This assumption is made as a test early on in the course of starting rivaroxaban may not be done to look for renal monitoring of DOAC - alternative indication may be more plausible 
    
    # This tests if a renal function test was done within 2 and 4 months for patients with CrCl < 30 
    group_1_appropriate_monitoring = patients.satisfying(
    """renal_function_test_3months AND baseline_crcl_cockroft_gault < 30""", 
    renal_function_test_3months = patients.with_these_clinical_events(
                creatinine_codes,
                between = ['rivaroxaban_initiation_date + 2 months', 'rivaroxaban_initiation_date + 4 months'],
                returning="binary_flag"), 
    return_expectations={"incidence": 0.5}), 
                                                                                        
    # This tests if a renal function test was done within 5 and 7 months for patients with CrCl between 30 - 60 
    group_2_appropriate_monitoring = patients.satisfying(
    """renal_function_test_6months AND baseline_crcl_cockroft_gault >=30 AND baseline_crcl_cockroft_gault < 60""", 
    renal_function_test_6months = patients.with_these_clinical_events(
                creatinine_codes,
                between = ['rivaroxaban_initiation_date + 5 months', 'rivaroxaban_initiation_date + 7 months'],
                returning="binary_flag"), 
    return_expectations={"incidence": 0.5}),                                                                                    
                                                                                        
    # This tests if a renal function test was done within 11 and 13 months for patients with CrCl > 60  
    group_3_appropriate_monitoring = patients.satisfying(
    """renal_function_test_12months AND  baseline_crcl_cockroft_gault >= 60""", 
    renal_function_test_12months = patients.with_these_clinical_events(
                creatinine_codes,
                between = ['rivaroxaban_initiation_date + 11 months', 'rivaroxaban_initiation_date + 13 months'],
                returning="binary_flag"), 
    return_expectations={"incidence": 0.5}),
                                                                                        
    # Pool the appropriate monitoring for all groups 
    appropriate_monitoring = patients.satisfying(
    """group_1_appropriate_monitoring OR group_2_appropriate_monitoring OR group_3_appropriate_monitoring""", 
        returning = "binary_flag",
        return_expectations={"incidence": 0.40})
)

# Measure function calculating the proportion of people with appropriate monitoring of renal function 
# if they were newly started rivaroxaban within the index dates provides
# Grouped by allpatients and by CrCl categories (<15, 15-30, 30-60, >60) 

measures = [
    Measure(
        id = "appropriate_renal_monitoring_of_rivaroxaban",
        numerator = "appropriate_monitoring",
        denominator = "required_monitoring",
        group_by = ['allpatients']
    ), 
    
    Measure(
        id = "appropriate_renal_monitoring_of_rivaroxaban",
        numerator = "appropriate_monitoring",
        denominator = "required_monitoring",
        group_by = ['crcl_categories'])
]