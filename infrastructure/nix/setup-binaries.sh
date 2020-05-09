#!/usr/bin/env bash

# this script will create links for all users.

function symlink_user_challenge() {
  local USER="$1"
  local CHAL_ID="$2"
  local CHAL_NAME="$3"
  local BINARY_CHALLENGE_PATH="$4"
  local UNPATCHED_BINARY_CHALLENGE_PATH="$5"
  local FLAG_USERNAME="$6"
  local USERNAME="$1-$2"

  if [ -d "/home/$USER-$CHAL_ID/challenge" ]; then
          rm -rf "/home/$USER-$CHAL_ID/challenge"
  fi

  if [ -d "/home/$USER-$CHAL_ID/unpatched" ]; then
          rm -rf "/home/$USER-$CHAL_ID/unpatched"
  fi

  cp -rf "$BINARY_CHALLENGE_PATH" "/home/$USER-$CHAL_ID/challenge"
  cp -rf "$UNPATCHED_BINARY_CHALLENGE_PATH" "/home/$USER-$CHAL_ID/unpatched"

  if [ -f "/home/$USER-$CHAL_ID/challenge/flag.txt" ]; then
          unlink "/home/$USER-$CHAL_ID/challenge/flag.txt"
  fi

  if [ -f "/run/keys/$USER-$CHAL_ID" ]; then
          ln -sf "/run/keys/$USER-$CHAL_ID" "/home/$USER-$CHAL_ID/challenge/flag.txt"
          chown -h "$FLAG_USERNAME:keys" "/home/$USER-$CHAL_ID/challenge/flag.txt"
  fi
        
  chown "$USERNAME:ctf" "/home/$USER-$CHAL_ID"
  chmod "g+rx" "/home/$USER-$CHAL_ID"

  chown "$USERNAME:ctf" "/home/$USER-$CHAL_ID/challenge"
  chown -R "$USERNAME:users" "/home/$USER-$CHAL_ID/unpatched"
  chown "$FLAG_USERNAME:keys" "/home/$USER-$CHAL_ID/challenge/$CHAL_NAME"
  chmod "ug+s" "/home/$USER-$CHAL_ID/challenge/$CHAL_NAME"
}
