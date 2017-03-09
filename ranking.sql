SELECT referee_name, count(case call_accuracy when 'IC' then 1 else null end) AS icc, count(case call_accuracy when 'INC' then 1 else null end) as incc, 
    count(case call_accuracy when 'IC' then 1 else null end) + count(case call_accuracy 
    when 'INC' then 1 else null end) as totali, count(comment) as total, ((count(case call_accuracy 
    when 'IC' then 1 else null end) + count(case call_accuracy when 'INC' then 1 else null 
    end)) * 1.00) / count(comment) AS percentage FROM referees JOIN calls ON 
    referees.game_code = calls.game_code GROUP BY referee_name ORDER BY total DESC;