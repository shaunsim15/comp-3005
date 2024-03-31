DROP TRIGGER IF EXISTS paid_sesh_member_achievement ON member_session;
DROP FUNCTION IF EXISTS check_paid_sesh_member_achievement;
DROP TABLE IF EXISTS "admin";
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS session_routine;
DROP TABLE IF EXISTS routine;
DROP TABLE IF EXISTS member_session;
DROP TABLE IF EXISTS "session";
DROP TABLE IF EXISTS trainer;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS member_achievement;
DROP TABLE IF EXISTS achievement;
DROP TABLE IF EXISTS weight_log;
DROP TABLE IF EXISTS member;



CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,   
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    goal_weight NUMERIC(5,2),
    goal_date DATE,
    height NUMERIC(5,2)
);

CREATE TABLE weight_log(
    weight NUMERIC(5,2),
    date DATE,
    member_id INT,
    PRIMARY KEY (member_id, date),
    FOREIGN KEY (member_id) REFERENCES member
        ON DELETE CASCADE
);

CREATE TABLE achievement(
    achievement_id SERIAL PRIMARY KEY,
    name VARCHAR(20)
);

CREATE TABLE member_achievement(
    member_id INT,
    achievement_id INT,
    date DATE,
    PRIMARY KEY (member_id, achievement_id),
    FOREIGN KEY (member_id) REFERENCES member
        ON DELETE SET CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievement
        ON DELETE SET CASCADE
);

CREATE TABLE room(
    room_id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    capacity INT
);


CREATE TABLE trainer(
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE session(
    session_id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    is_group_booking BOOLEAN,
    pricing NUMERIC(8,2) CHECK (pricing > 0),
    room_id INT,
    trainer_id INT,
    FOREIGN KEY (room_id) REFERENCES room
        ON DELETE SET NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainer
        ON DELETE SET NULL
);



CREATE TABLE member_session(
    member_id INT,
    session_id INT,
    has_paid_for BOOLEAN,
    PRIMARY KEY (member_id, session_id),
    FOREIGN KEY (member_id) REFERENCES member
        ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES session
        ON DELETE CASCADE
);

CREATE TABLE routine(
    routine_id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    calories_burnt INT
);

CREATE TABLE session_routine(
    session_id INT,
    routine_id INT,
    routine_count INT,
    PRIMARY KEY (session_id, routine_id),
    FOREIGN KEY (session_id) REFERENCES session
        ON DELETE CASCADE,
    FOREIGN KEY (routine_id) REFERENCES routine
        ON DELETE CASCADE
);

CREATE TABLE schedule(
    trainer_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    PRIMARY KEY (trainer_id, start_time),
    FOREIGN KEY (trainer_id) REFERENCES trainer
        ON DELETE CASCADE
);

CREATE TABLE equipment(
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    last_maintained_date DATE,
    days_in_maintenance_interval INT,
    room_id INT,
    FOREIGN KEY (room_id) REFERENCES room
        ON DELETE SET NULL
);

CREATE TABLE admin(
    admin_id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(20),
    last_name VARCHAR(20)
);

CREATE FUNCTION check_paid_sesh_member_achievement()
returns TRIGGER
language plpgsql
AS
$$
    declare
        paid_member_sesh_count INTEGER;
    begin
        paid_member_sesh_count := ( SELECT COUNT(member_session.session_id) 
            FROM member_session 
            WHERE member_session.member_id = NEW.member_id 
            AND member_session.has_paid_for = TRUE
            );
        IF paid_member_sesh_count = 1 THEN
            INSERT INTO member_achievement VALUES
            (NEW.member_id, 1, CURRENT_DATE);
        ELSIF paid_member_sesh_count = 5 THEN
            INSERT INTO member_achievement VALUES
            (NEW.member_id, 2, CURRENT_DATE);
        ELSIF paid_member_sesh_count = 10 THEN
            INSERT INTO member_achievement VALUES
            (NEW.member_id, 3, CURRENT_DATE);
        END IF;
        RETURN NEW;
    end;
$$;

CREATE TRIGGER paid_sesh_member_achievement
AFTER UPDATE
ON member_session
FOR EACH ROW
EXECUTE PROCEDURE check_paid_sesh_member_achievement();