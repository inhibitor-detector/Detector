#!/bin/bash

# Define the file path
file_path="app/.env"

# Generate a new password
new_password=$(openssl rand -hex 12)

# Read the file line by line
while IFS= read -r line; do
    # Check if the line contains the PASSWORD variable
    if [[ $line == *"PASSWORD="* ]]; then
        # Replace the existing password with the new one
        echo "PASSWORD=$new_password" >> temp_file
    else
        # Write the original line to the temporary file
        echo "$line" >> temp_file
    fi
done < "$file_path"

# Move the temporary file to the original file
mv temp_file "$file_path"
