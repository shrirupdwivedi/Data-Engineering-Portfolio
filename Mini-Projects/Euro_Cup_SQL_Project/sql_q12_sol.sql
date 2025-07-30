Select pp.position_desc, sc.country_name , count(*) as count 
from goal_details gd, 
	 player_mast pm,
     playing_position pp,
     soccer_country sc 
where gd.player_id = pm.player_id
  and pm.posi_to_play = pp.position_id
  and gd.team_id = sc.country_id 
group by pp.position_desc, sc.country_name 
order by pp.position_desc, sc.country_name;