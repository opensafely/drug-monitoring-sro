

measures_dict = dict(
    # dictionary of dictionaries, listing all measure variables and the grouping variables
    inr=dict(
        label = "INR",
        groups = dict(
            allpatients = dict(   
                label = "overall",
                measure_args = dict(
                    id = "inr_allpatients", # this should be "{key of the level 1 dict}_{key of the level 3 dict}"
                    numerator = "inr_numer",
                    denominator = "inr_denom",
                    group_by = "allpatients"
                ),
            ),
            practice = dict(
                label = "by practice",
                measure_args = dict(
                    id = "inr_practice",
                    numerator = "inr_numer",
                    denominator = "inr_denom",
                    group_by = "practice"
                ),
            ),
                        
            ageband = dict(
                label = "by age band",
                measure_args = dict(
                    id = "inr_ageband",
                    numerator = "inr_numer",
                    denominator = "inr_denom",
                    group_by = "ageband"
                ),
            ),                    
        ),
    ),
    high_inr=dict(
        label = "High INR",
        groups = dict(
            allpatients = dict(   
                label = "overall",
                measure_args = dict(
                    id = "high_inr_allpatients",
                    numerator = "high_inr_numer",
                    denominator = "high_inr_denom",
                    group_by = "allpatients"
                ),
            ),
            practice = dict(
                label = "by practice",
                measure_args = dict(
                    id = "high_inr_practice",
                    numerator = "high_inr_numer",
                    denominator = "high_inr_denom",
                    group_by = "practice"
                ),
                
            ),
            ageband = dict(
                label = "by age band",
                measure_args = dict(
                    id = "high_inr_ageband",
                    numerator = "high_inr_numer",
                    denominator = "high_inr_denom",
                    group_by = "ageband"
                ),
            ),
        ),
    ),
    
    high_inr2=dict(
        label = "High INRs among pts tested",
        groups = dict(
            allpatients = dict(   
                label = "overall",
                measure_args = dict(
                    id = "high_inr2_allpatients",
                    numerator = "high_inr2_numer",
                    denominator = "high_inr2_denom",
                    group_by = "allpatients"
                ),
            ),
            practice = dict(
                label = "by practice",
                measure_args = dict(
                    id = "high_inr2_practice",
                    numerator = "high_inr2_numer",
                    denominator = "high_inr2_denom",
                    group_by = "practice"
                ),
                
            ),
            ageband = dict(
                label = "by age band",
                measure_args = dict(
                    id = "high_inr2_ageband",
                    numerator = "high_inr2_numer",
                    denominator = "high_inr2_denom",
                    group_by = "ageband"
                ),
            ),
        ),
    ),

    renal_function_test = dict(
        label = "Renal Function Test",
        groups = dict(
            allpatients = dict(   
                label = "overall",
                measure_args = dict(
                    id = "renal_function_test_allpatients",
                    numerator = "renal_function_test_numer",
                    denominator="renal_function_test_denom",
                    group_by = "allpatients"
                ),
            ),
            practice = dict(
                label = "by practice",
                measure_args = dict(
                    id = "renal_function_test_practice",
                     numerator = "renal_function_test_numer",
                    denominator="renal_function_test_denom",
                    group_by = "practice"
                ),
            ),
            ageband = dict(
                label = "by age band",
                measure_args = dict(
                    id = "renal_function_test_ageband",
                    numerator = "renal_function_test_numer",
                    denominator="renal_function_test_denom",
                    group_by = "ageband"
                ),
            ),

        ),
    ),
)
