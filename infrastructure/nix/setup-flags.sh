#!/usr/bin/env bash

# this script will create links for all users.

function symlink_user_flag() {
  USER="$1"
  CHAL_ID="$2"

  if [ -f "/home/$USER-$CHAL_ID/flag.txt" ]; then
          unlink "/home/$USER-$CHAL_ID/flag.txt"
  fi

  ln -sf "/run/keys/$USER-$CHAL_ID" "/home/$USER-$CHAL_ID/flag.txt"
  chown -h "flags-$USER-$CHAL_ID:root" "/home/$USER-$CHAL_ID/flag.txt"
}
