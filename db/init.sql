USE quiz_db;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;


-- =========================
-- テーブル作成（存在しなければ）
-- =========================

CREATE TABLE IF NOT EXISTS quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    type VARCHAR(20) NOT NULL,
    choice_a TEXT,
    choice_b TEXT,
    choice_c TEXT,
    choice_d TEXT,
    correct VARCHAR(1) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    score INT NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- =========================
-- 初期データリセット
-- =========================

DELETE FROM quizzes;
DELETE FROM scores;

-- AUTO_INCREMENT を戻したい場合（任意）
ALTER TABLE quizzes AUTO_INCREMENT = 1;
ALTER TABLE scores AUTO_INCREMENT = 1;

-- =========================
-- 初期クイズデータ
-- =========================

INSERT INTO quizzes
(question, type, choice_a, choice_b, choice_c, choice_d, correct)
VALUES
('「座右の銘」は英語で何という？', 'choice', 'アンセム', 'スローガン', 'ブーム', 'モットー', 'D'),
('サハラ砂漠の「サハラ」は日本語で何？', 'choice', '太陽', 'オアシス', '砂漠', '乾燥', 'C'),
('靴の「ローファー」には英語でどんな意味がある？', 'choice', '怠け者', '働き者', '幸せ者', '大金持ち', 'A'),
('ことわざの「急がば回れ」の語源となった場所はどこ？', 'choice', '富士山', '清水寺', '厳島神社', '琵琶湖', 'D'),
('学校で給食を一番に食べるのが仕事なのは誰？', 'choice', '校長', '教頭', '保健室の先生', '配膳係の人', 'A'),
('視力検査で使用されるCの形をしたものの名前は？', 'choice', 'Cマーク', '視力マーク', 'サークルC', 'ランドルト環', 'D'),
('富士山は標高何m？。', 'choice', '3333', '3776', '3778', '3770', 'B');
