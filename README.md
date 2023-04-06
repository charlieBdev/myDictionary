# myDictionary
#### Video Demo:  <https://www.youtube.com/watch?v=XFjA27s_Lq0>
#### Description: A web app for English language learners that lets them save vocabulary

myDictionary is for English language learners. It acts as a vocabulary journal to help them remember words they encounter in class or everyday life. Users can enter the words any way they like - which may not be 100% accurate - but the language is personalised and therefore hopefully more memorable.

Users can **Register** and **Log In**.

There are various error messages using the apology template/route if the user doesn't enter a username for example or if the password and confirmation don't match.

The password is hashed upon entry into the database.

The database has two tables - one for **users** and one for **words**. Note - there's another table but I'm not sure if that was created automatically by the system so left it there.

All the words get stored in one table. There is a foreign key in the words table (userID), that references the id (PK) field in the users table.

There is a UNIQUE INDEX on username in the users table to ensure no one else can have tha same username.

Once logged in they can see all the words they have added.

A for loop is used with Jinja syntax to populate each row (or word entry) in the table.

To add a word, they click **Add a word**.

Upon adding a word, variables are declared and assigned using request.form.get("").

db.execute("SQL STATEMENT HERE") is then used to INSERT the values into the database.

Users can also **Edit** and **Delete** words (Be careful as there is no confirmation implemented!).

When editing words, db.execute("SQL STATEMENT HERE") is used with UPDATE/SET.

Question marks (?) are used in the SQL statements to prevent SQL injection attacks, which act as placeholders for the values that are 'plugged in' at the end of the line.

When the render_template function is returned, we pass the template we want to use, and add the variables we want to pass as arguments, which can then be refered to in the corresponding template using Jinja syntax.

There is also some Bootstrap on the table and buttons most noticeably.

The templates folder contains the various pages that are plugged into the layout page.

The app.py file contains all the routes and methods (?) that are called when necessary.

The myDictionary.db file contains the database.

Finally, I used a Google Font for the myDictionary writing which is linked to in the layout template.

I used:
**Flask**
**SQLite3**
**HTML**
**CSS**
**Python**
**Bootstrap**
**Jinja**

It was tough to finish and I didn't think I'd get there but I stuck with it and used concepts I'd picked up from Finance and David's lecture on Flask.

Things to improve/add:
- a profile section with option to delete account
- a simple search bar that will navigate directly to that search term in a given dictionary
- stats on usage ie how many words the user has added in total/today
- ensure password are longer, contain a range of characters/symbols, etc

Thank you CS50! It's been a blast!
