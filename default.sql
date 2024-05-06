CREATE TABLE alembic_version (
        version_num VARCHAR(32) NOT NULL,
        CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE IF NOT EXISTS "Polls" (
        "poll_ID" INTEGER NOT NULL,
        "pollAuthor_ID" INTEGER,
        "Option1" VARCHAR,
        "Option2" VARCHAR, tag1 VARCHAR, tag2 VARCHAR, tag3 VARCHAR, date VARCHAR(10), prompt VARCHAR,
        PRIMARY KEY ("poll_ID"),
        FOREIGN KEY("pollAuthor_ID") REFERENCES "Users" ("user_ID")
);
CREATE TABLE IF NOT EXISTS "VotePoll" (
        "user_ID" INTEGER NOT NULL,
        "poll_ID" INTEGER NOT NULL,
        "Vote_opt" INTEGER,
        PRIMARY KEY ("user_ID", "poll_ID"),
        FOREIGN KEY("user_ID") REFERENCES "Users" ("user_ID"),
        FOREIGN KEY("poll_ID") REFERENCES "Polls" ("poll_ID")
);
CREATE TABLE IF NOT EXISTS "Users" (
        "user_ID" INTEGER NOT NULL,
        username VARCHAR,
        email VARCHAR,
        password VARCHAR,
        date VARCHAR(10),
        PRIMARY KEY ("user_ID"),
        UNIQUE (email),
        UNIQUE (username)
);