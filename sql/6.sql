SELECT de.person_id, de.drug_exposure_start_date, STRING_AGG (CAST (de.drug_concept_id AS TEXT), ', ') as agg
FROM de.condition_occurrence co
JOIN de.drug_exposure de on co.person_id = de.person_id
WHERE co.condition_concept_id IN
(3191208,36684827,3194332,3193274,43531010,4130162,45766052,
45757474,4099651,4129519,4063043,4230254,4193704,4304377,201826,
 3194082,3192767)
AND de.drug_concept_id IN
(19018935, 1539411,1539463, 19075601, 1115171)
GROUP BY 1,2
ORDER BY 1,2;