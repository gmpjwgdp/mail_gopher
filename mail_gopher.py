import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import cv2


# Gmail APIのスコープを設定
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.modify",
]


def get_credential():
    """
    アクセストークンの取得

    カレントディレクトリに pickle 形式でトークンを保存し、再利用できるようにする。
    """
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_id.json", SCOPES)
            creds = flow.run_local_server()
            #creds = flow.run_console()
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

def get_unread_mail(service):
  results = service.users().messages().list(userId="me", q="is:unread", maxResults=500).execute()
  return results

def main():
  creds = get_credential()
  service = build("gmail", "v1", credentials=creds, cache_discovery=False)
  count_unread = len(get_unread_mail(service)['messages'])
  if count_unread == 0:
    text = 'You have no unread messages.'
  elif count_unread == 500:
    text = 'You have over 500 unread messages.'
  else:
    text = f'You have {count_unread} unread messages.'
  gopher_head = cv2.imread('./gopher_head.png')
  gopher_middle = cv2.imread('./gopher_middle.png')
  gopher_middle_white = cv2.imread('./gopher_middle_white.png')
  gopher_bottom = cv2.imread('./gopher_bottom.png')
  gopher = cv2.vconcat([gopher_head] + [gopher_middle_white] * 10 + [gopher_middle] * count_unread + [gopher_bottom])
  cv2.putText(gopher,
            text=text,
            org=(0, 225),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=0.8,
            color=(255, 0, 0),
            thickness=1,
            lineType=cv2.LINE_4)
  cv2.imshow('gopher_front', gopher)
  cv2.waitKey(0)


if __name__ == "__main__":
  main()
