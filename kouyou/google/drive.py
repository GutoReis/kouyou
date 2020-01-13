import os

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def connect_to_google_drive():
    """Create connection with google drive api.

    :return: instance of google drive api connection
    :rtype: googleapiclient.discovery.Resource
    """
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    try:
        cred_file = (os.path.expanduser("~") +
                     "/.ssh/google_drive_key.json")
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't find file 'google_drive_key.json'," +
                                " verify if file exists in /home/USER/.ssh/")

    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file,
                                                                   SCOPES)
    driver_service = build("drive", "v3", credentials=credentials)
    return driver_service


def delete_file_in_drive(file_name, folder_id):
    """Delete every file with name from especific dir on Drive.

    :param file_name: Name of the file to be deleted
    :type file_name: str
    :param folder_id: parent folder id where lies the files
    :type folder_id: str
    """
    drive_service = connect_to_google_drive()
    # Get files in directory
    result = drive_service.files().list(q="'"+folder_id+"' in parents").execute()

    # Get file(s) ID
    id_list = list()
    for file in result["files"]:
        if file["name"] == file_name:
            id_list.append(file["id"])
    # Deleting file(s)
    for file_id in id_list:
        drive_service.files().delete(fileId=file_id).execute()
