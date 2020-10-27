# APS360
APS360 Group Project

# Scripts

## check_for_incomplete_entries:
Used during data cleaning for the MuxspaceDataset

Specifically, it looks for:
1. Entries that do not have a corresponding image in the image folder
2. Entries that do not have an assigned emotion

The script will not do anything else other than tell you that these exist (script will not modify anything)

To run:
1. cd into `Data/MuspaceDataset`
2. run `python check_for_incomplete_entries.py`