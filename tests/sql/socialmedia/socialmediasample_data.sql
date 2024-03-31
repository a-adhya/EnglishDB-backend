INSERT INTO users (username, fullname, email, filename, password) VALUES
('bigshu22', 'Angshu Adhya', 'aadhya@umich.edu', 'bigshu22_b61d75f6c4ce49a2.jpg', ';4J<+B#0)g)I'),
('clafrankie', 'Chris Lafrankie', 'clafrankie@umich.edu', 'clafrankie_2c62808bc8e24e3d.jpg', 'helloworld'),
('jtdiaz', 'Jared Diax', 'jtdiaz@umich.edu', 'jtdiaz_269321cb255a2175.jpg', 'SA,lZr(HXb5r');

INSERT INTO posts (filename, owner) VALUES
('post1_bigshu22.jpg', 'bigshu22'),
('post2_clafrankie.jpg', 'clafrankie'),
('post3_jtdiaz.jpg', 'jtdiaz');

INSERT INTO following (username1, username2) VALUES
('bigshu22', 'clafrankie'),
('clafrankie', 'jtdiaz'),
('jtdiaz', 'bigshu22'),
('bigshu22', 'jtdiaz'),
('clafrankie', 'bigshu22');

INSERT INTO comments (owner, postid, text) VALUES
('clafrankie', 1, 'Awesome post!'),
('jtdiaz', 2, 'Really insightful'),
('bigshu22', 3, 'Loved this!'),
('clafrankie', 1, 'Great job'),
('jtdiaz', 2, 'Fantastic work!');

INSERT INTO likes (owner, postid) VALUES
('jtdiaz', 1),
('bigshu22', 2),
('clafrankie', 3),
('jtdiaz', 1),
('bigshu22', 2);

