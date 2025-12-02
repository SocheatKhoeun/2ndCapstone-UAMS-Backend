-- Add start_time and end_time timestamptz columns to course_offerings
ALTER TABLE course_offerings
  ADD COLUMN IF NOT EXISTS start_time TIMESTAMP WITH TIME ZONE;

ALTER TABLE course_offerings
  ADD COLUMN IF NOT EXISTS end_time TIMESTAMP WITH TIME ZONE;

-- Verify
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'course_offerings';
