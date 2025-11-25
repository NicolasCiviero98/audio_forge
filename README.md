

docker build -t audioforge .

docker run -p 8080:8080 --env-file .env audioforge

docker run -p 8080:8080 `
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/sa.json `
  -v "C:\Projetos\python\audioForge\app\sa.json:/app/sa.json" `
  --env-file ".env" `
  audioforge


Activate the Service Account
`gcloud auth activate-service-account --key-file="C:\Projetos\python\audioForge\app\sa.json"`
Verify the Active Account
`gcloud auth list`
Set the Project: Ensure your gcloud CLI is configured to use the correct Google Cloud Project associated with your service account.
gcloud config set project mesa-online-42f53


Step 2: Configure Docker for Artifact Registry
gcloud auth configure-docker southamerica-east1-docker.pkg.dev

export IMAGE_PATH="us-central1-docker.pkg.dev/mesa-online-42f53/fastapi-repo/audioforge-api:latest"










