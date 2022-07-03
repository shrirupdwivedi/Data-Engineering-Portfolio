select m.play_stage, COUNT(*) as 'number of substitution' 
from player_in_out as p 
INNER JOIN match_mast as m 
USING(match_no) 
GROUP BY (m.play_stage) 

-- sql_q1_sol