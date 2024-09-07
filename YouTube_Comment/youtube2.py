import googleapiclient.discovery
import pandas as pd

class YouTubeCommentsFetcher:
    def __init__(self, api_key, video_id):
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.api_key = api_key
        self.video_id = video_id
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.api_key
        )

    def fetch_comments(self, total_comments=1000):
        comments = []
        next_page_token = None

        while len(comments) < total_comments:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=self.video_id,
                maxResults=min(total_comments - len(comments), 100),
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append([
                    comment['authorDisplayName'],
                    comment['publishedAt'],
                    comment['updatedAt'],
                    comment['likeCount'],
                    comment['textDisplay']
                ])

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        return pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

    def save_comments_to_csv(self, file_name):
        df = self.fetch_comments()
        df.to_csv(file_name, index=True)
        

