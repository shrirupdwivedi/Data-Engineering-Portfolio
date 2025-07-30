-- 2. List the names of students with id in the range of v2 (id) to v3 (inclusive).
CREATE INDEX student_indx ON Student(id,name) 
EXPLAIN 
SELECT name FROM Student WHERE id BETWEEN @v2 AND @v3;

/* 

● What was the bottleneck? no index in relevant columns
● How did you identify it? Using schema
● What method you chose to resolve the bottleneck? creating index 


*/

