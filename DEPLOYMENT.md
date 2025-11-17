# 🚀 Deployment Guide - Railway

Quick deployment checklist for Railway.

## Pre-Deployment Checklist

- [ ] Railway account created
- [ ] GitHub repository is public or Railway has access
- [ ] At least one AI API key ready (OpenAI, Cohere, or Anthropic)
- [ ] Environment variables documented

## Railway Deployment Steps

### 1. Initial Setup

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `AI-Code-Review` repository

### 2. Configure Environment Variables

In Railway dashboard → Your Service → Variables:

**Required:**
```env
OPENAI_API_KEY=your_key_here
# OR
COHERE_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here
```

**Optional but Recommended:**
```env
OPENAI_MODEL=gpt-4
SECRET_KEY=generate-a-random-secret-key
ALLOWED_ORIGINS=["*"]
```

### 3. Enable Auto-Deploy

1. Railway → Project → Settings
2. Enable **"Auto Deploy"**
3. Select branch: `main`
4. Railway will deploy on every push!

### 4. Verify Deployment

1. Check Railway → Deployments tab
2. Wait for build to complete (usually 2-5 minutes)
3. Railway provides a public URL automatically
4. Test the health endpoint: `https://your-app.railway.app/health`

## Post-Deployment

- [ ] Health check endpoint works
- [ ] API documentation accessible at `/docs`
- [ ] Environment variables configured correctly
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

## Troubleshooting

### Build Fails
- Check Railway logs for errors
- Verify Dockerfile is correct
- Ensure all dependencies are in requirements-minimal.txt

### App Crashes
- Check environment variables are set
- Verify PORT is being used correctly
- Check application logs in Railway dashboard

### API Not Working
- Verify API keys are correct
- Check CORS settings
- Ensure health endpoint responds

## Useful Commands

```bash
# View logs
railway logs

# Check status
railway status

# Open in browser
railway open
```

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Issues: GitHub Issues

