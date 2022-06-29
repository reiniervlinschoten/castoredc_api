"""File to extract secrets and ids from environment for testing purposes"""
import os

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

test_client_study_id = os.environ["CLIENT_STUDY_ID"]
test_study_study_id = os.environ["STUDY_STUDY_ID"]
test_import_study_id = os.environ["IMPORT_STUDY_ID"]
test_special_study_id = os.environ["SPECIAL_STUDY_ID"]
write_client_study_id = os.environ["WRITE_STUDY_ID"]
