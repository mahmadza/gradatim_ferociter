

/* as per https://aws.amazon.com/de/blogs/big-data/implement-serverless-log-analytics-using-amazon-kinesis-analytics/ */

/* create destination stream to store response count */
CREATE STREAM "DESTINATION_SQL_STREAM" (
  applicationName VARCHAR(64),
  contact VARCHAR(64),
  response  SMALLINT,
  responseCount SMALLINT);


-- Aggregrate response over joined data with host application mapping stored on S3.
-- It always uses the latest S3 file

CREATE OR REPLACE PUMP "DESTINATION_SQL_STREAM" AS
  INSERT INTO "DESTINATION_SQL_STREAM"
  SELECT STREAM   metadata."ApplicationName",
                  metadata."Contact",
                  logstream."response",
                  COUNT(*) as responseCount
      FROM "SOURCE_SQL_STREAM_001" logstream LEFT JOIN "ApplicationHostMapping" metadata
        ON logstream."host" = metadata."Host"
          GROUP BY  metadata."ApplicationName",
                    metadata."Contact",
                    logstream."response",
                    FLOOR((logstream.ROWTIME - TIMESTAMP '1970-01-01 00:00:00') MINUTE / 5 TO MINUTE);
