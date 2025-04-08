#!/bin/bash

cd backend || { echo "Error: 'backend' folder not found."; exit 1; }

run_command() {
    eval "$1"
    if [ $? -ne 0 ]; then
        echo "Error: Command '$1' failed."
    else
        echo "Success: Command completed."
    fi
}

echo "Initializing Aerich..."
run_command "aerich init -t raktar_backend.TORTOISE_ORM"

echo "Running 'aerich init-db'..."
aerich init-db | while IFS= read -r line; do
    echo "$line"
    if [[ "$line" == *"Success generating initial migration file for app \"models\""* ]]; then
        echo "Killing Aerich..."
        pkill -P $$ aerich
        break
    fi
done

echo "Running migrations..."
migration_output=$(timeout 30s aerich migrate)
if [ $? -eq 124 ]; then
    echo "Warning: Migration either took too long or doesn't exist. If there is something to migrate, please run 'aerich migrate' manually."
else
    echo "$migration_output"
    run_command "aerich upgrade"
fi

echo "Starting backend..."
run_command "python3 raktar_backend.py"