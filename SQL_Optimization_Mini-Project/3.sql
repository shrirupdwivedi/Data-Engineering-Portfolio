-- 3. List the names of students who have taken course v4 (crsCode).

EXPLAIN ANALYZE
SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);


/*

'-> Inner hash join (student.id = `<subquery2>`.studId)  (cost=414.91 rows=400) (actual time=0.175..0.472 rows=2 loops=1)
    -> Table scan on Student  (cost=5.04 rows=400) (actual time=0.007..0.269 rows=400 loops=1)
    -> Hash
        -> Table scan on <subquery2>  (cost=0.26..2.62 rows=10) (actual time=0.001..0.001 rows=2 loops=1)
            -> Materialize with deduplication  (cost=11.51..13.88 rows=10) (actual time=0.125..0.126 rows=2 loops=1)
                -> Filter: (transcript.studId is not null)  (cost=10.25 rows=10) (actual time=0.051..0.117 rows=2 loops=1)
                    -> Filter: (transcript.crsCode = <cache>((@v4)))  (cost=10.25 rows=10) (actual time=0.050..0.116 rows=2 loops=1)
                        -> Table scan on Transcript  (cost=10.25 rows=100) (actual time=0.020..0.089 rows=100 loops=1)
'
● What was the bottleneck? Nothing
● How did you identify it? No process in the query is wasting resources as observed through the result 
● What method you chose to resolve the bottleneck: N/A



*/