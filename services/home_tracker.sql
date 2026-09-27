CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    telegram_id TEXT UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    full_name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS assignments
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    due_date DATE
);

CREATE TABLE IF NOT EXISTS submissions
(
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    assignment_id BIGINT REFERENCES assignments(id) ON DELETE CASCADE,
    submitted_at TIMESTAMP DEFAULT now(),
    grade SMALLINT NULL CHECK(grade >= 1 and grade <= 100),
    UNIQUE(user_id, assignment_id)
);
