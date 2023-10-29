
### Middelware to navigate authenticated users.
import functools
from flask import session, redirect

# Dashbord authentication middleware
def auth(func):

    @functools.wraps(func)
    def decorated(*args, **kwargs):

        ## Allow access of dashboard to only authenticated users.
        if 'email' not in session:
            return redirect('/login')
        return func(*args, **kwargs)
    
    return decorated


# Guest middleware
def guest(func):

    @functools.wraps(func)
    def decorated(*args, **kwargs):

        ## Allow access of login and registration page to guest users.
        if 'email' in session:
            return redirect('/dashboard')
        return func(*args, **kwargs)
    
    return decorated