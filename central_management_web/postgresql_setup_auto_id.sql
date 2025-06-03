





--- 










ALTER TABLE schedule
ADD CONSTRAINT days_valid CHECK (
    array_length(day, 1) = 3
    AND days <@ ARRAY['2','3','4','5','6','7','CN']
);


ALTER TABLE schedule
ADD CONSTRAINT check_time_2h
CHECK (end_time = start_time + INTERVAL '2 hours');