-- 4. List the names of students who have taken a course taught by professor v5 (name).


CREATE INDEX TID ON teaching(profId);
CREATE INDEX Tcr ON teaching(crsCode);
CREATE INDEX sid ON Student(id);
CREATE INDEX pid ON Professor(id);

EXPLAIN ANALYZE
SELECT name FROM Student,
	(SELECT studId FROM Transcript,
		(SELECT crsCode, semester FROM Professor
			JOIN Teaching
			WHERE Professor.name = @v5 AND Professor.id = Teaching.profId) as alias1
	WHERE Transcript.crsCode = alias1.crsCode AND Transcript.semester = alias1.semester) as alias2
WHERE Student.id = alias2.studId;

/*

INITIAL RESULT
'-> Inner hash join (student.id = transcript.studId)  (cost=1313.72 rows=160) (actual time=0.360..0.360 rows=0 loops=1)
    -> Table scan on Student  (cost=0.03 rows=400) (never executed)
    -> Hash
        -> Inner hash join (professor.id = teaching.profId)  (cost=1144.90 rows=4) (actual time=0.347..0.347 rows=0 loops=1)
            -> Filter: (professor.`name` = <cache>((@v5)))  (cost=0.95 rows=4) (never executed)
                -> Table scan on Professor  (cost=0.95 rows=400) (never executed)
            -> Hash
                -> Filter: ((teaching.semester = transcript.semester) and (teaching.crsCode = transcript.crsCode))  (cost=1010.70 rows=100) (actual time=0.336..0.336 rows=0 loops=1)
                    -> Inner hash join (<hash>(teaching.semester)=<hash>(transcript.semester)), (<hash>(teaching.crsCode)=<hash>(transcript.crsCode))  (cost=1010.70 rows=100) (actual time=0.336..0.336 rows=0 loops=1)
                        -> Table scan on Teaching  (cost=0.01 rows=100) (actual time=0.005..0.131 rows=100 loops=1)
                        -> Hash
                            -> Table scan on Transcript  (cost=10.25 rows=100) (actual time=0.020..0.092 rows=100 loops=1)
'
'
OPTIMIZED RESULT

'-> Nested loop inner join  (cost=53.55 rows=1) (actual time=1.243..1.243 rows=0 loops=1)
    -> Nested loop inner join  (cost=49.94 rows=10) (actual time=1.242..1.242 rows=0 loops=1)
        -> Nested loop inner join  (cost=46.33 rows=10) (actual time=1.241..1.241 rows=0 loops=1)
            -> Filter: ((transcript.crsCode is not null) and (transcript.studId is not null))  (cost=10.25 rows=100) (actual time=0.025..0.215 rows=100 loops=1)
                -> Table scan on Transcript  (cost=10.25 rows=100) (actual time=0.023..0.179 rows=100 loops=1)
            -> Filter: ((teaching.semester = transcript.semester) and (teaching.profId is not null))  (cost=0.26 rows=0.1) (actual time=0.010..0.010 rows=0 loops=100)
                -> Index lookup on Teaching using Tcr (crsCode=transcript.crsCode)  (cost=0.26 rows=1) (actual time=0.007..0.009 rows=1 loops=100)
        -> Index lookup on Student using sid (id=transcript.studId)  (cost=0.26 rows=1) (never executed)
    -> Filter: (professor.`name` = <cache>((@v5)))  (cost=0.25 rows=0.1) (never executed)
        -> Index lookup on Professor using pid (id=teaching.profId)  (cost=0.25 rows=1) (never executed)
'
● What was the bottleneck? One or more processes took more cost and had less actual work -> Inner hash join (professor.id = teaching.profId)  (cost=1144.90 rows=4) (actual time=0.347..0.347 rows=0 loops=1)
● How did you identify it? using EXPLAIN ANALYZE
● What method you chose to resolve the bottleneck: create multiple indexes where the processes it was needed.
CREATE INDEX TID ON teaching(profId);
CREATE INDEX Tcr ON teaching(crsCode);
CREATE INDEX sid ON Student(id);
CREATE INDEX pid ON Professor(id);

*/