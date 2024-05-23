gcloud builds submit \
  --tag gcr.io/$GOOGLE_CLOUD_PROJECT/web-server
gcloud run deploy web-server \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/web-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --max-instances=1