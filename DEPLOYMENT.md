# 🚀 Deployment Guide - Gemini 2.0 Web App

This guide walks you through deploying your Gemini 2.0 web app to various cloud platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Google Cloud Project with Vertex AI API enabled
- ✅ Service Account with `Vertex AI User` role
- ✅ Service Account Key (JSON file)
- ✅ Your app working locally

---

## 🌟 Option 1: Streamlit Cloud (Easiest & Free)

**Best for:** Quick deployment, free hosting, easy setup

### Step 1: Prepare Your Repository
1. Push your code to GitHub (public or private repo)
2. Make sure all files are committed:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Choose `streamlit_app.py` as the main file
6. Click "Deploy"

### Step 3: Configure Secrets
1. In your Streamlit Cloud app dashboard, go to "Settings" → "Secrets"
2. Add your secrets in TOML format:
   ```toml
   GOOGLE_CLOUD_PROJECT = "your-project-id"
   VERTEX_AI_LOCATION = "us-central1"
   
   # Paste your entire service account JSON here
   GOOGLE_APPLICATION_CREDENTIALS_JSON = '''
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "...",
     "private_key": "...",
     "client_email": "...",
     "client_id": "...",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "..."
   }
   '''
   ```

### Step 4: Access Your App
Your app will be available at: `https://your-app-name.streamlit.app`

**✅ Pros:** Free, easy setup, automatic updates
**❌ Cons:** Limited resources, public unless you pay

---

## 🔥 Option 2: Google Cloud Run (Recommended for Production)

**Best for:** Scalable deployment, pay-per-use, same cloud as Vertex AI

### Step 1: Enable Required Services
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Deploy
```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build the container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/gemini-web-app

# Deploy to Cloud Run
gcloud run deploy gemini-web-app \
  --image gcr.io/$PROJECT_ID/gemini-web-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501 \
  --memory 2Gi \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID
```

### Step 3: Set Up Service Account
```bash
# Create service account for the app
gcloud iam service-accounts create gemini-web-app-sa

# Grant Vertex AI permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:gemini-web-app-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Update Cloud Run service to use the service account
gcloud run services update gemini-web-app \
  --service-account gemini-web-app-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --region us-central1
```

**✅ Pros:** Highly scalable, pay-per-use, same cloud as Vertex AI
**❌ Cons:** Requires Google Cloud knowledge, potential costs

---

## 🚢 Option 3: Railway (Easy Alternative)

**Best for:** Modern deployment, good free tier, easy setup

### Step 1: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/in with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect it's a Python app

### Step 2: Configure Environment Variables
In Railway dashboard:
```
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
```

### Step 3: Add Service Account Key
1. Create a new variable `GOOGLE_APPLICATION_CREDENTIALS_JSON`
2. Paste your entire service account JSON as the value

**✅ Pros:** Easy deployment, modern interface, good free tier
**❌ Cons:** Newer platform, limited free resources

---

## 🌐 Option 4: Render (Reliable Alternative)

**Best for:** Reliable hosting, good for production, free tier available

### Step 1: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up/in with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

### Step 2: Configure Environment Variables
```
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS_JSON=<your-service-account-json>
```

**✅ Pros:** Reliable, good free tier, easy SSL
**❌ Cons:** Can be slow on free tier

---

## 🐳 Option 5: Docker + Any Cloud (Advanced)

**Best for:** Full control, any cloud provider, containerized deployment

### Step 1: Build Docker Image
```bash
# Build the image
docker build -t gemini-web-app .

# Test locally
docker run -p 8501:8501 \
  -e GOOGLE_CLOUD_PROJECT=your-project-id \
  -e GOOGLE_APPLICATION_CREDENTIALS_JSON='<your-json>' \
  gemini-web-app
```

### Step 2: Deploy to Any Cloud
- **AWS:** Use ECS or EKS
- **Azure:** Use Container Instances or AKS
- **DigitalOcean:** Use App Platform
- **Heroku:** Use Container Registry

---

## 🔧 Deployment Checklist

Before deploying:
- [ ] Test your app locally
- [ ] Ensure all dependencies are in `requirements.txt`
- [ ] Set up Google Cloud service account
- [ ] Test authentication with your service account
- [ ] Choose your deployment platform
- [ ] Configure environment variables/secrets
- [ ] Test the deployed app
- [ ] Set up monitoring (optional)

## 🛡️ Security Best Practices

1. **Never commit secrets:** Use `.gitignore` for sensitive files
2. **Use environment variables:** Never hardcode credentials
3. **Limit service account permissions:** Only grant necessary roles
4. **Enable authentication:** For production apps, consider adding auth
5. **Monitor usage:** Set up billing alerts and usage monitoring

## 💰 Cost Considerations

| Platform | Free Tier | Paid Starting |
|----------|-----------|---------------|
| Streamlit Cloud | 1 private app | $20/month |
| Google Cloud Run | 2M requests/month | Pay per use |
| Railway | $5/month included | $5/month |
| Render | 750 hours/month | $7/month |

## 🆘 Troubleshooting

**Authentication Issues:**
- Verify service account has correct permissions
- Check if credentials JSON is properly formatted
- Ensure project ID is correct

**Deployment Failures:**
- Check logs in your platform's dashboard
- Verify all environment variables are set
- Ensure Python version compatibility

**Performance Issues:**
- Increase memory allocation
- Add caching for repeated requests
- Consider using a CDN for static assets

---

## 🎯 Recommended Deployment Path

1. **Start with Streamlit Cloud** - Quick and easy for testing
2. **Move to Google Cloud Run** - When you need more control/scale
3. **Add monitoring and optimization** - For production use

---

**Need help?** Check the troubleshooting section in the main README.md or create an issue in the repository! 