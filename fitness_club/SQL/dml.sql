-- The unhashed password for each user is written as a comment on each line. Use these to login.
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
('1st Session Paid For'),
('5 Sessions Paid For'),
('10 Sessions Paid For');

-- I'm commenting this out because data in MemberAchievement should be populated by the trigger function when Members complete Achievements. This table should have no initial data.
-- But I'm leaving in some example DML so the TA can see what member_achievement records look like.
-- INSERT INTO member_achievement (member_id, achievement_id, date)
-- VALUES
-- (1, 2, '2024-03-10'),
-- (1, 1, '2024-03-05'),
-- (3, 3, '2024-03-20'),
-- (4, 1, '2024-03-12'),
-- (5, 2, '2024-03-18'),
-- (6, 1, '2024-03-25'),
-- (2, 2, '2024-03-12'),
-- (3, 1, '2024-03-10'),
-- (4, 2, '2024-03-18'),
-- (5, 3, '2024-03-22'),
-- (7, 1, '2024-03-25'),
-- (8, 2, '2024-03-27'),
-- (9, 1, '2024-03-20'),
-- (10, 2, '2024-03-29');

INSERT INTO room (name, capacity)
VALUES
('Cardio Room', 20),
('Weightlifting Area', 15),
('Exercise Studio', 30),
('Tiny Room', 2);

INSERT INTO trainer (first_name, last_name, email, password)
VALUES
('Emily', 'Davis', 'emilyd@gmail.com', '$2b$12$orV99QxNV5sLXJbHVDfxyeCXjvoz8VH047AhEqYNTnHLjIDlySG2O'), -- pass: trainerpass
('David', 'Wilson', 'davidw@gmail.com', '$2b$12$tL3ccEDulB117rDrxBjA1OTSXMsxlGBiC/pmBq.BA1DSiaKdmy6gu'), -- pass: fitness123
('Rachel', 'Miller', 'rachelm@gmail.com', '$2b$12$s6vgQdc8am8wdXzCv2LQp.93TidIsI.h/vIXdQK/aQ5ZuS/sqriXy'), -- pass: trainer123
('Kevin', 'Clark', 'kevinc@gmail.com', '$2b$12$n27PMi9llts5Uo2MLPERFuVH2/NQpjK6X/DPoain/T5Q7fTRZTPLi'), -- pass: fitnessking
('Jessica', 'Brown', 'jessicab@gmail.com', '$2b$12$dVRJweWoq/NolRxeMZDIiOJkOwUcoodsovdw6NlV8TQJvigwgZoe.'), -- pass: trainer456
('Michael', 'Taylor', 'michaelt@gmail.com', '$2b$12$J0WpbvMaefcJRmGMUCVvx.JX/VQJ66ICfOHOtrVAQPC73b3Ii4Ppy'), -- pass: trainer789
('Samantha', 'Evans', 'samanthae@gmail.com', '$2b$12$U1fHJRlQRCLDDtTFUpHe7ePquBczlgJLJ23Zi5eFxRg2CXWrqecZe'), -- pass: gymlover
('Ryan','Garcia', 'ryang@gmail.com', '$2b$12$q35D3KA1Ig4D3uLoX17nYulOcNMu20uBrxr2jDl/DFiwonwM1KGWe'); -- pass: fitnessexpert


INSERT INTO session (name, start_time, end_time, is_group_booking, pricing, room_id, trainer_id)
VALUES
('Session 1', '2024-03-16 08:00:00', '2024-03-16 09:00:00', true, 15.00, 3, 1),
('Session 2', '2024-03-16 17:00:00', '2024-03-16 18:00:00', true, 20.00, 2, 2),
('Session 3', '2024-03-16 18:30:00', '2024-03-16 19:30:00', true, 15.00, 1, 3),
('Session 4', '2024-03-16 10:00:00', '2024-03-16 11:00:00', true, 18.00, 3, 4),
('Session 5', '2024-03-16 18:00:00', '2024-03-16 19:00:00', true, 15.00, 3, 5),
('Session 6', '2024-03-16 09:00:00', '2024-03-16 10:00:00', false, 15.00, 3, 1),
('Session 7', '2024-03-16 18:00:00', '2024-03-16 19:00:00', false, 20.00, 2, 2),
('Session 8', '2024-03-27 19:30:00', '2024-03-27 20:30:00', false, 20.00, 3, 3),
('Session 9', '2024-03-28 19:30:00', '2024-03-28 20:30:00', false, 20.00, 3, 3);



INSERT INTO member_session (member_id, session_id, has_paid_for)
VALUES
(1, 1, false),
(1, 3, false),
(1, 4, false),
(1, 7, false),
(2, 2, true),
(3, 3, false),
(1, 8, false),
(1, 9, false);

-- These dummy updates are just to cause the trigger to fire, since it doesn't fire on inserts; only on updates
UPDATE member_session
SET has_paid_for = true
WHERE has_paid_for = true;

-- Note that each calories_burnt figure is for one unit of that routine. E.g. 200 calories burnt after doing 1 pushup.
-- calories_burnt isn't really used in our app currently, but it would be cool in future to report data on calories burnt in the MemberDashboard
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
(5, 5, 1),
(8, 1, 1), 
(8, 2, 1),
(8, 3, 1),
(8, 4, 2),
(8, 5, 2),
(9, 1, 1), 
(9, 2, 1),
(9, 3, 1),
(9, 4, 2),
(9, 5, 2);

INSERT INTO schedule (trainer_id, start_time, end_time)
VALUES
(1, '2024-03-16 08:00:00', '2024-03-16 12:00:00'),
(1, '2024-03-17 08:00:00', '2024-03-17 12:00:00'),
(1, '2024-03-18 08:00:00', '2024-03-18 12:00:00'),
(1, '2024-03-19 08:00:00', '2024-03-19 12:00:00'),
(1, '2024-03-20 08:00:00', '2024-03-20 12:00:00'),
(1, '2024-03-21 08:00:00', '2024-03-21 16:00:00'),
(1, '2024-03-22 08:00:00', '2024-03-22 14:00:00'),
(2, '2024-03-16 14:00:00', '2024-03-16 20:00:00'),
(2, '2024-03-17 14:00:00', '2024-03-17 20:00:00'),
(2, '2024-03-18 14:00:00', '2024-03-18 20:00:00'),
(2, '2024-03-19 14:00:00', '2024-03-19 20:00:00'),
(2, '2024-03-20 14:00:00', '2024-03-20 20:00:00'),
(2, '2024-03-21 14:00:00', '2024-03-21 20:00:00'),
(2, '2024-03-22 14:00:00', '2024-03-22 20:00:00'),
(3, '2024-03-16 08:00:00', '2024-03-16 12:00:00'),
(3, '2024-03-16 13:00:00', '2024-03-16 17:00:00'),
(3, '2024-03-16 18:00:00', '2024-03-16 22:00:00'),
(3, '2024-03-27 18:00:00', '2024-03-27 22:00:00'),
(3, '2024-03-28 18:00:00', '2024-03-28 22:00:00'),
(4, '2024-03-16 09:00:00', '2024-03-16 13:00:00'),
(4, '2024-03-16 14:00:00', '2024-03-16 18:00:00'),
(4, '2024-03-16 19:00:00', '2024-03-16 23:00:00'),
(4, '2024-03-17 00:00:00', '2024-12-31 23:59:59'), -- Make Kevin Clark availabile all year round, for ease of testing
(5, '2024-03-16 10:00:00', '2024-03-16 14:00:00'),
(5, '2024-03-16 15:00:00', '2024-03-16 19:00:00'),
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
('Rowing Machine', '2024-02-15', 60, 2),
('Stationary Bike', '2024-03-05', 45, 3);



INSERT INTO admin (email, password, first_name, last_name)
VALUES
('evan@gmail.com', '$2b$12$LfbIwn6pcv0LTiRfeP4Pm.Bq7XO2K1seQGo08s1o7S3Co1pK6czHi', 'Evan', 'Lastnameone'), -- pass: adminpass1
('sean@gmail.com', '$2b$12$PQu093G4ZQ95pmQg4n7VL.Vh8dJ9Nq.YI2GNA2f/fjlpzSvRloju.', 'Sean', 'Lastnametwo'), -- pass: adminpass2
('david@gmail.com', '$2b$12$vmBtHElfhSTDYz4PLOOZbufbJrcBUU7di6onn7mZ2aA4m7E40E5L.', 'David', 'Lastnamethree'), -- pass: adminpass3
('precious@gmail.com', '$2b$12$r7hB0hhILq5FjLFxLO99iuyu0NEjZoCEyLH3XqL1oucyCESBBF8CK', 'Precious', 'Four'); -- pass: adminpass4
