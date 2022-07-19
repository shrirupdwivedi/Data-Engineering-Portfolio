EXPLAIN ANALYZE
SELECT name FROM Student,
	(SELECT studId
	FROM Transcript
		WHERE crsCode IN
		(SELECT crsCode FROM Course WHERE deptId = @v8)
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course )) as alias
WHERE id = alias.studId;

/*
'-> Nested loop inner join  (cost=3.43 rows=2) (actual time=0.034..0.034 rows=0 loops=1)
    -> Filter: (alias.studId is not null)  (cost=1.36..2.73 rows=2) (actual time=0.033..0.033 rows=0 loops=1)
        -> Table scan on alias  (cost=2.50..2.50 rows=0) (actual time=0.000..0.000 rows=0 loops=1)
            -> Materialize  (cost=2.50..2.50 rows=0) (actual time=0.032..0.032 rows=0 loops=1)
                -> Filter: (count(0) = (select #5))  (actual time=0.021..0.021 rows=0 loops=1)
                    -> Table scan on <temporary>  (actual time=0.000..0.000 rows=0 loops=1)
                        -> Aggregate using temporary table  (actual time=0.020..0.020 rows=0 loops=1)
                            -> Nested loop inner join  (cost=5.66 rows=10) (actual time=0.014..0.014 rows=0 loops=1)
                                -> Filter: (`<subquery3>`.crsCode is not null)  (cost=12.66..1.97 rows=10) (actual time=0.013..0.013 rows=0 loops=1)
                                    -> Table scan on <subquery3>  (cost=0.25..2.62 rows=10) (actual time=0.001..0.001 rows=0 loops=1)
                                        -> Materialize with deduplication  (cost=14.11..16.48 rows=10) (actual time=0.013..0.013 rows=0 loops=1)
                                            -> Filter: (course.crsCode is not null)  (cost=12.82 rows=10) (actual time=0.008..0.008 rows=0 loops=1)
                                                -> Nested loop inner join  (cost=12.82 rows=10) (actual time=0.008..0.008 rows=0 loops=1)
                                                    -> Filter: (course.crsCode is not null)  (cost=1.75 rows=10) (actual time=0.007..0.007 rows=0 loops=1)
                                                        -> Index lookup on Course using course_idx1 (deptId=(@v8)), with index condition: (course.deptId = <cache>((@v8)))  (cost=1.75 rows=10) (actual time=0.007..0.007 rows=0 loops=1)
                                                    -> Covering index lookup on Teaching using Tcr (crsCode=course.crsCode)  (cost=1.01 rows=1) (never executed)
                                -> Index lookup on Transcript using transcript_idx_1 (crsCode=`<subquery3>`.crsCode)  (cost=2.76 rows=1) (never executed)
                    -> Select #5 (subquery in condition; uncacheable)
                        -> Zero input rows (no matching row in const table), aggregated into one output row  (cost=0.00..0.00 rows=1)
                -> Select #5 (subquery in projection; uncacheable)
                    -> Zero input rows (no matching row in const table), aggregated into one output row  (cost=0.00..0.00 rows=1)
    -> Single-row index lookup on Student using student_idx1 (id=alias.studId)  (cost=0.30 rows=1) (never executed)
'


'-> Nested loop inner join  (cost=3.43 rows=2) (actual time=0.034..0.034 rows=0 loops=1)
    -> Filter: (alias.studId is not null)  (cost=1.36..2.73 rows=2) (actual time=0.033..0.033 rows=0 loops=1)
        -> Table scan on alias  (cost=2.50..2.50 rows=0) (actual time=0.000..0.000 rows=0 loops=1)
            -> Materialize  (cost=2.50..2.50 rows=0) (actual time=0.033..0.033 rows=0 loops=1)
                -> Filter: (count(0) = (select #4))  (actual time=0.023..0.023 rows=0 loops=1)
                    -> Table scan on <temporary>  (actual time=0.001..0.001 rows=0 loops=1)
                        -> Aggregate using temporary table  (actual time=0.022..0.022 rows=0 loops=1)
                            -> Nested loop inner join  (cost=5.55 rows=10) (actual time=0.013..0.013 rows=0 loops=1)
                                -> Filter: (`<subquery3>`.crsCode is not null)  (cost=2.67..1.94 rows=10) (actual time=0.013..0.013 rows=0 loops=1)
                                    -> Table scan on <subquery3>  (cost=0.26..2.62 rows=10) (actual time=0.001..0.001 rows=0 loops=1)
                                        -> Materialize with deduplication  (cost=3.01..5.38 rows=10) (actual time=0.012..0.012 rows=0 loops=1)
                                            -> Filter: (course.crsCode is not null)  (cost=1.75 rows=10) (actual time=0.009..0.009 rows=0 loops=1)
                                                -> Index lookup on Course using course_idx1 (deptId=(@v8)), with index condition: (course.deptId = <cache>((@v8)))  (cost=1.75 rows=10) (actual time=0.008..0.008 rows=0 loops=1)
                                -> Index lookup on Transcript using transcript_idx_1 (crsCode=`<subquery3>`.crsCode)  (cost=2.68 rows=1) (never executed)
                    -> Select #4 (subquery in condition; run only once)
                        -> Count rows in Course
    -> Single-row index lookup on Student using student_idx1 (id=alias.studId)  (cost=0.30 rows=1) (never executed)

'
● What was the bottleneck? 1)As all the courses in Teaching table existed in the Course table, there was no need to select crsCode from the teaching table. 
2) There was no need to use the deptId=v8 twice as the WHERE clause would take care of the check
● How did you identify it? using by reading the script
● What method you chose to resolve the bottleneck? by updating the script
*/
