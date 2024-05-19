# CITS3403-Group-Project

| UWA ID   | Name             | GitHub User Name      |
| -------- | ---------------- | --------------------- |
| 24005494 | Jacob Bennett    | MagMicro              |
| 22974298 | Max Bennett      | Max-Bennett-22974298  |
| 22712171 | Jeremy Boulter   | JeremyBoulter         |
| 24145365 | Jamie Laubbacher | Jamie-sll             |

#Purpose:
The website we have created is a polling website, inspired by the likes of "Would you rather", where users can vote between a set of two options for a given prompt and see what options the majority of other users selected. Because of the user requests requirement, we made a website where users can create polls (create a request) that other users can vote on (service a request), with extra user functionality added along the way for easy navigation and greater user interaction. The website layout consists of a variety of different HTML pages dedicated to one particular view, such as login or creation. For navigation, all webpages share the same template that implements a navigation banner that provides butons to go to particular pages and a search bar feature that allows for users to easy search for polls to vote on based on search requirements and filters. Furthermore, the main page provides links to key pages, and some other pages include url links that further link to other pages they reference. Another note about the views of the website is that there are two distict views, 'logged-in' users & 'anonymous' users. Logged in users get access to features such as poll creation & deletion , comment creation & deletion, leaderboard page and account management (seeing their own posts and performace, being able to modify their data). Anonymous users can only search polls and cannot see comments nor create polls nor see leaderboard. if they attempt to do these things, they are redirected to the login page. New users can create new accounts through our creation page and login through the login page, where their credentials are validated and certain requirements are enforced (such as strong passwords and unique usernames/emails).

As for the user interaction, this is provided via polls comment sections and the ranking page. The user comments allow for logged in users on any given page to write comments and see the comments from others, and allows them to communicate and talk about the given poll. The leaderboard rewards users who are able to make "Good" polls, which i will define in the objectives section. Users can get the accomplishemnt of being the top poll creators on the site, and compare themselves with other users.

#Objective of the website:
As the name SplitDif suggests (based on split the difference), the goal of poll creation is to create polls with the smallest difference between voting options. Polls are ranked according to how indecisive they are when it comes to who voted for what. However, for this idea to be executed, the amount of votes must also be taken into account. A poll with a 40/60 split between 1000 votes is more impressive than a poll of 10 votes with a 50/50 split. Because of this, users are ranked according to our ranking system where we use points. A users points are calculated by (1 - overall difference) * total number of votes. This makes users also consider getting as many votes as possible.
Another ranking system provided is our poll ranking system "Most popular", which ranks polls based on how many votes they have received within a given timeframe (day/week/month). This adds another means of making users attempt to make polls people actually want to vote on, rather than random gibberish.

Set up:
1. Unzip the zip file
2. Create a new python virtual environment
3. Activate the virtual environment
4. Install the packages from requirements.txt using { pip install -r requirements.txt }
5. Set environment variable for secret key using { export FLASK_SECRET_KEY=zyx }
6. Run the web application using { python3 SplitDif.py }

Testing:
To run tests, navigate to the root directory of the project and run the command: { python3 -m unittest tests/run_tests.py }
For controller testing, remove flash messages from controller.py and run the command { python3 -m unittest tests/ControllerTests.py }
