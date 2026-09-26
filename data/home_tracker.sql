CREATE TABLE IF NOT EXISTS assignments
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    due_date TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS submissions 
(
    id SERIAL PRIMARY KEY,
    telegram_id TEXT,
    assignment_id INT REFERENCES assignments(id) ON DELETE CASCADE,
    submitted_at DATE,
    grade SMALLINT NULL
);