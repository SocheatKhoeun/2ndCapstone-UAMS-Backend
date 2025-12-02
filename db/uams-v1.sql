-- =========================
-- ENUM TYPES
-- =========================
CREATE TYPE session_status AS ENUM ('planned','completed','canceled','makeup');
CREATE TYPE attendance_status AS ENUM ('present','late','absent','excused');
CREATE TYPE attendance_method AS ENUM ('face','qr','manual');
CREATE TYPE device_type AS ENUM ('kiosk','mobile','web');
CREATE TYPE gender_enum AS ENUM ('male','female','other');
CREATE TYPE verification_result AS ENUM ('success','fail_match','fail_liveness','fail_quality','error');
CREATE TYPE role AS ENUM ('superadmin','admin');
CREATE TYPE position AS ENUM ('professor','lecturer','assistant');

-- =========================
-- PEOPLE
-- =========================
CREATE TABLE admins (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  email           VARCHAR(255) UNIQUE NOT NULL,
  password        VARCHAR(255),
  role            role NOT NULL,        -- enum
  first_name      VARCHAR(255),
  last_name       VARCHAR(255),
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE settings (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  key             VARCHAR(255) UNIQUE NOT NULL,
  value           TEXT,
  description     TEXT,
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE instructors (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  first_name      VARCHAR(255),
  last_name       VARCHAR(255),
  email           VARCHAR(255) UNIQUE NOT NULL,
  phone_number    VARCHAR(50) UNIQUE NULL,
  password        VARCHAR(255),
  position        "position" NOT NULL,    -- enum
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

-- ======== GENERATIONS ========
CREATE TABLE generations (
  id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  generation  VARCHAR(255) UNIQUE NOT NULL,  -- e.g., 'Batch 2025'
  start_year  SMALLINT,
  end_year    SMALLINT,
  active      SMALLINT DEFAULT 1,
  created_at  TIMESTAMP DEFAULT NOW(),
  updated_at  TIMESTAMP DEFAULT NOW()
);


-- ======== STUDENTS (with FK to generations) ========
CREATE TABLE students (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  student_code    VARCHAR(50) UNIQUE NOT NULL,
  first_name      VARCHAR(255),
  last_name       VARCHAR(255),
  gender          gender_enum,
  dob             DATE,
  email           VARCHAR(255) UNIQUE NOT NULL,
  phone_number    VARCHAR(50) UNIQUE NULL,
  password        VARCHAR(255),
  address         TEXT,
  profile_image   VARCHAR(255),
  generation_id   INT REFERENCES generations(id),  -- <--- added
  group_id       INT NULL REFERENCES groups(id),
  active          SMALLINT DEFAULT 1,
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

-- helpful index for filtering by generation
CREATE INDEX idx_students_generation ON students (generation_id);

-- =========================
-- CATALOG
-- =========================
CREATE TABLE departments (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  name            VARCHAR(255) UNIQUE NOT NULL,
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE specializations (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  name            VARCHAR(255) UNIQUE NOT NULL,
  department_id   INT NOT NULL,
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_specialization_department FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE subjects (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  code            VARCHAR(255) UNIQUE NOT NULL,
  specialization_id INT NOT NULL,
  name            VARCHAR(255) NOT NULL,
  description     TEXT,
  credits         INT,
  lecture_hours   INT,
  lab_hours       INT,
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_subject_specialization FOREIGN KEY (specialization_id) REFERENCES specializations(id)
);

CREATE TABLE terms (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  term            VARCHAR(255) UNIQUE NOT NULL,
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE groups (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  group_name      VARCHAR(255) UNIQUE NOT NULL,
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE rooms (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  room            VARCHAR(255) UNIQUE NOT NULL,
  capacity        INT,
  active          SMALLINT DEFAULT 1,     -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

-- =========================
-- OFFERINGS / ENROLLMENTS
-- =========================
CREATE TABLE course_offerings (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  group_id        INT NOT NULL,
  subject_id      INT NOT NULL,
  term_id         INT NOT NULL,
  instructor_id   INT NOT NULL,
  assistant_id    INT NOT NULL,
  room_id         INT,
  generation_id   INT NOT NULL,
  description     VARCHAR(255),
  start_time      TIMESTAMP,   -- use the time only
  end_time        TIMESTAMP,   -- use the time only
  status          INT                      -- 1=planned,2=active,3=completed,4=canceled
  active          SMALLINT DEFAULT 1,      -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_offering_subject    FOREIGN KEY (subject_id)    REFERENCES subjects(id),
  CONSTRAINT fk_offering_group      FOREIGN KEY (group_id)      REFERENCES groups(id),
  CONSTRAINT fk_offering_term       FOREIGN KEY (term_id)       REFERENCES terms(id),
  CONSTRAINT fk_offering_instructor FOREIGN KEY (instructor_id) REFERENCES instructors(id),
  CONSTRAINT fk_offering_generation FOREIGN KEY (generation_id) REFERENCES generations(id),
  CONSTRAINT fk_offering_room       FOREIGN KEY (room_id)       REFERENCES rooms(id),
  CONSTRAINT fk_offering_assistant FOREIGN KEY (assistant_id) REFERENCES instructors(id)
);

CREATE INDEX idx_course_offerings_subject_term_instructor
  ON course_offerings (subject_id, term_id, instructor_id, group_id, generation_id, room_id, assistant_id);

CREATE TABLE enrollments (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  student_id      INT NOT NULL,
  offering_id     INT NOT NULL,
  status          INT,                     -- 1=enrolled,2=dropped,3=completed
  active          SMALLINT DEFAULT 1,      -- <<< smallint
  enrolled_at     TIMESTAMP DEFAULT NOW(),
  dropped_at      TIMESTAMP,               -- was "datetime" -> TIMESTAMP
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW(),
  CONSTRAINT uq_enrollment UNIQUE (student_id, offering_id);
  CONSTRAINT fk_enroll_student   FOREIGN KEY (student_id)  REFERENCES students(id),
  CONSTRAINT fk_enroll_offering  FOREIGN KEY (offering_id) REFERENCES course_offerings(id)
);

CREATE INDEX idx_enrollments_student_offering
  ON enrollments (student_id, offering_id);

-- =========================
-- SESSIONS (REAL CLASSES)
-- =========================
CREATE TABLE sessions (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  offering_id     INT NOT NULL,
  room_id         INT NOT NULL,
  start_datetime  TIMESTAMP NOT NULL,      -- was "datetime"
  end_datetime    TIMESTAMP NOT NULL,      -- was "datetime"
  status          session_status,  -- ('planned','completed','canceled','makeup');
  active          SMALLINT DEFAULT 1,      -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_session_offering FOREIGN KEY (offering_id) REFERENCES course_offerings(id),
  CONSTRAINT fk_session_room     FOREIGN KEY (room_id)     REFERENCES rooms(id)
);

CREATE INDEX idx_sessions_offering_room_start
  ON sessions (offering_id, room_id, start_datetime);

-- =========================
-- DEVICES & BIOMETRICS
-- =========================
-- CREATE TABLE devices (
--   id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--   global_id       VARCHAR(255) UNIQUE NOT NULL,
--   room_id         INT,                     -- nullable for mobile
--   type            device_type,
--   identifier      VARCHAR(255) UNIQUE NOT NULL,
--   auth_key        VARCHAR(255) UNIQUE NOT NULL,
--   last_seen_at    TIMESTAMP,
--   active          SMALLINT DEFAULT 1,      -- <<< smallint
--   created_at      TIMESTAMP DEFAULT NOW(),
--   updated_at      TIMESTAMP DEFAULT NOW(),
--   CONSTRAINT fk_device_room FOREIGN KEY (room_id) REFERENCES rooms(id)
-- );

-- CREATE INDEX idx_devices_room ON devices (room_id);

CREATE TABLE biometric_templates (
  id               INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  student_id       INT,
  embedding        BYTEA,                  -- was "blob" -> BYTEA (use pgvector if needed)
  model            VARCHAR(64),
  dimension        INT,
  -- source_device_id INT,
  active          SMALLINT DEFAULT 1,      -- <<< smallint
  created_at       TIMESTAMP DEFAULT NOW(),
  updated_at       TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_bio_student  FOREIGN KEY (student_id)       REFERENCES students(id),
  -- CONSTRAINT fk_bio_device   FOREIGN KEY (source_device_id) REFERENCES devices(id)
);

-- CREATE INDEX idx_biometric_templates_student_device
--   ON biometric_templates (student_id, source_device_id);

CREATE TABLE verifications (
  id                INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id         VARCHAR(255) UNIQUE NOT NULL,
  -- device_id         INT,
  session_id        INT,
  student_id        INT,
  template_id       INT,
  similarity        NUMERIC(5,4),          -- was decimal(5,4)
  liveness_score    NUMERIC(5,4),
  result            verification_result,
  captured_image_url VARCHAR(1024),
  captured_at       TIMESTAMP DEFAULT NOW(),
  active            SMALLINT DEFAULT 1,      -- <<< smallint
  created_at        TIMESTAMP DEFAULT NOW(),
  updated_at        TIMESTAMP DEFAULT NOW(),
  -- CONSTRAINT fk_verif_device   FOREIGN KEY (device_id)   REFERENCES devices(id),
  CONSTRAINT fk_verif_session  FOREIGN KEY (session_id)  REFERENCES sessions(id),
  CONSTRAINT fk_verif_student  FOREIGN KEY (student_id)  REFERENCES students(id),
  CONSTRAINT fk_verif_template FOREIGN KEY (template_id) REFERENCES biometric_templates(id)
);

CREATE INDEX idx_verifications_multi
  ON verifications (session_id, student_id, template_id, result);

-- =========================
-- ATTENDANCE
-- =========================
CREATE TABLE attendance (
  id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  global_id       VARCHAR(255) UNIQUE NOT NULL,
  session_id      INT NOT NULL,
  student_id      INT NOT NULL,
  status          attendance_status,
  checkin_time    TIMESTAMP,               -- was "datetime"
  -- checkout_time   TIMESTAMP,               -- was "datetime"
  method          attendance_method,
  -- device_id       INT,
  verification_id INT,
  remarks         TEXT,
  active          SMALLINT DEFAULT 1,      -- <<< smallint
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_att_session      FOREIGN KEY (session_id)      REFERENCES sessions(id),
  CONSTRAINT fk_att_student      FOREIGN KEY (student_id)      REFERENCES students(id),
  -- CONSTRAINT fk_att_device       FOREIGN KEY (device_id)       REFERENCES devices(id),
  CONSTRAINT fk_att_verification FOREIGN KEY (verification_id) REFERENCES verifications(id),
  CONSTRAINT uq_att_unique UNIQUE (session_id, student_id)     -- prevent duplicates
);

CREATE INDEX idx_attendance_session_student_device
  ON attendance (session_id, student_id);
