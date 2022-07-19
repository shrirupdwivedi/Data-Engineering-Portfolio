-- 3. List the names of students who have taken course v4 (crsCode).

CREATE INDEX transcript_idx_1 ON Transcript(crsCode);

EXPLAIN ANALYZE
SELECT name FROM Student WHERE id IN (SELECT studId FROM Transcript WHERE crsCode = @v4);


/*
● What was the bottleneck? No index on crsCode column in Transcript table
● How did you identify it? Used EXPLAIN ANALYZE on statement -> Table scan on Transcript  (cost=10.25 rows=100)
● What method you chose to resolve the bottleneck: Create index on crsCode column in Transcript table.
 Cost of Transcript table access and total execution time significantly went down.



*/