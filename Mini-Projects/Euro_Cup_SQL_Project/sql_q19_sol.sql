 SELECT COUNT(md.player_gk) 
FROM match_details as md  
INNER JOIN match_captain mc  
ON md.player_gk = mc.player_captain 