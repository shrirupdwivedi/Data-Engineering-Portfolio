EXPLAIN ANALYZE
SELECT name FROM Student,
	(SELECT studId
	FROM Transcript
		WHERE crsCode IN
		(SELECT crsCode FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))) as alias
WHERE id = alias.studId;

/*
'-> Nested loop inner join  (cost=7.12 rows=10) (actual time=0.155..0.155 rows=0 loops=1)
    -> Filter: (alias.studId is not null)  (cost=0.36..3.62 rows=10) (actual time=0.154..0.154 rows=0 loops=1)
        -> Table scan on alias  (cost=2.50..2.50 rows=0) (actual time=0.000..0.000 rows=0 loops=1)
            -> Materialize  (cost=2.50..2.50 rows=0) (actual time=0.153..0.153 rows=0 loops=1)
                -> Filter: (count(0) = (select #5))  (actual time=0.144..0.144 rows=0 loops=1)
                    -> Table scan on <temporary>  (actual time=0.000..0.000 rows=0 loops=1)
                        -> Aggregate using temporary table  (actual time=0.144..0.144 rows=0 loops=1)
                            -> Filter: (transcript.crsCode = `<subquery3>`.crsCode)  (cost=128.35 rows=103) (actual time=0.137..0.137 rows=0 loops=1)
                                -> Inner hash join (<hash>(transcript.crsCode)=<hash>(`<subquery3>`.crsCode))  (cost=128.35 rows=103) (actual time=0.136..0.136 rows=0 loops=1)
                                    -> Table scan on Transcript  (cost=1.28 rows=100) (never executed)
                                    -> Hash
                                        -> Table scan on <subquery3>  (cost=0.25..2.62 rows=10) (actual time=0.001..0.001 rows=0 loops=1)
                                            -> Materialize with deduplication  (cost=22.61..24.98 rows=10) (actual time=0.125..0.125 rows=0 loops=1)
                                                -> Filter: (course.crsCode is not null)  (cost=21.32 rows=10) (actual time=0.122..0.122 rows=0 loops=1)
                                                    -> Nested loop inner join  (cost=21.32 rows=10) (actual time=0.122..0.122 rows=0 loops=1)
                                                        -> Filter: ((course.deptId = <cache>((@v8))) and (course.crsCode is not null))  (cost=10.25 rows=10) (actual time=0.121..0.121 rows=0 loops=1)
                                                            -> Table scan on Course  (cost=10.25 rows=100) (actual time=0.019..0.102 rows=100 loops=1)
                                                        -> Covering index lookup on Teaching using Tcr (crsCode=course.crsCode)  (cost=1.01 rows=1) (never executed)
                    -> Select #5 (subquery in condition; uncacheable)
                        -> Aggregate: count(0)  (cost=22.35 rows=1)
                            -> Nested loop semijoin  (cost=21.32 rows=10)
                                -> Filter: ((course.deptId = <cache>((@v8))) and (course.crsCode is not null))  (cost=10.25 rows=10)
                                    -> Table scan on Course  (cost=10.25 rows=100)
                                -> Covering index lookup on Teaching using Tcr (crsCode=course.crsCode)  (cost=1.05 rows=1)
                -> Select #5 (subquery in projection; uncacheable)
                    -> Aggregate: count(0)  (cost=22.35 rows=1)
                        -> Nested loop semijoin  (cost=21.32 rows=10)
                            -> Filter: ((course.deptId = <cache>((@v8))) and (course.crsCode is not null))  (cost=10.25 rows=10)
                                -> Table scan on Course  (cost=10.25 rows=100)
                            -> Covering index lookup on Teaching using Tcr (crsCode=course.crsCode)  (cost=1.05 rows=1)
    -> Index lookup on Student using sid (id=alias.studId)  (cost=0.26 rows=1) (never executed)
'


*/