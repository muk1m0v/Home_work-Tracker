CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    full_name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS assignments
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    due_date TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS submissions 
(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    assignment_id INT REFERENCES assignments(id) ON DELETE CASCADE,
    submitted_at DATE,
    grade SMALLINT NULL
);