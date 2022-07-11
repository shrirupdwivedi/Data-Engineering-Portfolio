
SELECT c.country_name, COUNT(p.kick_id) AS penalty_shots
FROM euro_cup_2016.soccer_country AS c
INNER JOIN euro_cup_2016.penalty_shootout AS p
ON c.country_id = p.team_id
GROUP BY c.country_name
ORDER BY penalty_shots DESC
LIMIT 1


