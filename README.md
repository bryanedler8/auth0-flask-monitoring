# CST8919-Assignment 1



**Student Name**: Bryan Edler  
**Student ID**: 041016930  
**Course**: 26S_CST8919_300 DevOps - Security and Compliance
**Semester**: Summer 2026  



## Demo Video

🎥 [Watch Demo Video](https://youtu.be/QXbagwd9NCE)

---

Here's a brief but comprehensive README.md that covers all the lab requirements:

```markdown
# 🔐 Auth0 Flask App with Azure Monitoring

## 📋 Lab Overview
This project is a secure Flask application with Auth0 SSO authentication, deployed on Azure App Service. It includes structured security logging, Azure Monitor integration with KQL queries, and automated alerts for detecting suspicious activity.

## 🎯 Lab Requirements Fulfilled
- ✅ Auth0 SSO authentication with Flask
- ✅ Structured security logging (logins, protected route access, unauthorized attempts)
- ✅ Deployed to Azure App Service (Python 3.10)
- ✅ KQL query for detecting excessive access (>10 in 15 minutes)
- ✅ Azure Alert with email notification
- ✅ GitHub repository with documentation and test files

## 🛠️ Tech Stack
- **Backend**: Python 3.10, Flask
- **Authentication**: Auth0 (OAuth2/SSO)
- **Cloud**: Azure App Service (Linux, B1 tier)
- **Monitoring**: Azure Log Analytics, KQL
- **Logging**: Structured logging with `SECURITY_EVENT` prefix

## 📁 Project Structure
```
auth0-flask-monitoring/
├── app.py              # Main Flask app with security logging
├── auth.py             # Auth0 authentication configuration
├── requirements.txt    # Python dependencies
├── startup.sh          # Azure startup script
├── test-app.http       # HTTP test requests
├── simulate_traffic.py # Traffic simulation script
├── templates/          # HTML templates
│   ├── index.html
│   ├── profile.html
│   └── protected.html
├── static/             # Static assets
└── README.md           # This file
```

##  Local Setup

### Prerequisites
- Python 3.10+
- Auth0 account
- Azure subscription

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/auth0-flask-monitoring.git
cd auth0-flask-monitoring

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your Auth0 credentials

# 5. Run locally
python app.py
# Visit http://localhost:5000
```

## ☁️ Azure Deployment

### Deploy from GitHub (Recommended)
1. Create Azure Web App (Python 3.10, Linux, B1 tier)
2. Set environment variables in Azure:
   ```
   AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, 
   AUTH0_SECRET, AUTH0_REDIRECT_URI
   ```
3. Deploy using GitHub Actions or Azure CLI:
   ```bash
   az webapp deploy --resource-group auth0-flask-rg \
     --name auth0-flask-monitor --src-path deploy.zip --type zip
   ```

### Update Auth0 Callback URLs
Add to Auth0 Application Settings:
- **Allowed Callback URLs**: `http://localhost:5000/callback, https://YOUR-APP.azurewebsites.net/callback`
- **Allowed Logout URLs**: `http://localhost:5000, https://YOUR-APP.azurewebsites.net`

## 📊 Monitoring & Detection

### KQL Query
Detects users accessing `/protected` more than 10 times in 15 minutes:
```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where Message contains "SECURITY_EVENT"
| where Message contains "protected_access"
| extend UserEmail = extract("\"email\": \"([^\"]+)\"", 1, Message)
| extend UserId = extract("\"user_id\": \"([^\"]+)\"", 1, Message)
| extend Route = extract("\"route\": \"([^\"]+)\"", 1, Message)
| where Route == "/protected"
| summarize AccessCount = count() by UserEmail, UserId
| where AccessCount > 10
| project UserEmail, UserId, AccessCount
| order by AccessCount desc
```

### Azure Alert Configuration
- **Alert Rule**: Excessive Protected Route Access
- **Condition**: When query result count > 0
- **Frequency**: Every 5 minutes
- **Action Group**: Email notification
- **Severity**: 3 (Low)

## 🧪 Testing & Traffic Simulation

### Manual Testing
1. Visit deployed app: `https://YOUR-APP.azurewebsites.net`
2. Login with Auth0
3. Access `/protected` 15+ times
4. Check logs in Azure Log Stream

### Automated Traffic Simulation
```bash
# Run the simulation script
python simulate_traffic.py
# Follow prompts to enter session cookie
```


## 📝 Submission Checklist
- [ ] App deployed to Azure App Service
- [ ] Auth0 login working on Azure
- [ ] SECURITY_EVENT logs visible in Azure Log Stream
- [ ] KQL query detects excessive access
- [ ] Azure Alert configured and email received
- [ ] GitHub repo public with all files
- [ ] YouTube demo recorded (10 min max)
- [ ] Brightspace submission complete


---

## 📝 Key Sections to Customize

1. **Replace `YOUR-USERNAME`** with your GitHub username
2. **Replace `YOUR-APP.azurewebsites.net`** with your actual Azure app URL
3. **Replace `YOUR_VIDEO_ID`** with your YouTube video ID
4. **Replace `[Your Name]`** with your actual name
5. **Add your actual deployment URL** in the "Azure Deployment" section

---

## 📋 What This README Covers

| Lab Requirement | README Section |
|-----------------|----------------|
| Setup steps (Auth0, Azure, .env) | Local Setup, Azure Deployment |
| Explanation of logging | Project Structure, Monitoring |
| KQL query | Monitoring & Detection |
| Alert logic | Monitoring & Detection |
| Test file | Testing & Traffic Simulation |
| GitHub repo structure | Project Structure |
| YouTube demo link | Demo Video |

---


