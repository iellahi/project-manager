# Project Manager
#### Video Demo: [Youtube Video] (https://youtu.be/-kIP9Tb1wtc)
#### Description: Final Project
Project manager is a basic flask web application that allows you to add projects, view them in detail and make changes whenever you want.

Once you log in, the projects page shows you a list of current projects. Here you can choose to create a new project which returns the editor page where you can add a title, summary, todo list, and even write down another username to allow him to view and make changes to the project. If you choose the option to view a current project, it takes you to editor again but all the changes you made are prefilled. You can reset everything to original values, save it to make changes, or mark complete or abandon to show that this project is ended.

Once a project is finished, you can press the complete button, or abandon if you are leaving it. The project will then appear in the history page; a green title for completed and a red title for abandoned.

At first, I created only options to login or register on the first page, however to make it more attractive, I chose to make a new column to display information about the website, so that users would be more attracted. I chose a simple light color scheme hoping to keep it simple and user friendly. In the editor view, I debated on using the input tag or textarea. Eventually, I settled on textarea since it would be possible to have pre-existing text when you wanted to edit a current projects. I also created two separate editor templates for creating a new project or editing a new one as I could not find the solution to making it work as one with jinja.

In the end, I managed to achieve all my goals to create everything I would want in a project manager and I believe it will be quite useful to me in the future.

Layout.html contains a base layout with a navbar.
Login.html contains the first page with 2 pictures, from the website, login, and register.
Projects.html contains a summarised list of existing projects. Here, you can either choose to create a new project or edit an existing one.
Editor.html shows you a form when creating a new project.
Editor2.html shows you the same form but with existing data prefilled when editing a project.
History.html shows you a list of completed and abandoned projects.
app.py contains all the code to enter data in sql tables and more.
Helpers.py contains apology and login_required which help out in app.py
Project.db contains all the sql databases.