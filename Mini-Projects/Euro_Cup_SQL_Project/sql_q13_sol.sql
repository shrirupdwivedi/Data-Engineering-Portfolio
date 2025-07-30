SELECT p.player_name 
FROM player_mast as p 
INNER JOIN goal_details as g 
USING(player_id)  
where p.posi_to_play = 'DF' 