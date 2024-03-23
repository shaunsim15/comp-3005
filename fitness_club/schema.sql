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
        ON DELETE SET NULL,
    FOREIGN KEY (achievement_id) REFERENCES achievement
        ON DELETE SET NULL
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
    is_room_confirmed BOOLEAN,
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
        ON DELETE SET NULL,
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

INSERT INTO member (first_name, last_name, email, password, goal_weight, goal_date, height)
VALUES
('John', 'Doe', 'johndoe@gmail.com', '$2b$12$HKOaYFobfQYbRyaMvLVcweG38Y1s3X/Rcr3bIZbvuyDLSSAIuWmAS', 70.5, '2024-06-01', 175), -- 'password123'
('Jane', 'Smith', 'janesmith@gmail.com', '$2b$12$fj/qNzLftQ.2GvgwT8PQBuK9JJ04og6IaZRYt2zGiLZf/mutL46wq', 65.2, '2024-07-15', 162), -- 'letmein'
('Michael', 'Johnson', 'michaelj@gmail.com', '$2b$12$HPmUjWnoKCooC.xs6e8IsuEM7bKANdmOUbCG6HN.ACK/cD0.hMlEu', 80.0, '2024-09-30', 180), -- 'abc123'
('Emily', 'Brown', 'emilybrown@gmail.com', '$2b$12$8vnF4xKBLQ75dUZDXRFhBei5q7eV6KKBCFxbeOUNKFAwK8iP8/5Hu', 60.0, '2024-08-20', 160), -- 'ilovefitness'
('Daniel', 'Williams', 'danielw@gmail.com', '$2b$12$ap9Cvz8szIaEuQBRjaBg/.m/i.OG2JgdyFwSTD3tbRr6hB7iNycnu', 75.8, '2024-10-10', 178), -- 'workout123'
('Jessica', 'Davis', 'jessicad@gmail.com', '$2b$12$aNXozG7V0w2n3mVk34m3v.PmmeO6bGiDRXOkOHrdCwuAOGKCP1uoS', 55.0, '2024-07-01', 155), -- 'fitnessgirl'
('Sarah', 'Wilson', 'sarahwilson@gmail.com', '$2b$12$fayHn0DDNFLjhRHyKmtG6.cQTj3boImZYk3WhstqvPTipHaj1AyWm', 62.5, '2024-08-10', 165), -- 'strongwoman'
('Matthew', 'Taylor', 'matthewtaylor@gmail.com', '$2b$12$LfJ68MJsQLBAmnJ0VMcsK.c7ydLHeG5fcD4KXBu0i5EWlVkcqQ8Nq', 72.3, '2024-09-20', 180), -- 'fitnessfreak'
('Emma', 'Anderson', 'emmaa@gmail.com', '$2b$12$FB2MsFr0Ob1kT0rbcjj8AeSE4ZofpJrvRrG/ndfhskLIIJKCN3Yz.', 55.8, '2024-07-05', 158), -- 'healthy123'
('Christopher', 'Martinez', 'chrism@gmail.com', '$2b$12$e4KyZBMIMvV7IIvLQ.PG3.4gf7RT40tbqErykI4NNZmBqqtrMGZoC', 68.0, '2024-10-15', 175); -- 'fitlife'


INSERT INTO weight_log (weight, date, member_id)
VALUES
(75.2, '2024-03-01', 1),
(73.5, '2024-03-15', 1),
(68.0, '2024-03-01', 2),
(67.5, '2024-03-15', 2),
(85.0, '2024-03-01', 3),
(83.5, '2024-03-15', 3),
(70.0, '2024-03-15', 4),
(62.0, '2024-03-15', 5),
(70.5, '2024-03-15', 6),
(61.8, '2024-03-15', 7),
(75.0, '2024-03-15', 8),
(54.5, '2024-03-15', 9),
(67.2, '2024-03-15', 10);

INSERT INTO achievement (name)
VALUES
('1st Session Done'),
('10 Sessions Done'),
('25 Sessions Done');

INSERT INTO member_achievement (member_id, achievement_id, date)
VALUES
(1, 2, '2024-03-10'),
(1, 1, '2024-03-05'),
(3, 3, '2024-03-20'),
(4, 1, '2024-03-12'),
(5, 2, '2024-03-18'),
(6, 1, '2024-03-25'),
(2, 2, '2024-03-12'),
(3, 1, '2024-03-10'),
(4, 2, '2024-03-18'),
(5, 3, '2024-03-22'),
(7, 1, '2024-03-25'),
(8, 2, '2024-03-27'),
(9, 1, '2024-03-20'),
(10, 2, '2024-03-29');

INSERT INTO room (name, capacity)
VALUES
('Cardio Room', 20),
('Weightlifting Area', 15),
('Exercise Studio', 30);

INSERT INTO trainer (first_name, last_name, email, password)
VALUES
('Emily', 'Davis', 'emilyd@gmail.com', 'trainerpass'),
('David', 'Wilson', 'davidw@gmail.com', 'fitness123'),
('Rachel', 'Miller', 'rachelm@gmail.com', 'trainer123'),
('Kevin', 'Clark', 'kevinc@gmail.com', 'fitnessking'),
('Jessica', 'Brown', 'jessicab@gmail.com', 'trainer456'),
('Michael', 'Taylor', 'michaelt@gmail.com', 'fitness789'),
('Samantha', 'Evans', 'samanthae@gmail.com', 'gymlover'),
('Ryan','Garcia', 'ryang@gmail.com', 'fitnessexpert');

INSERT INTO session (name, start_time, end_time, is_group_booking, pricing, is_room_confirmed, room_id, trainer_id)
VALUES
('Session 1', '2024-03-16 08:00:00', '2024-03-16 09:00:00', true, 15.00, true, 3, 1),
('Session 2', '2024-03-16 17:00:00', '2024-03-16 18:00:00', true, 20.00, true, 2, 2),
('Session 3', '2024-03-16 18:30:00', '2024-03-16 19:30:00', true, 15.00, true, 1, 3),
('Session 4', '2024-03-16 10:00:00', '2024-03-16 11:00:00', true, 18.00, true, 3, 4),
('Session 5', '2024-03-16 18:00:00', '2024-03-16 19:00:00', true, 15.00, true, 3, 5);


INSERT INTO member_session (member_id, session_id, has_paid_for)
VALUES
(1, 1, true),
(2, 2, true),
(3, 3, false);


INSERT INTO routine (name, calories_burnt)
VALUES
('Push Ups', 200),
('Plank', 300),
('Sit Ups', 150),
('Squats', 250),
('Jumping Jacks', 200),
('Burpees', 350),
('Mountain Climbers', 300),
('Lunges', 220),
('Bicycle Crunches', 180),
('Russian Twists', 170),
('Deadlifts', 280),
('Pull-Ups', 320),
('Dumbbell Rows', 240),
('Leg Press', 290),
('Chest Press', 260),
('Shoulder Press', 230),
('Leg Curls', 270),
('Tricep Dips', 210),
('Bicep Curls', 200),
('Calf Raises', 180);

-- Inserting data into the session_routine table
INSERT INTO session_routine (session_id, routine_id, routine_count)
VALUES
(1, 1, 1), 
(1, 2, 1),
(1, 3, 1),
(1, 4, 2),
(1, 5, 2),
(2, 6, 2), 
(2, 7, 2),
(2, 8, 3),
(2, 9, 2),
(2, 10, 1),
(3, 11, 3),
(3, 12, 2),
(3, 13, 2),
(3, 14, 1),
(3, 15, 1),
(4, 16, 1),
(4, 17, 2),
(4, 18, 1),
(4, 19, 1),
(4, 20, 2),
(5, 1, 2),
(5, 2, 1),
(5, 3, 2),
(5, 4, 2),
(5, 5, 1);

INSERT INTO schedule (trainer_id, start_time, end_time)
VALUES
(1, '2024-03-16 08:00:00', '2024-03-16 12:00:00'),
(1, '2024-03-17 08:00:00', '2024-03-16 12:00:00'),
(1, '2024-03-18 08:00:00', '2024-03-16 12:00:00'),
(1, '2024-03-19 08:00:00', '2024-03-16 12:00:00'),
(1, '2024-03-20 08:00:00', '2024-03-16 12:00:00'),
(1, '2024-03-21 08:00:00', '2024-03-16 16:00:00'),
(1, '2024-03-22 08:00:00', '2024-03-16 14:00:00'),
(2, '2024-03-16 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-17 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-18 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-19 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-20 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-21 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-22 14:00:00', '2024-03-16 20:00:00'),
(3, '2024-03-16 08:00:00', '2024-03-16 12:00:00'),
(3, '2024-03-16 13:00:00', '2024-03-16 17:00:00'),
(3, '2024-03-16 18:00:00', '2024-03-16 22:00:00'),
(4, '2024-03-16 09:00:00', '2024-03-16 13:00:00'),
(4, '2024-03-16 14:00:00', '2024-03-16 18:00:00'),
(4, '2024-03-16 19:00:00', '2024-03-16 23:00:00'),
(5, '2024-03-16 10:00:00', '2024-03-16 14:00:00'),
(5, '2024-03-16 15:00:00', '2024-03-16 19:00:00'),
(5, '2024-03-16 20:00:00', '2024-03-16 00:00:00'),
(6, '2024-03-16 11:00:00', '2024-03-16 15:00:00'),
(6, '2024-03-16 16:00:00', '2024-03-16 20:00:00'),
(6, '2024-03-16 21:00:00', '2024-03-17 01:00:00'),
(7, '2024-03-16 12:00:00', '2024-03-16 16:00:00'),
(7, '2024-03-16 17:00:00', '2024-03-16 21:00:00'),
(7, '2024-03-16 22:00:00', '2024-03-17 02:00:00'),
(8, '2024-03-16 13:00:00', '2024-03-16 17:00:00'),
(8, '2024-03-16 18:00:00', '2024-03-16 22:00:00'),
(8, '2024-03-16 23:00:00', '2024-03-17 03:00:00');


INSERT INTO equipment (name, last_maintained_date, days_in_maintenance_interval, room_id)
VALUES
('Treadmill', '2024-03-01', 30, 1),
('Dumbbells', '2024-02-15', 60, 2),
('Yoga Mats', '2024-03-05', 45, 3);



INSERT INTO admin (email, password, first_name, last_name)
VALUES
('evan@gmail.com', 'adminpass1', 'Evan', 'Lastnameone'),
('sean@gmail.com', 'adminpass2', 'Sean', 'Lastnametwo'),
('david@gmail.com', 'adminpass3', 'David', 'Lastnamethree'),
('precious@gmail.com', 'adminpass4', 'Precious', 'Four');
