import time

import pytest

from kouyou.google import drive


def test_connect_to_google_drive():
    """Test method connect_to_google_drive.
    Validate if connection returned as googleapiclient.discovery.Resource
    """
    from googleapiclient.discovery import Resource
    drive_connection = drive.connect_to_google_drive()
    assert isinstance(drive_connection, Resource)


def test_create_3rdparty_file_in_drive():
    """Test method create_3rdparty_file_in_drive.
    After creating validate if the file was created in directory
    """
    folder_id = "1gV39MHAmLr84Gqr_7jUWm-BNW_zdh3Yx"
    file_name = "kouyou_drive_3rdparty_test"
    drive.create_3rdparty_file_in_drive(file_name, folder_id)

    # Wait to upload
    time.sleep(20)
    # Checking if file has been uploaded
    uploaded = False
    drive_service = drive.connect_to_google_drive()
    search_query = f"'{folder_id}' in parents and name='{file_name}'"
    search_result = drive_service.files().list(q=search_query).execute()
    if len(search_result["files"]) == 1:
        if search_result["files"][0]["name"] == file_name:
            uploaded = True
    assert uploaded


def test_delete_file_in_drive():
    """Test method delete_file_in_drive.
    The file that will be deleted is the file
    created in test_create_3rdparty_file_in_drive
    """
    drive_service = drive.connect_to_google_drive()
    folder_id = "1gV39MHAmLr84Gqr_7jUWm-BNW_zdh3Yx"
    file_name = "kouyou_drive_3rdparty_test"
    deleted = False
    # Checking if file exists
    search_query = f"'{folder_id}' in parents and name='{file_name}'"
    search_result = drive_service.files().list(q=search_query).execute()
    if len(search_result["files"]) > 0:
        if search_result["files"][0]["name"] == file_name:
            # Deleting the file
            drive.delete_file_in_drive(file_name, folder_id)
    # Verifying if file(s) has been deleted
    search_query = f"'{folder_id}' in parents and name='{file_name}'"
    search_result = drive_service.files().list(q=search_query).execute()
    if len(search_result["files"]) == 0:
        deleted = True
    assert deleted