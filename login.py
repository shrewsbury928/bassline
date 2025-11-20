import hashlib
import sqlite3 as sql
import time
import string
import os

# Use an absolute path for the database file so it opens regardless
# of the current working directory when the app is launched.
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bassline.db'))
db = sql.connect(DB_PATH)
c = db.cursor() #cursor

#c.execute('DROP TABLE IF EXISTS profiles')

c.execute('''
CREATE TABLE IF NOT EXISTS profiles (
    userID INTEGER PRIMARY KEY NOT NULL,
    Username VARCHAR,
    Email VARCHAR,
    Password VARCHAR(255),
    Attempts INTEGER DEFAULT 0,
    Lockout_Date REAL
    )
''')

#function to determine whether username or email is present
def validate(username, email):
    #check if email exists
    c.execute("SELECT userID FROM profiles WHERE email = ?", (email,))
    email_check = c.fetchone()
    if email_check: #if a value is present
        return False

    #check if username exists
    c.execute("SELECT userID FROM profiles WHERE username = ?", (username,))
    username_check = c.fetchone()
    if username_check: #if a value is present
        return False

    return True

#function to make sure password is okay then add user to database  
def register(userInput, emailInput, passwordInput):    
    valid = validate(userInput, emailInput)

    if valid:
        error = []
        if not len(passwordInput) >= 8:
            error.append('Password must be at least 8 characters')
        if not any(char.isdigit() for char in passwordInput):
            error.append( 'Password must contain at least 1 number')
        if not any(char in string.punctuation for char in passwordInput):
            error.append('Password must contain at least 1 punctuation')

        if error: #if error cotnains a value
            #print(error)
            return error
        else:
            hashed = hashlib.sha256(passwordInput.encode('utf8')).digest()
            c.execute('INSERT INTO profiles (Username, Email, Password, Attempts, Lockout_Date) VALUES(?,?,?,?,?)', (userInput, emailInput, hashed, 0, None))
            db.commit()
            #print("done")
            return True
    else:
        #print('Username or email exists already')
        return False


def login(userInput, emailInput, passwordInput):
    c.execute('SELECT Password, Attempts, Lockout_Date FROM profiles WHERE Username = ? AND Email = ?', 
              (userInput, emailInput))
    stored = c.fetchone()
    
    if not stored:
        return 'No such username or email found'
    
    stored_pass, attempts, lockout_date = stored
    
    # Check and handle lockout
    if attempts >= 5:
        if lockout_date and time.time() - lockout_date < 3600:
            time_remaining = round(3600 - (time.time() - lockout_date), 2)
            return f'Application Locked, wait {time_remaining} seconds'
        # Reset after cooldown
        attempts = 0
        c.execute('UPDATE profiles SET Attempts = 0, Lockout_Date = NULL WHERE Username = ? AND Email = ?', 
                  (userInput, emailInput))
        db.commit()
    
    # Verify password
    hashed_input = hashlib.sha256(passwordInput.encode('utf8')).digest()
    
    if hashed_input == stored_pass:
        # Successful login - reset attempts
        c.execute('UPDATE profiles SET Attempts = 0, Lockout_Date = NULL WHERE Username = ? AND Email = ?', 
                  (userInput, emailInput))
        db.commit()
        return True
    
    # Failed login - increment attempts
    attempts += 1
    lockout_date = time.time() if attempts >= 5 else None
    c.execute('UPDATE profiles SET Attempts = ?, Lockout_Date = ? WHERE Username = ? AND Email = ?', 
              (attempts, lockout_date, userInput, emailInput))
    db.commit()
    
    return 'Application Locked' if attempts >= 5 else 'Incorrect username/password'
    