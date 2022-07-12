#! /bin/sh

# from script folder move to deploy destination.
cd ../deploy/parenting.production

# git checkout main branch in heroku repository
# maybe should git pull the newest version from remote repositroy
git checkout main

# move to base folder
cd ../../


# clean the deploy folder.
rm -rfv deploy/parenting.production/*

# copy deploy need project files
cp -R parenting/ deploy/parenting.production/parenting

# remove the local debug files
rm deploy/parenting.production/.env

# copy git ignore avoid some ignore file been uploading
cp deploy/ignorefiles/.gitignore deploy/parenting.production

# copy pipfile that install requirement packages
cp -R pyproject.toml deploy/parenting.production/pyproject.toml
cp -R poetry.lock deploy/parenting.production/poetry.lock

# copy procfile from procfiles folder, it decide how to startup the project on heroku
cp deploy/procfiles/parenting.production.Procfile deploy/parenting.production/Procfile

# remote to deploy folder
cd deploy/parenting.production

# create a commit prepare pushing to heroku remote repository.
git add -A
git commit
git push heroku main -f

# and then, heroku receive the push request, it will start the pipeline flow 
# with build, test, deploy, startup...etc