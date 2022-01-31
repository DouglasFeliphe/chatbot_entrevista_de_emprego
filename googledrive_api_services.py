from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from config import DEFAULT_BOT_FOLDER_ID


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


"""Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())      
 
   
googledrive_service = build('drive', 'v3', credentials=creds) 


def create_user_folder(user_fullname):
    print('creating user folder...')
    user_folder_id = None
    
    try:
        FILE_METADATA = {
            'name': user_fullname,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [DEFAULT_BOT_FOLDER_ID]
        }
        
        file = googledrive_service.files().create(body=FILE_METADATA,
                                    fields='id').execute()
        user_folder_id = file.get('id')
        print('Folder ID: ', user_folder_id)
        
        # list files
        # results = googledrive_service.files().list(
        #     pageSize=10  fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])
        # if not items:
        #     print('No files found.')
        # else:            
        #     print('Files:')
        #     for item in items:
        #         print(u'{0} ({1})'.format(item['name'], item['id']))
            
        
        # Call the Drive v3 API
        # results = googledrive_service.files().list(
        #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])

        # if not items:
        #     print('No files found.')
        #     return
        # print('\nFiles:')
        # for item in items:
        #     print(u'{0} ({1})'.format(item['name'], item['id']))

        return user_folder_id
    
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
                
  
        
def upload_file_in_user_folder(filename, user_folder_id, file):
    print('uploading file in user folder...')
    
    try:      
        
        FILE_METADATA = {
            'name': filename,
            'parents': [user_folder_id]
        }        
        
        MIME_TYPE = file.mime_type        
        
        # print('filename: ', f'{filename}')
        media = MediaFileUpload(filename, chunksize=1024 * 1024, mimetype=MIME_TYPE,  resumable=True)
        request = googledrive_service.files().create(body=FILE_METADATA,
                                media_body=media)  
        
            #'VideoNote' object has no attribute 'mime_type'
            
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print( "Uploaded %d%%." % int(status.progress() * 100))  
        
        
        # list files in the user folder
        file = googledrive_service.files().create(
                body=FILE_METADATA,
                media_body=media,
                fields='id').execute()
        print ('File ID: %s' % file.get('id'))
        return file.get('id')
        
        
    except HttpError as error:
        #TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')




def upload_video_in_user_folder(filename, user_folder_id, MIME_TYPE):
    print('uploading video in user folder...')
    
    try:      
        
        FILE_METADATA = {
            'name': filename,
            'parents': [user_folder_id]
        }             
        
        # print('filename: ', f'{filename}')
        media = MediaFileUpload(filename, chunksize=1024 * 1024, mimetype=MIME_TYPE,  resumable=True)
        request = googledrive_service.files().create(body=FILE_METADATA,
                                media_body=media)  
        
            
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print( "Video Uploaded %d%%." % int(status.progress() * 100))  
                
        
        # list files in the user folder
        file = googledrive_service.files().create(
                body=FILE_METADATA,
                media_body=media,
                fields='id').execute()
        print ('File ID: %s' % file.get('id'))
        return file.get('id')
        
    except HttpError as error:
        #TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
                
        
        