#!/bin/bash

# Send POST request to start scraping
START_URL="http://127.0.0.1:8000/api/taskmanager/start_scraping/"
START_RESPONSE=$(curl -s -X POST $START_URL -H "Content-Type: application/json" -d '["DUKO", "xrp", "bitcoin"]')

# Extract job ID from response
JOB_ID=$(echo $START_RESPONSE | jq -r '.job_id')

# Initialize status as pending
STATUS="Pending"

# Define the status URL with job ID
STATUS_URL="http://127.0.0.1:8000/api/taskmanager/scraping_status/$JOB_ID/"

# Send GET request to check scraping status continuously until it's no longer pending
while [ "$STATUS" == "Pending" ]
do
    STATUS_RESPONSE=$(curl -s $STATUS_URL)
    STATUS=$(echo $STATUS_RESPONSE | jq -r '.status')
    sleep 5  # Wait for 5 seconds before checking again
done

# Save output to files
echo $START_RESPONSE > start_response.json
echo $STATUS_RESPONSE > status_response.json
