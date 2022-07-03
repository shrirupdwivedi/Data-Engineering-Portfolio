SELECT p.player_name,p.jersey_no 
FROM match_details as m 
LEFT JOIN player_mast as p 
ON m.player_gk = p.player_id 
WHERE m.team_id = 1208 and m.play_stage = 'G' 

-- sql_q1_sol