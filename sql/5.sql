SELECT COUNT(*)
FROM
(SELECT co.person_id
FROM de.condition_occurrence co
JOIN de.person p on co.person_id = p.person_id
JOIN de.drug_exposure de on p.person_id = de.person_id
WHERE co.condition_concept_id IN
(3191208,36684827,3194332,3193274,43531010,4130162,45766052,
45757474,4099651,4129519,4063043,4230254,4193704,4304377,201826,
 3194082,3192767)
AND DATE_PART('year', AGE(p.birth_datetime)) >= 18
AND de.drug_concept_id = 40163924
GROUP BY 1
HAVING sum(de.days_supply) >= 90) as cpdpi;