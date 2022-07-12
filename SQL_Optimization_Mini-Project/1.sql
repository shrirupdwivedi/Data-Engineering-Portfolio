
-- 1. List the name of the student with id equal to v1 (id).
EXPLAIN ANALYZE
SELECT name FROM Student WHERE id = @v1;

/*'-> Filter: (student.id = <cache>((@v1)))  (cost=41.00 rows=40) (actual time=0.090..0.335 rows=1 loops=1)
    -> Table scan on Student  (cost=41.00 rows=400) (actual time=0.023..0.279 rows=400 loops=1)
' 

● What was the bottleneck? Nothing
● How did you identify it? The above result from EXPLAIN ANALYZE
● What method you chose to resolve the bottleneck? N/A


*/