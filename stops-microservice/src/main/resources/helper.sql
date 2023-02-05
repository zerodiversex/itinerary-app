DELETE FROM
    stop
WHERE
        stop.stop_desc NOT LIKE '%75%';

DELETE FROM
    stop a
    USING stop b
WHERE
    a.stop_id < b.stop_id
  AND a.stop_desc = b.stop_desc;

DELETE FROM
    transfer t
WHERE
        t.from_stop_id
        NOT IN (SELECT stop_id FROM stop)
  AND t.to_stop_id
    NOT IN (SELECT stop_id FROM stop);