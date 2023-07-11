# python-flask-base-webapp

Project web base that include: auth, connection DB (mysql), SMTP and templates.

### Instruction

#### mac/linux
$ source venv/bin/activate

#### windows
\venv\Scripts\activate

#### Install lib required
python -m pip install --upgrade pip

python -m pip install -r requirements.txt

#### Run app
$ flask run

http://127.0.0.1:8000/auth/register

#### DDL
CREATE TABLE `user` (
`user_id` int NOT NULL AUTO_INCREMENT,
`username` varchar(100) NOT NULL,
`password` varchar(255) NOT NULL,
`key_pwd` varchar(205) DEFAULT NULL,
`salt` varchar(255) DEFAULT NULL,
PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
