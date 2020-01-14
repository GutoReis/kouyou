import numpy as np
import pandas as pd
import pytest

from kouyou.google import drive, sheets


@pytest.fixture
def workbook_as_df():
    # First worksheet
    column1 = ["10", "11", "12", "13", "14", "15",
               "16", "17", "18", "19", "20"]
    column2 = ["20", "21", "22", "23", "24", "25",
               "26", "27", "28", "29", "30"]
    column3 = ["30", "31", "32", "33", "34", "35",
               "36", "37", "38", "39", "40"]
    column4 = ["40", "41", "42", "43", "44", "45",
               "46", "47", "48", "49", "50"]
    worksheet1_datas = {"Column 1": column1,
                        "Column 2": column2,
                        "Column 3": column3,
                        "Column 4": column4}
    ws_1_df = pd.DataFrame(worksheet1_datas)
    # Second worksheet
    columnA = ["60", "61", "62", "63", "64", "65",
               "66", "67", "68", "69", "70"]
    columnB = ["70", "71", "72", "73", "74", "75",
               "76", "77", "78", "79", "80"]
    columnC = ["80", "81", "82", "83", "84", "85",
               "86", "87", "88", "89", "90"]
    columnD = ["90", "91", "92", "93", "94", "95",
               "96", "97", "98", "99", "100"]
    worksheet2_datas = {"Column A": columnA,
                        "Column B": columnB,
                        "Column C": columnC,
                        "Column D": columnD}
    ws_2_df = pd.DataFrame(worksheet2_datas)

    return {"test_1": ws_1_df, "test_2": ws_2_df}


def test_connection_to_google_sheet():
    """Test the connection method to google sheets api.

    Validate if connection returned as gspread.client.Client
    """
    from gspread.client import Client
    sheets_service = sheets.connect_to_google_sheet()
    assert isinstance(sheets_service, Client)


def test_get_workbook_as_df(workbook_as_df):
    """Test get_workbook_as_df to check if reading is ok.

    Compare what returns from the method to workbook_as_df var
    """
    file_name = "kouyou_sheets_read_test"
    gspread_workbook = sheets.get_workbook_as_df(file_name)
    assert gspread_workbook["test_1"].equals(workbook_as_df["test_1"])
    assert gspread_workbook["test_2"].equals(workbook_as_df["test_2"])


def test_error_get_workbook_as_df():
    """Test error case when getting workbook from gdrive."""
    from gspread.exceptions import SpreadsheetNotFound
    with pytest.raises(SpreadsheetNotFound):
        sheets.get_workbook_as_df("wrong_spreadsheet_name")


def test_send_df_to_gspread():
    """Test send_df_to_gspread method.

    After sending, the file is searched in the folder,
    and deleted after that
    """
    test_df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)),
                           columns=list("ABCD"))
    folder_id = "1gV39MHAmLr84Gqr_7jUWm-BNW_zdh3Yx"
    file_name = "kouyou_sheets_write_test"
    sheets.send_df_to_gspread(workbook_name=file_name,
                              folder_id=folder_id,
                              df_list=[test_df])

    # Checking if file has been uploaded
    uploaded = False
    drive_service = drive.connect_to_google_drive()
    search_query = f"'{folder_id}' in parents and name='{file_name}'"
    search_result = drive_service.files().list(q=search_query).execute()
    if len(search_result["files"]) == 1:
        if search_result["files"][0]["name"] == file_name:
            uploaded = True
            drive.delete_file_in_drive(file_name, folder_id)
    assert uploaded


def test_error_send_df_to_gspread():
    """Test error case when uploading file to gdrive."""
    from googleapiclient.errors import HttpError

    test_df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)),
                           columns=list("ABCD"))
    file_name = "test_error"
    folder_id = "folder_error"
    with pytest.raises(HttpError):
        sheets.send_df_to_gspread(file_name, folder_id, [test_df])
