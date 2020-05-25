def pytest_addoption(parser):
    parser.addoption("--kafka-bootstrap-server", default="kafka:9092")
    parser.addoption("--postgres-host", default="postgres")
    parser.addoption("--postgres-user", default="postgres")
    parser.addoption("--postgres-password", default="postgres")
    parser.addoption("--postgres-dbname", default="checks")
