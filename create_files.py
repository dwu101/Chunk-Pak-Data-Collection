def create_files(target_folder, month, year):
    from Google import Create_Service
    from settings import floor_13_id, floor_4_id, source_folder_id, CLIENT_SECRET, CloudEmail

    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    service = Create_Service(CLIENT_SECRET, API_SERVICE_NAME, API_VERSION, SCOPES)

    properties = {
                'title': '{x} {y}'.format(x= month, y = year),
                'locale': 'en_US',
                'autoRecalc': 'ON_CHANGE', 
                'timeZone': 'America/Los_Angeles'
                }

    if target_folder == floor_4_id or target_folder == floor_13_id:
        sheet_body = {
            'properties': properties,
            
            'sheets': [
                {
                    'properties': {
                        'title': 'Week 1 Noise'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 1 AQ'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 2 Noise'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 2 AQ'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 3 Noise'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 3 AQ'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 4 Noise'
                    }
                },
                {
                    'properties': {
                        'title': 'Week 4 AQ'
                    }
                }
            ],
        
        }
    else:
        sheet_body = {
        'properties': properties,

        'sheets': [
            {
                'properties': {
                    'title': 'Week 1 Noise'
                }
            },
            
            
            {
                'properties': {
                    'title': 'Week 2 Noise'
                }
            },
            {
                'properties': {
                    'title': 'Week 3 Noise'
                }
            },
            
            {
                'properties': {
                    'title': 'Week 4 Noise'
                }
            },
        
        ],
    
    }


    sheets_file = service.spreadsheets().create(body=sheet_body).execute()    

    source_file_id = sheets_file['spreadsheetId']

    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET, API_SERVICE_NAME, API_VERSION, SCOPES)

    service.files().update(
        fileId = source_file_id,
        addParents = target_folder,
        removeParents = source_folder_id,
    ).execute()

    service.permissions().create(
        fileId= source_file_id,
        body = {
            "role": "writer",
            "type": "user",
            "emailAddress": CloudEmail,
        }
    ).execute()

    return source_file_id
