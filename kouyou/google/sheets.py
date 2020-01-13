import os

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import unidecode

from kouyou.google import drive


def connect_to_google_sheet():
    """Create connection with google spreadsheets api.

    :return: instance os google api connection
    :rtype: gspread.client.Client
    """
    SCOPES = ["https://www.googleapis.com/auth/drive",
              "https://spreadsheets.google.com/feeds"]
    try:
        cred_file = (os.path.expanduser("~") +
                     "/.ssh/google_drive_key.json")
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't find file 'google_drive_key.json'," +
                                " verify if file exists in /home/USER/.ssh/")

    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file,
                                                                   SCOPES)
    google_connection = gspread.authorize(credentials)
    return google_connection


def get_workbook_as_df(file_name):
    """Get shared spreadsheet from google drive.

    :param file_name: File name to search
    :type file_name: str

    :return: dict from spreadsheet file: pandas.core.frame.DataFrame
    :rtype: dict
    """
    google_connection = connect_to_google_sheet()
    workbook = google_connection.open(file_name)

    worksheet_list = workbook.worksheets()
    worksheet_df_dict = dict()

    for worksheet in worksheet_list:
        title = unidecode.unidecode(worksheet.title).lower()
        data = worksheet.get_all_values()
        worksheet_df = pd.DataFrame(data)
        worksheet_df_dict[title] = worksheet_df
    return worksheet_df_dict


def send_df_to_gspread(workbook_name, folder_id, df_list):
    """Upload a file as a google spreadsheet direct to google drive.

    :param workbook_name: File name, without extension
    :type workbook_name: str
    :param folder_id: Google Drive Folder ID
    :type folder_id: str
    :param df_list: List of pandas.core.frame.DataFrame with the datas
    :type df_list: list
    """
    GSPREAD_MIMETYPE = "application/vnd.google-apps.spreadsheet"
    EXCEL_MIMETYPE = ("application/vnd.openxmlformats-officedocument." +
                      "spreadsheetml.sheet")
    # Writing file to send
    writer = pd.ExcelWriter(workbook_name+".xlsx")
    sheet_number = 1
    for df in df_list:
        df.to_excel(writer,
                    sheet_name=f"sheet-{sheet_number}",
                    index=False)
        sheet_number += 1
    writer.save()

    # Connect to google drive
    driver_service = drive.connect_to_google_drive()

    body = {"name": workbook_name,
            "mimeType": GSPREAD_MIMETYPE,
            "parents": [folder_id]}
    media = MediaFileUpload(workbook_name+".xlsx", mimetype=EXCEL_MIMETYPE)
    driver_service.files().create(body=body, media_body=media).execute()

    # Remove local sheet
    os.remove(workbook_name+".xlsx")
    