#!/bin/bash
# Script to check Ada.goldwing@gmail.com for new emails and send summary via Telegram

# Ensure Himalaya is available
if ! command -v himalaya &> /dev/null; then
    echo "Himalaya not installed. Please install Himalaya CLI and configure account for Ada.goldwing@gmail.com"
    exit 1
fi

# Default account - adjust if needed
ACCOUNT="ada"  # Change to match the account name in Himalaya config

# Get unseen emails from INBOX
UNSEEN=$(himalaya --account "$ACCOUNT" envelope list --unseen --folder INBOX --output plain 2>/dev/null || true)

if [ -z "$UNSEEN" ]; then
    MESSAGE="📧 *Email Check for Ada.goldwing@gmail.com*\n\nNo new unseen emails."
else
    # Count unseen emails
    COUNT=$(echo "$UNSEEN" | wc -l)
    # Get details for each unseen email (limit to 5 to avoid too long message)
    DETAILS=""
    while IFS= read -r line; do
        # Extract email ID from line (format varies; assume first column is ID)
        ID=$(echo "$line" | awk '{print $1}')
        if [ -n "$ID" ]; then
            # Get subject and sender
            SUBJECT=$(himalaya --account "$ACCOUNT" message read "$ID" --header Subject 2>/dev/null | sed -n 's/^Subject: //p')
            SENDER=$(himalaya --account "$ACCOUNT" message read "$ID" --header From 2>/dev/null | sed -n 's/^From: //p')
            # Truncate if too long
            SUBJECT_TRUNC=$(echo "$SUBJECT" | cut -c1-50)
            SENDER_TRUNC=$(echo "$SENDER" | cut -c1-30)
            DETAILS="$DETAILS• From: $SENDER_TRUNC\n  Subject: $SUBJECT_TRUNC\n\n"
        fi
    done <<< "$UNSEEN"
    
    # Limit details to first 5 emails
    DETAILS_LIMITED=$(echo "$DETAILS" | head -n 15)  # rough limit
    
    MESSAGE="📧 *Email Check for Ada.goldwing@gmail.com*\n\n*$COUNT new unseen email(s)*:\n\n$DETAILS_LIMITED\n_Time: $(date)_"
fi

# Output the message (will be captured by cron job delivery)
echo -e "$MESSAGE"