select rm.referee_name, sv.venue_name, count(*) count 
from  match_mast mm,
      referee_mast rm, 
      soccer_venue sv 
where mm.referee_id = rm.referee_id 
  and mm.venue_id= sv.venue_id 
group by rm.referee_name, sv.venue_name
 ;

