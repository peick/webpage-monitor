CREATE DATABASE checks;

\connect checks;

CREATE TABLE webpage_checks_0 (
    id BIGSERIAL PRIMARY KEY,
    httpResponseTime INT NOT NULL,
    httpStatusCode INT NULL,
    errorCode INT NULL,
    patternFound BOOL NULL
);

CREATE TABLE webpage_checks_1 (
    id BIGSERIAL PRIMARY KEY,
    httpResponseTime INT NOT NULL,
    httpStatusCode INT NULL,
    errorCode INT NULL,
    patternFound BOOL NULL
);
