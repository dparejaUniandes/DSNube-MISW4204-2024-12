gcloud builds submit \
  --tag gcr.io/$GOOGLE_CLOUD_PROJECT/worker-server

gcloud run deploy worker-server \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/worker-server \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated \
  --max-instances=1