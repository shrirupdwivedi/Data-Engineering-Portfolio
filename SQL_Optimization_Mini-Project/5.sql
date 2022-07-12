
-- 5. List the names of students who have taken a course from department v6 (deptId), but not v7.

CREATE INDEX trid ON Transcript(studId)

EXPLAIN ANALYZE
SELECT * FROM Student, 
	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode
	AND studId NOT IN
	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;

/*


ORIGINAL RESULT
'-> Nested loop inner join  (cost=46.52 rows=10) (actual time=0.118..0.118 rows=0 loops=1)
    -> Filter: (transcript.crsCode = course.crsCode)  (cost=20.52 rows=10) (actual time=0.115..0.115 rows=0 loops=1)
        -> Inner hash join (<hash>(transcript.crsCode)=<hash>(course.crsCode))  (cost=20.52 rows=10) (actual time=0.114..0.114 rows=0 loops=1)
            -> Filter: (transcript.studId is not null)  (cost=0.13 rows=10) (never executed)
                -> Table scan on Transcript  (cost=0.13 rows=100) (never executed)
            -> Hash
                -> Filter: (course.deptId = <cache>((@v6)))  (cost=10.25 rows=10) (actual time=0.108..0.108 rows=0 loops=1)
                    -> Table scan on Course  (cost=10.25 rows=100) (actual time=0.019..0.093 rows=100 loops=1)
    -> Filter: <in_optimizer>(transcript.studId,<exists>(select #3) is false)  (cost=0.25 rows=1) (never executed)
        -> Index lookup on Student using sid (id=transcript.studId)  (cost=0.25 rows=1) (never executed)
        -> Select #3 (subquery in condition; dependent)
            -> Limit: 1 row(s)  (cost=110.52 rows=1)
                -> Filter: <if>(outer_field_is_not_null, <is_not_null_test>(transcript.studId), true)  (cost=110.52 rows=100)
                    -> Filter: (<if>(outer_field_is_not_null, ((<cache>(transcript.studId) = transcript.studId) or (transcript.studId is null)), true) and (transcript.crsCode = course.crsCode))  (cost=110.52 rows=100)
                        -> Inner hash join (<hash>(transcript.crsCode)=<hash>(course.crsCode))  (cost=110.52 rows=100)
                            -> Table scan on Transcript  (cost=0.13 rows=100)
                            -> Hash
                                -> Filter: (course.deptId = <cache>((@v7)))  (cost=10.25 rows=10)
                                    -> Table scan on Course  (cost=10.25 rows=100)
'

OPTIMIZED RESULT

'-> Nested loop inner join  (cost=46.52 rows=10) (actual time=0.201..0.201 rows=0 loops=1)
    -> Filter: (transcript.crsCode = course.crsCode)  (cost=20.52 rows=10) (actual time=0.200..0.200 rows=0 loops=1)
        -> Inner hash join (<hash>(transcript.crsCode)=<hash>(course.crsCode))  (cost=20.52 rows=10) (actual time=0.199..0.199 rows=0 loops=1)
            -> Filter: (transcript.studId is not null)  (cost=0.13 rows=10) (never executed)
                -> Table scan on Transcript  (cost=0.13 rows=100) (never executed)
            -> Hash
                -> Filter: (course.deptId = <cache>((@v6)))  (cost=10.25 rows=10) (actual time=0.183..0.183 rows=0 loops=1)
                    -> Table scan on Course  (cost=10.25 rows=100) (actual time=0.023..0.156 rows=100 loops=1)
    -> Filter: <in_optimizer>(transcript.studId,<exists>(select #3) is false)  (cost=0.25 rows=1) (never executed)
        -> Index lookup on Student using sid (id=transcript.studId)  (cost=0.25 rows=1) (never executed)
        -> Select #3 (subquery in condition; dependent)
            -> Limit: 1 row(s)  (cost=10.22 rows=0.02)
                -> Filter: <if>(outer_field_is_not_null, <is_not_null_test>(transcript.studId), true)  (cost=10.22 rows=0.02)
                    -> Filter: (course.crsCode = transcript.crsCode)  (cost=10.22 rows=0.02)
                        -> Inner hash join (<hash>(course.crsCode)=<hash>(transcript.crsCode))  (cost=10.22 rows=0.02)
                            -> Filter: (course.deptId = <cache>((@v7)))  (cost=4.71 rows=1)
                                -> Table scan on Course  (cost=4.71 rows=100)
                            -> Hash
                                -> Filter: <if>(outer_field_is_not_null, ((<cache>(transcript.studId) = transcript.studId) or (transcript.studId is null)), true)  (cost=0.70 rows=2)
                                    -> Alternative plans for IN subquery: Index lookup unless studId IS NULL  (cost=0.70 rows=2)
                                        -> Index lookup on Transcript using trid (studId=<cache>(transcript.studId) or NULL)
                                        -> Table scan on Transcript
'
● What was the bottleneck? The filter process in transcript.studId took more time as it had no index
● How did you identify it? using EXPLAIN ANALYE statement
● What method you chose to resolve the bottleneck? creating index in transcript.studId

*/