
SELECT COUNT(*)
FROM euro_cup_2016.match_details AS t1, euro_cup_2016.match_details AS t2
WHERE t1.match_no = t2.match_no
AND t1.team_id != t2.team_id
AND t1.goal_score - t2.goal_score = 1
AND t1.win_lose = 'W'
AND t1.penalty_score IS NULL

-- sql_q1_sol

