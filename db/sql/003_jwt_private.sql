-- Seed JWT private secret for local development/test
-- This file inserts or updates the `jwt_private` setting used by the application to sign JWT tokens.

INSERT INTO settings (key, value, description, created_at, updated_at)
VALUES ('jwt_private', '6aw-zJR1JVOrA6qW2LXgdJ8igknw--r8teMqQYLH5FQEIr4Xy2LcoKJAWp9UyCYU', 'JWT HMAC secret used to sign tokens', now(), now())
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now();
