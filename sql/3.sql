SELECT drug_concept_id,
       MIN(drug_exposure_start_date),
       MAX(drug_exposure_end_date),
       MAX(drug_exposure_end_date) - MIN(drug_exposure_start_date) + 1 as duration
FROM de.drug_exposure
WHERE person_id=1891866
GROUP BY 1
ORDER BY 4 DESC;