import os

GOOGLE_API_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID')

GOOGLE_API_AUTH = {
  'type': os.environ.get('GOOGLE_AUTH_TYPE'),
  'project_id': os.environ.get('GOOGLE_AUTH_PROJECT_ID'),
  'private_key_id': os.environ.get('GOOGLE_AUTH_PRIVATE_KEY_ID'),
  'private_key': os.environ.get('GOOGLE_AUTH_PRIVATE_KEY'),
  'client_email': os.environ.get('GOOGLE_AUTH_CLIENT_EMAIL'),
  'client_id': os.environ.get('GOOGLE_AUTH_CLIENT_ID'),
  'auth_uri': os.environ.get('GOOGLE_AUTH_AUTH_URI'),
  'token_uri': os.environ.get('GOOGLE_AUTH_TOKEN_URI'),
  'auth_provider_x509_cert_url': os.environ.get('GOOGLE_AUTH_PROVIDER'),
  'auth_provider_x509_cert_url': os.environ.get('GOOGLE_AUTH_CERT_URL'),
}
