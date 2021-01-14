#cockcroft-Gault Function 

def cockcroft_gault_crcl(self, between = None): 
    
    """Calculates creatinine clearance using the most recent serum creatinine and weight. 
    If either is missing - returns an empty value. Can limit how contemporary the values used by changing the between datecockcroft."""
    
    date_condition = make_date_filter("ConsultationDate", between)
    
    weight_codes = [
            "X76C7",  # Concept containing "body weight" terms:
            "22A..",  # O/E weight
    ] 
    
    weight_codes_sql = codelist_to_sql(weight_codes)
    
    creatinine_codes = ["BLANK BLANK"] #this needs to be filled in 
    
    creatinine_codes_sql = codelist_to_sql(creatinine_codes)
    
    creatinine_date_condition = make_date_filter("ConsultationDate", between, upper_bound_only=True)

    patients_cte = """
        SELECT Patient_ID, DateOfBirth, sex
        FROM Patient
        """
    
    weights_cte = f"""
        SELECT t.Patient_ID, t.weight, t.ConsultationDate
        FROM (
            SELECT Patient_ID, NumericValue AS weight, ConsultationDate,
            ROW_NUMBER() OVER (PARTITION BY Patient_ID ORDER BY ConsultationDate DESC) AS rownum
            FROM CodedEvent
            WHERE CTV3Code IN ({weight_codes_sql}) AND {date_condition}
          ) t
          WHERE t.rownum = 1
        """
    
    creatinine_cte = f"""
          SELECT t.Patient_ID, t.creatinine, t.ConsultationDate
          FROM (
            SELECT Patient_ID, NumericValue AS height, ConsultationDate,
            ROW_NUMBER() OVER (PARTITION BY Patient_ID ORDER BY ConsultationDate DESC) AS rownum
            FROM CodedEvent
            WHERE CTV3Code IN ({creatinine_codes_sql}) AND {creatinine_date_condition}
          ) t
          WHERE t.rownum = 1
        """

    sql = f"""
    SELECT
    patients.Patient_ID AS patient_id,  
        CASE 
            WHEN sex = 'F' THEN ROUND(COALESCE(((140-age)*(NULLIF(weight,0)))/((NULLIF(creatinine,0))*72))*0.85) AS crcl, 
            ELSE ROUND(COALESCE(((140-age)*(NULLIF(weight,0)))/((NULLIF(creatinine,0))*72))) AS crcl, 
        END   
    FROM ({patients_cte}) AS patients
    LEFT JOIN ({creatinine_cte}) AS crcl
    """
    columns = ["patient_id", "crcl"]
    
    return columns, sql