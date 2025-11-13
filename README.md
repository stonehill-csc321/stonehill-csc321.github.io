#Stonehill CSC321 Final Projects

This repository is set up to deploy to https://stonehill-csc321.github.io. If you add your data and dashboard code to this repository, it will be on the Internet.

### Instructions for Adding your Dashboard

One member of your group should take responsibility for interacting with Github. If no one on your team has used github before, let me know.

1. If you haven't already, create a github account: https://github.com/signup
2. If you are on a windows computer and haven't done so already: download [Git for windows](https://gitforwindows.org/). 
3. If you are comfortable using the terminal, use `git clone git@github.com:stonehill-csc321/stonehill-csc321.github.io.git`. If not, use [Github desktop](https://desktop.github.com/download/) to clone https://github.com/stonehill-csc321/stonehill-csc321.github.io
4. Put the files from your project into the `assets` folder. I've created a folder for each project:
* `MyAnimeList`: Nate and Michely
* `PremierLeague`: Alexi, Reid, Nick
* `CovidCases`: Michael
* `Pokemon`: Josh, Liam, Cody
* `SpotifySongs`: Jason, Mark, Sean
* `Basketball`: Arthur, Cael, Emilio

Feel free to change these folder names if you want.

**Do not add data files of more than 20mb** If your dataset is larger than that, do your data munging separately and only upload the needed data. If you commit any large files to this repository, you won't be able to push to github. If you really do need a single huge file for some reason, talk to me.

5. Create a file in `_projects/` named `your_project_name.md` where `your_project_name` is your project name, then add yaml with the name and url of your project in assets. Look at `test_project.md` as an example of the right format.
6. `git add`, `git commit` and `git push` the files. If you're unsure how to do that, come to my office hours. Please do not commit any changes to the existing files in the repository.
7. After pushing, wait ~2 minutes then check https://stonehill-csc321.github.io to see your project deployed!
