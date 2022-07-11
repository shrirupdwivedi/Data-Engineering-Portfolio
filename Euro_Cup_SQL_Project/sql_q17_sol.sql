
SELECT 
	sc.country_name
	,count(*) AS 'ass_ref_count'
FROM asst_referee_mast AS arm

INNER JOIN soccer_country AS sc ON
	arm.country_id = sc.country_id
GROUP BY
	sc.country_name
ORDER BY 
	ass_ref_count DESC
LIMIT 1