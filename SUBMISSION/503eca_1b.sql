-- Check data type of vtt table DESCRIBE vtt;
-- Convert TimeFrom and TimeTo to TIME type
ALTER TABLE vtt MODIFY TimeFrom TIME(3);

ALTER TABLE vtt MODIFY TimeTo TIME(3);

-- Use TIMESTAMPDIFF to calculate the difference between two datetime
-- Specify the unit as microsecond, the two datetime: TimeFrom and TimeTo
CREATE TABLE vttclean AS
SELECT
	*,
	TIMESTAMPDIFF(
		MICROSECOND, TimeFrom, TimeTo)
	DIV 1000 AS milliseconds
FROM
	vtt;

-- To see result
SELECT
	*
FROM
	vttclean;