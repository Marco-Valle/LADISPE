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

    if [ $REMOTE = $BASE ]; then
        # Already fetched before revert
        git fetch --all
    fi

    git checkout $UPSTREAM
    git pull
}

remove_dockers () {

    if [[ $RECREATE_DB -eq 1 ]]; then
        postgres_id=$(docker container ls --all | grep postgres | cut -d' ' -f1)
        postgres_image_id=$(docker image ls | grep postgres |  cut -d' ' -f14)
        if [ $postgres_id -df '' ]; then docker container rm ${postgres_id}; fi
        if [ $postgres_image_id -df '' ]; then docker image rm ${postgres_image_id}; fi
    fi

    nginx_id=$(docker container ls --all | grep nginx | cut -d' ' -f1)
    nginx_image_id=$(docker image ls | grep nginx |  cut -d' ' -f14)
    if [ $nginx_id -df '' ]; then docker container rm $nginx_id; fi
    if [ $nginx_image_id -df '' ]; then docker image rm $nginx_image_id; fi
    
    backend_id=$(docker container ls --all | grep backend | cut -d' ' -f1)
    backend_image_id=$(docker image ls | grep backend |  cut -d' ' -f12)
    if [ $backend_id -df '' ]; then docker container rm $backend_id; fi
    if [ $backend_image_id -df '' ]; then docker image rm $backend_image_id; fi
}

revert () {

    echo "UP $UPSTREAM"

    if [[ $ASK -eq 1 ]]; then 
        read -p "Revert local changes? y/N? " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo '[!] Aborted'
            exit 1
        fi
    fi

    exit 0
    git fetch --all
    git reset --hard "origin/$UPSTREAM"
}

main () {

    args_parse "$@"

    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "origin/$UPSTREAM")
    BASE=$(git merge-base @ "origin/$UPSTREAM")

    if [ $LOCAL = $REMOTE ]; then
        echo "[*] Up-to-date"
        exit 0
    elif [ $LOCAL = $BASE ]; then
        echo "[*] Need to pull"
    else [ $REMOTE = $BASE ]
        echo "[!] Need to revert changes"
        revert
    fi

    docker-compose --file docker-compose.prod.yml down
    remove_dockers
    git_update
    docker-compose --file docker-compose.prod.yml up -d --force-recreate

}

main "$@"