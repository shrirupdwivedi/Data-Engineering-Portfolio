SELECT p.player_name, p.jersey_no, p.playing_club 
FROM match_details as m 
INNER JOIN player_mast as p 
ON m.player_gk = p.player_id 
WHERE p.team_id = 1206 
