#!/bin/bash
# This script will download exact copies of several git repositories specified from a file
#FIX this does not handle paths with spaces correctly


REPO_LIST="REPOS.list"  # Specify the location of your list of repos here. This should be a newline seperated file of links to repos
OPTIONS="--recurse-submodules --jobs=10"
# Prevents git from prompting for authentication when repos go private
export GIT_TERMINAL_PROMPT=0  # For git>2.3
#export GIT_ASKPASS=/bin/echo  # For git <=2.3

color="echo -ne "

# Check if the REPO_LIST file exists. If not, exit
if [[ ! -f $REPO_LIST ]]
then
  echo "FAILED! Please specify the REPO_LIST variable in the script file!"
  exit -1
fi


echo "++ Cloning any new repos ++"
while read repo;
do
  folder=$(basename "$repo")-$(basename "$(dirname "$repo")")  # stores the repo in a folder named REPO_NAME-USER
  if [[ ! -d $folder ]]
    then
    echo "$folder"
    git clone $OPTIONS "$repo" "$folder"
  fi
done < $REPO_LIST


echo "++ Updating existing repos ++"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
find "$SCRIPT_DIR" -mindepth 1 -maxdepth 1 -type d -print \
 | while read repo;
do
  $color "\033[0;33m"
  echo "$(basename $(dirname $repo))/$(basename $repo)" # : $repo"
  $color "\033[0m"
  cd "$repo" && \
  git pull --rebase -f $OPTIONS && \
  git reset --hard -q && \
  git clean -f #&& \
# WARNING: The following will purge local branches that were deleted off the remote.
# This is good for exact copies, even if destructive, but not for archives, as if the remote is deleted, your copy is deleted.
  #git remote prune origin
done

echo -e "\nCOMPLETE!"


# RESOURCES
# https://stackoverflow.com/questions/23563062/how-do-i-force-git-not-to-prompt-for-credentials#23563077

