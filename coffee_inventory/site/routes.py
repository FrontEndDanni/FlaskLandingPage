from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder = 'site_templates')

"""
Note that in the above code, some arguments are specified when creating the blueprint objects
The first argument, 'site', is the Blueprint's name. 
It's used by Flask's routing mechanism.
The second argument, '__name__, is the Blueprint's import name, which 
Flask uses to locate the Blueprint's resources."""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')  