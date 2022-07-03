SELECT ref.referee_name, count(m.match_no) as 'Number of Matches' 
FROM referee_mast as ref 
INNER JOIN match_mast as m 
USING(referee_id) 
GROUP BY ref.referee_name 