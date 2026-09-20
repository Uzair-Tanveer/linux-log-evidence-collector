# Linux Log Review / Evidence Collection Script

## Overview

This project is a simple Linux-based Python tool that reviews authentication logs for failed login attempts and generates a timestamped evidence report.

## Purporse

The goal of this project is to demonstrate:
-Linux command-line familiarity
-Log review
-Evidence collection
-Python scripting
-Documentation and GitHub workflow

## Tools Used

-Linux
-Python 3
-Git
-GitHub

## How it Works

The script reads '/var/log/auth.log' searching for failed login entries such as 'Failed Password' and 'authentication failure', counts them, and saves the results into a timestamped report in the 'reports' folder.

## Lessons Learned

This project helped me practice reviewing security-related logs and documenting findings in a clear and repeatable format.
