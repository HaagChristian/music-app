DB_INTEGRITY_ERROR: str = "Email already exists"

DB_NO_RESULT_FOUND: str = "No data found"

JWT_INVALID_TOKEN: str = "Provide a valid auth token"

WRONG_MME_TYPE: str = "Wrong media type. Please provide a valid mp3 file"

NO_METADATA_FOUND: str = "No ID3 tags found in the file"

METADATA_VALIDATION_ERROR: str = "An error occurred while validating the metadata. " \
                                 "Please try again or try another file. " \
                                 "If the error persists, please contact the administrator"

MISSING_DATA: str = "Please specify at least one of the parameters"

MISSING_TOKEN: str = "No token provided"

MISSING_PARAMETER: str = "Please specify at least one metadata field"

MISSING_SEARCH_CRITERIA: str = "Please specify at least one search criteria"

UNSUPPORTED_FORMAT_ERROR: str = "Requested format is not supported"

FILE_CONVERSION_ERROR: str = "Error occurred during file conversion"

UPDATE_METADATA_FROM_FILE: str = "Error occurred while updating the metadata from the file. Please try again later. " \
                                 "If the error persists, please contact the administrator"

MISSING_TITLE_FROM_METADATA: str = "Title is missing in the metadata. " \
                                   "Please make sure that at least a title is included in the metadata"

SONG_ALREADY_IN_DB: str = "Song already exists in the database"

INVALID_YEAR: str = "Invalid year. Please provide a valid year in the metadata"

IMPOSSIBLE_YEAR: str = "Year is not possible. Please provide a valid year in the metadata"
