#!/bin/bash

ASK=1
RECREATE_DB=0
UPSTREAM='main'

POSITIONAL_ARGS=()

args_parse () {
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dev)
            UPSTREAM='dev'
            shift
            ;;
            -db|--database)
            RECREATE_DB=1
            shift
            ;;
            -h|--help)
            help
            exit 0
            ;;
            -y|--no-ask)
            ASK=0
            shift
            ;;
            -*|--*)
            echo "Unknown option $1"
            help
            exit 1
            ;;
            *)
            POSITIONAL_ARGS+=("$1") # save positional arg
            shift # past argument
            ;;
        esac
    done

}

help () {

    echo "Usage: $0 [OPTIONS]"
    echo 'Update tool for the site of LADISPE'
    echo
    echo 'Options:'
    echo -e '-d, --dev \t\t pull from the dev repository'
    echo -e '-db, --database \t\t recreate also the database container'
    echo -e '-h, --help \t\t print this usage message'
    echo -e '-y, --no-ask \t\t no ask for user confirmation'

}

git_update () {

    if [ -z "$MODIFICATIONS" ]; then
        # Already done
        git checkout --quiet $UPSTREAM
    fi

    git pull
    echo "[*] Code pulling completed"
}

remove_dockers () {

    echo '[*] Removing old versions of the dockers'
    
    if [[ $RECREATE_DB -eq 1 ]]; then
        postgres_id=$(docker container ls --all | grep postgres | cut -d' ' -f1)
        postgres_image_id=$(docker image ls | grep postgres |  cut -d' ' -f14)
        if [ ! -z "$postgres_id" ]; then docker container rm "postgres_id"; fi
        if [ ! -z "$postgres_image_id" ]; then docker image rm "postgres_image_id"; fi
    fi

    nginx_id=$(docker container ls --all | grep nginx | cut -d' ' -f1)
    nginx_image_id=$(docker image ls | grep nginx |  cut -d' ' -f14)
    if [ ! -z "$nginx_id" ]; then docker container rm "$nginx_id"; fi
    if [ ! -z "$nginx_image_id" ]; then docker image rm "$nginx_image_id"; fi
    
    backend_id=$(docker container ls --all | grep backend | cut -d' ' -f1)
    backend_image_id=$(docker image ls | grep backend |  cut -d' ' -f12)
    if [ ! -z "$backend_id" ]; then docker container rm "$backend_id"; fi
    if [ ! -z "$backend_image_id" ]; then docker image rm "$backend_image_id"; fi

    echo '[*] Old versions of the dockers removed'
}

revert () {

    echo
    echo "Actually on branch: $OLD_BRANCH"
    echo  "$MODIFICATIONS"
    echo

    if [[ $ASK -eq 1 ]]; then 
        read -p "Revert local changes? y/N? " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo '[!] Aborted'
            exit 1
        fi
    fi

    git checkout --quiet -f "$UPSTREAM"
    git reset --hard --quiet "origin/$UPSTREAM"
    
    echo "[*] Modifications reverted" 
}

main () {

    args_parse "$@"

    echo "[*] $(git fetch --all)" 
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "origin/$UPSTREAM")
    BASE=$(git merge-base @ "origin/$UPSTREAM")

    MODIFICATIONS=$(git status | grep 'modified:')
    OLD_BRANCH=$(git status | grep 'On branch' | sed 's/On branch //')

    if [ $LOCAL = $REMOTE ]; then
        echo "[*] Up-to-date"
        exit 0
    elif [ $LOCAL = $BASE ]; then
        echo "[*] Need to pull"
    else
        if [ -z "$MODIFICATIONS" ]; then
            echo "[!] Need to revert changes"
            revert
        else
            echo "[!] Need to checkout"
        fi
    fi

    docker-compose --file docker-compose.prod.yml down
    remove_dockers
    git_update

    echo '[*] Trying to run the new version of the dockers'
    docker-compose --file docker-compose.prod.yml up -d --force-recreate

    echo '[*] Done'
    exit 0

}

main "$@"