SELECT COUNT(match_no) as 'Maximum number of foul cards in one match' from player_booked 
GROUP BY match_no 
ORDER BY COUNT(match_no) DESC 
LIMIT 1 