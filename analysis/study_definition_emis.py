
# Import functions

from cohortextractor import (
    StudyDefinition, 
    Measure,
    patients, 
    codelist, 
    codelist_from_csv
)

# import dictionary of measures
from measures_dict import measures_dict

# Import codelists
from codelists_snomed import *

index_date="2020-01-01"

# Specifiy study defeinition

study = StudyDefinition(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "index_date", "latest": "index_date + 1 month"},
        "rate": "exponential_increase",
    },
            
    index_date = index_date,
    
    # This line defines the study population
    population=patients.satisfying(
        """
        (sex = 'F' OR sex = 'M') AND
        (age >= 18 AND age < 120) AND
        (atrial_fibrillation) AND
        (NOT died) AND
        (registered)
        """
    ),

    # The rest of the lines define the covariates with associated GitHub issues
    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/33
    age=patients.age_as_of(
        index_date,
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    # https://github.com/ebmdatalab/tpp-sql-notebook/issues/46
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    
    died = patients.satisfying(
        """dead_ONS OR dead_GP""",
        dead_ONS = patients.died_from_any_cause(
            on_or_before=index_date,
            returning="binary_flag"
        ),
        dead_GP = patients.with_death_recorded_in_primary_care(
            on_or_before=index_date,
            returning="binary_flag"
        ),
        return_expectations={"incidence": 0.01}
    ),

    registered = patients.registered_as_of(
        index_date,
        return_expectations={"incidence": 0.99}
    ),

    # atrial fibrillation
    atrial_fibrillation = patients.with_these_clinical_events(
        codes_af,
        returning="binary_flag",
        on_or_before = "index_date",
        return_expectations={"incidence": 0.10}
    ),
    
    # practice 
    practice=patients.registered_practice_as_of(
    "index_date",
    returning="pseudo_id",
    return_expectations={
        "int": {"distribution": "normal", "mean": 1000, "stddev": 100},
        "incidence": 1,
        },
            ),
            
    ageband = patients.categorised_as(
        {
            "0": "DEFAULT",
            "18-49": """ age >= 18 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate":"universal",
            "category": {"ratios": {"18-49": 0.5, "50-59": 0.2, "60-69": 0.1, "70-79":0.1, "80+":0.1 }}
        },
    ),
  
    allpatients=patients.satisfying("""age>=0""", return_expectations={"incidence": 1}),
    
    # event population
    inr = patients.with_these_clinical_events(
        codes_inr,
        returning="binary_flag",
        between = ["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 0.80}
    ),

    inr_denom = patients.with_these_medications(
        codes_warfarin,
        returning="binary_flag",
        between = ["index_date - 3 months", "index_date - 1 day"],
        return_expectations={"incidence": 0.80}
    ),
    
    high_inr_denom = patients.satisfying(
        """(inr_denom)""",
        return_expectations={"incidence": 0.80}
    ),

    high_inr2_denom = patients.satisfying(
        """(inr_denom AND inr)""",
        return_expectations={"incidence": 0.70}
    ),
        
    renal_function_test_denom = patients.with_these_medications(
        codes_doac,
        returning="binary_flag",
        between = ["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 0.80}
    ),



    #  events
    inr_numer = patients.satisfying( # this will be both a numerator and denominator
        "(inr_denom AND inr)",
        return_expectations={"incidence": 0.40}
    ),
    
    high_inr_numer = patients.satisfying(
        """(high_inr_denom AND max_inr_value>=8)""",
        max_inr_value=patients.maximum_of(
            first_inr_value = patients.with_these_clinical_events(
                codes_inr,
                find_first_match_in_period=True,
                returning="numeric_value",
                between = ["index_date", "last_day_of_month(index_date)"],
            ),
            last_inr_value = patients.with_these_clinical_events(
                codes_inr,
                find_last_match_in_period=True,
                returning="numeric_value",
                between = ["index_date", "last_day_of_month(index_date)"],
            ),
        ),
        return_expectations={"incidence": 0.10}
    ),

    high_inr2_numer = patients.satisfying(
        """(high_inr2_denom AND high_inr_numer)""",
        return_expectations={"incidence": 0.10}
    ),
        
    renal_function_test_numer = patients.satisfying(
        """(renal_function_test_denom AND renal_function_test)""",
        renal_function_test = patients.with_these_clinical_events(
            codes_renal_function_test,
            returning="binary_flag",
            between = ["index_date - 12 months", "last_day_of_month(index_date)"],
        ),
        return_expectations={"incidence": 0.10}
    ),
 )
   
    
measures = []
for k1 in measures_dict.keys():
    for k2 in measures_dict[k1]["groups"].keys():
        #print(measures_dict[k1][k2])
        measures = measures + [Measure(**measures_dict[k1]["groups"][k2]["measure_args"])]
    
