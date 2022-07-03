SELECT ref.referee_name, COUNT(pb.match_no) as 'Number of Bookings' 
FROM referee_mast as ref 
INNER JOIN match_mast as m 
USING(referee_id) 
INNER JOIN player_booked as pb 
USING (match_no) 
GROUP BY ref.referee_name 
ORDER BY COUNT(pb.match_no) DESC 
LIMIT 1 