SELECT * 
FROM player_mast as p  
INNER JOIN soccer_country as c 
ON c.country_id = p.team_id 
WHERE c.country_name = 'England' and p.playing_club = 'Liverpool' 
