SELECT s.venue_name 
FROM match_mast as m  
INNER JOIN soccer_venue as s 
USING(venue_id) 
WHERE decided_by = 'P' 

-- sql_q1_sol