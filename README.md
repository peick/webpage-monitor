# webpage-monitor

The *webpage-monitor* monitors the status of a webpage and stores the check
results into kafka. A kafka consumer stores the check results into a postgres
database.

## How to run

To build the docker image run `make build`. This creates a docker image called
`webpage-monitor`.

### wpmon-collector

run e.g. with `docker run webpage-monitor wpmon-collector ...`

```plain
usage: wpmon-collector [-h] [-v] [--kafka-host KAFKA_HOST]
                       [--kafka-port KAFKA_PORT] --kafka-topic KAFKA_TOPIC
                       --url URL [--pattern PATTERN] [--interval INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase log level
  --kafka-host KAFKA_HOST
                        Hostname of the kafka server. Default: localhost
  --kafka-port KAFKA_PORT
                        Port of the kafka server. Default: 9092
  --kafka-topic KAFKA_TOPIC
                        The kafka topic to read from or publish to
  --url URL             The url to monitor
  --pattern PATTERN     A regular expression checked on the downloaded webpage
  --interval INTERVAL   Check interval in seconds. Default: 5
```

### wpmon-pgwriter

run e.g. with `docker run webpage-monitor wpmon-pgwriter ...`

```plain
usage: wpmon-pgwriter [-h] [-v] [--kafka-host KAFKA_HOST]
                      [--kafka-port KAFKA_PORT] --kafka-topic KAFKA_TOPIC
                      [--kafka-group-id KAFKA_GROUP_ID] --db-host DB_HOST
                      [--db-port DB_PORT] --db-user DB_USER --db-password
                      DB_PASSWORD --db-name DB_NAME --db-table DB_TABLE

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase log level
  --kafka-host KAFKA_HOST
                        Hostname of the kafka server. Default: localhost
  --kafka-port KAFKA_PORT
                        Port of the kafka server. Default: 9092
  --kafka-topic KAFKA_TOPIC
                        The kafka topic to read from or publish to
  --kafka-group-id KAFKA_GROUP_ID
                        Kafka consumer group. Default: pgwriter
  --db-host DB_HOST     Postgress server hostname
  --db-port DB_PORT
  --db-user DB_USER     Database username
  --db-password DB_PASSWORD
                        Database password
  --db-name DB_NAME     Database to use
  --db-table DB_TABLE
```

## Testing manually

I.e. all tests are executed in CI, but it's also possible to run them manually.

To run unittests execute: `tox -- -m "not integ"`

To run integration tests execute: `tox -- -m integ`
