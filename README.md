<p align="center"><img src="https://raw.githubusercontent.com/pawanpaudel93/motion-planning-dashboard/master/src/assets/logo.png?token=AC2JVREHJQGDA6LJWPCGVVDAHJ53I" alt="original" width="250" height="250"></p>

<h1 align="center">Welcome to Motion Planning Dashboard</h1>

It is a Django Vue Dashboard for the Udacity Motion Planning Simulation. 

## Features
- Each simulation done in the Unity simulator is named session and dashboard shows a list of all sessions.
- Live movement of the quadcopter showing on the Plotlyjs Heatmap.
- Showing start and goal position of simulation on the Plotlyjs Heatmap.
- Showing the actual map of the simulated environment with the quadcopter movement path between start and goal coordinates.
- Timeseries graph of the Local Position and Local Velocity with Global Position on the tooltip of the data generated.
- Data table of Local Position, Local Velocity, Global Velocity, Global Position.

## Local Installation
- Clone the repository
`git clone https://github.com/pawanpaudel93/motion-planning-dashboard.git`
- Rename `.env-example` to .env and modify the values as you like and keeping the same value for development is okay.
- Install pipenv from [pipenv repo](https://github.com/pypa/pipenv) and create 
a virtual environment and install django and django dependencies with it from the Pipfile.
- And `npm install` to install all the vue dependencies from package.json
- Run `python manage.py makemigrations && python manage.py migrate` to make and migrate the migrations to PostgreSQL database.

### Local Development
- Then run `python manage.py runserver` to run the django development server.
- In the next terminal tab or command prompt run `npm run serve` to compile and hot-reload for development. The vuejs will run at `localhost:8080` or `127.0.0.1:8080`.
- Now you can access the development server at `localhost:8000` or `127.0.0.1:8000` to view motion planning dashboard served through django consumed using django-webpack-loader.

### Local Deployment
- Run `npm run build` to build the vue app and Then run `python manage.py runserver` to run the django development server.
- Now you can access the development server at `localhost:8000` or `127.0.0.1:8000` to view the motion planning dashboard.

## Motion Planning Code Modification
You have to import MyDrone from drone.py and inherit from MyDrone Class instead of Drone Class from udacidrone. The MyDrone class inherits itself from Drone Class of Udacidrone and it performs the session creation and updating the session with the movement data, local velocity, local position, global position and global home. And the Motion Planning Dashboard visualizes and shows the data of the simulation.

Follow this steps to modify your code.
1. Inherit MyDrone from drone.py instead of Drone from udacidrone.
2. Modify the first line of __init__ method as
```python
# target_altitude and safety_distance can be some numbers or variable in your code so replace it with some numbers or variable
super().__init__(connection, target_altitude, safety_distance)
```
3. Set the property north_offset and east_offset with their respective values where they are generated.
```python
self.north_offset = north_offset
self.east_offset = east_offset
```
4. Paste the line to the end of method waypoint_transition(self)
```python
class waypoint_transition(self):
	# your default lines
	self.session.send_movement([self.target_position[0] - self.north_offset, self.target_position[1] - self.east_offset])
```
5. Paste this line once you get the values for (graph_start, graph_goal) or (grid_start, grid_goal) in your code.
```python
# names may vary so you may have different names for it.
self.session.update_session(grid_start, grid_goal)
```
6. Paste this line at the end of method landing_transition(self)
```python
class landing_transition(self):
	# your default lines
	self.session.end_session()
```

## Performing the simulation
- Start your django server with `python manage.py runserver`
- Then you can run your simulation and view your dashboard meanwhile running the simulation.

## Heroku Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/pawanpaudel93/motion-planning-dashboard/tree/master)

OR

You can use this commands for deployment or use the heroku website for this purpose. For heroku deployment run the following commands after logging to heroku on terminal after installing heroku cli and logging to heroku using command `heroku login`.

Check heroku cli install guide for installation [Heroku cli Install guide](https://devcenter.heroku.com/articles/heroku-cli)

Change the heroku app name as per your wish as I have selected motion-planning-dashboard-demo for this demo purpose.
```bash
heroku apps:create motion-planning-dashboard-demo
heroku buildpacks:add --index 2 heroku/python
heroku buildpacks:add --index 1 heroku/nodejs
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set VUE_APP_BASEURL=heroku web app URL from first command without http/https
heroku config:set DJANGO_SECRET_KEY=your secret key # secret key without space or with space enclosed with inverted commas
heroku config:set DJANGO_DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com
git push heroku master
```
After this steps you can access the deployed demo app at URL which you get from the first command.(Mine is deployed at [https://motion-planning-dashboard.herokuapp.com](https://motion-planning-dashboard.herokuapp.com))


## Author

👤 **Pawan Paudel**

* Github: [@pawanpaudel93](https://github.com/pawanpaudel93)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/pawanpaudel93/motion-planning-dashboard/issues). 

## Show your support

Give a ⭐️ if this project helped you!

Copyright © 2021 [Pawan Paudel](https://github.com/pawanpaudel93).<br />
