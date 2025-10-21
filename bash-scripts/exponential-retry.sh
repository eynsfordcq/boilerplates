#!/bin/bash

# configuration 
MAX_RETRIES=5
INITIAL_DELAY=2

retry_command() {
    local retries=0
    local delay=$INITIAL_DELAY
    local success=0

    while [ $retries -lt $MAX_RETRIES ]; do
        "$@" && { success=1; break; } # Run the command and break if successful
        retries=$((retries + 1))
        echo "Attempt $retries failed. Retrying in $delay seconds..."
        sleep $delay
        delay=$((delay * 2)) # Exponential backoff: double the delay
    done

    if [ $success -ne 1 ]; then
        echo "Command failed after $MAX_RETRIES attempts."
        return 1
    fi
}

# sample: upload to s3 with retry
retry_command sudo /usr/local/bin/aws s3 cp /some/file s3://some/bucket/
