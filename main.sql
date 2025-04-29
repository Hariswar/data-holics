CREATE TABLE leaguify_sport (
    sportName VARCHAR(32) NOT NULL,
    sportID INT PRIMARY KEY,
    individualSport BOOLEAN
);

CREATE TABLE leaguify_team (
    teamID INT PRIMARY KEY,
    teamName VARCHAR(62) NOT NULL,
    sportID INT,
    FOREIGN KEY (sportID) REFERENCES leaguify_sport(sportID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE leaguify_league (
    leagueID INT PRIMARY KEY,
    dateCreated DATE NOT NULL,
    leagueName VARCHAR(32) NOT NULL
);

CREATE TABLE leaguify_player (
    playerID INT PRIMARY KEY,
    emailAddress VARCHAR(64) NOT NULL,
    firstName VARCHAR(32) NOT NULL,
    middleName VARCHAR(32),
    lastName VARCHAR(32) NOT NULL,
    teamID INT,
    FOREIGN KEY (teamID) REFERENCES leaguify_team(teamID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE leaguify_social_media (
    playerID INT,
    userName VARCHAR(32) NOT NULL,
    type VARCHAR(32) NOT NULL,
    FOREIGN KEY (playerID) REFERENCES leaguify_player(playerID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE leaguify_team_social_media (
    playerID INT,
    userName VARCHAR(32) NOT NULL,
    type VARCHAR(32) NOT NULL,
    FOREIGN KEY (playerID) REFERENCES leaguify_player(playerID) ON DELETE CASCADE ON UPDATE CASCADE
); 

CREATE TABLE leaguify_game (
    gameID INT PRIMARY KEY,
    winnerID INT,
    leagueID INT,
    sportID INT,
    description TEXT,
    FOREIGN KEY (winnerID) REFERENCES leaguify_team(teamID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (leagueID) REFERENCES leaguify_league(leagueID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (sportID) REFERENCES leaguify_sport(sportID) ON DELETE CASCADE ON UPDATE CASCADE
); 

CREATE TABLE leaguify_plays (
    leagueID INT, 
    teamID INT,
    gameID INT,
    FOREIGN KEY (leagueID) REFERENCES leaguify_league(leagueID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (teamID) REFERENCES leaguify_team(teamID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (gameID) REFERENCES leaguify_game(gameID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE leaguify_sport_stats (
    teamID INT,
    score INT NOT NULL,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    draws INT DEFAULT 0,
    leagueID INT,
    sportID INT,
    sportStatID INT PRIMARY KEY,
    elo FLOAT,
    gamesPlayed INT,
    winPercent FLOAT,
    FOREIGN KEY (teamID) REFERENCES leaguify_team(teamID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (leagueID) REFERENCES leaguify_league(leagueID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (sportID) REFERENCES leaguify_sport(sportID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE leaguify_scored_sport (
    rootStatsID INT,
    scoreFor INT NOT NULL,
    avgScore FLOAT NOT NULL,
    FOREIGN KEY (rootStatsID) REFERENCES leaguify_sport_stats(sportStatID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO leaguify_sport 
values ('baseball', 0, FALSE),
('football', 1, FALSE),
('ice hockey', 2, FALSE),
('table tennis', 3, TRUE),
('tennis', 4, TRUE),
('cricket', 5, FALSE),
('basketball', 6, FALSE);