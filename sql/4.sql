with drug_list as (
select distinct drug_concept_id, concept_name, count(*) as cnt
from de.drug_exposure de
join de.concept
on drug_concept_id = concept_id
where concept_id in (
40213154,19078106,19009384,40224172,19127663,1511248,40169216,1539463,
19126352,1539411,1332419,40163924,19030765,19106768,19075601)
group by drug_concept_id,concept_name
order by count(*) desc
)
, drugs as (select drug_concept_id, concept_name from drug_list)
, prescription_count as (select drug_concept_id, cnt from drug_list)
SELECT dg.concept_name
FROM de.drug_pair dp
JOIN drugs dg ON dg.drug_concept_id = dp.drug_concept_id1
JOIN prescription_count pc ON pc.drug_concept_id = dp.drug_concept_id1
WHERE
(SELECT pc.cnt as cnt1
FROM prescription_count pc
WHERE pc.drug_concept_id = dp.drug_concept_id1)
<
(SELECT pc.cnt as cnt2
FROM prescription_count pc
WHERE pc.drug_concept_id = dp.drug_concept_id2)
ORDER BY pc.cnt;