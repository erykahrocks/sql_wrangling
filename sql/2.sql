SELECT DISTINCT concept.concept_name
FROM de.concept
    JOIN de.condition_occurrence co on concept.concept_id = co.condition_concept_id
WHERE LOWER(concept_name) SIMILAR TO '(a|b|c|d|e)%heart%';
