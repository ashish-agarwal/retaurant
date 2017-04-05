# Restaurant Menu Project

The goal of this project is to create restaurants menus.

A user of this project can add, edit, and delete his menu items belonging to a particular restaurant.  

Authentication is handled by Google OAuth.  User can only edit or delete items they create.

# Prerequisites
Requires Python, pip, and git.

# How to Install
To download and install this program, you will need git installed.

At the command line, enter:
```
git clone https://github.com/ashish-agarwal/restaurant-webapp.git
```

# How to Use Google Authentication Services
You need to supply a client_secret.json file. You can create an application to use
Google's OAuth service at https://console.developers.google.com. 

After creating and downloading your client_secret.json file, move it to the root directory of project so it is accessible to the Item Catalog application.

# How to Use Facebook Authentication Services
You need to supply a fb_config.json file. You can create an application to use
Facebook's OAuth service at https://developer.facebook.com. 

After creating the app, Copy the app_id and app_secret in fb_config.json.


# How to Initialize Database and Load Initial Categories
To initialize the SQLite database (create empty tables) enter
```
python db/database_setup.py
```

To load some restaurants with menus enter
```
python lotsofmenu.py
```

# Starting Application
To start the application enter:
```
python startup.py
```

Then bring up a browser and point it to localhost:5000.