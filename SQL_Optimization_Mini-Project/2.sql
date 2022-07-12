-- 2. List the names of students with id in the range of v2 (id) to v3 (inclusive).
EXPLAIN ANALYZE
SELECT name FROM Student WHERE id BETWEEN @v2 AND @v3;

/* 
'-> Filter: (student.id between <cache>((@v2)) and <cache>((@v3)))  (cost=5.44 rows=44) (actual time=0.032..0.407 rows=278 loops=1)
    -> Table scan on Student  (cost=5.44 rows=400) (actual time=0.027..0.328 rows=400 loops=1)
'
● What was the bottleneck? Nothing
● How did you identify it? Using result from above.
● What method you chose to resolve the bottleneck N/A


*/

