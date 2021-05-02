select visit_end_date - visit_start_date + 1 as max_duration, COUNT(*)
from de.visit_occurrence
where visit_end_date - visit_start_date + 1 =
(SELECT MAX(visit_end_date - visit_start_date + 1) as max_
FROM de.visit_occurrence)
GROUP BY 1;