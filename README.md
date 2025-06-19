# Instagram Bot

An automated Instagram bot built with Python using the `instagrapi` library. This bot can perform various Instagram activities like following users, interacting with timelines, and more.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Local Development Setup](#local-development-setup)
- [Session Setup](#session-setup)
- [Docker Deployment](#docker-deployment)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Git** - for cloning the repository
- **Docker** - for containerized deployment
- **Docker Compose** - for orchestrating the container
- **Python 3.8+** (optional, for local development)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/myagizmaktav/instagramAutoFollowBotDockerized.git
cd instagramAutoFollowBotDockerized
```

### 2. Directory Structure

After cloning, your project structure should look like this:

```
instaBot/
├── docker-compose.yml
├── Dockerfile
├── index.py
├── requirements.txt
├── follows.json
├── session.json
├── timeline.json
├── LICENSE.md
└── README.md
```

## 💻 Local Development Setup

### 1. Install Python

#### On Windows:
1. **Download Python** from [python.org](https://www.python.org/downloads/)
2. **Run the installer** and make sure to check "Add Python to PATH"
3. **Verify installation**:
   ```cmd
   python --version
   pip --version
   ```

#### On macOS:
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### On Linux (Ubuntu/Debian):
```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### 2. Set Up Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

#### On Windows:
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### 3. Install Required Packages

After activating your virtual environment:

```bash
# Install all required packages from requirements.txt
pip install -r requirements.txt

# Or install packages individually:
pip install instagrapi
pip install python-dotenv
pip install requests
```

### 4. Create Environment Configuration

Create a `.env` file in the project root directory:

```env
# Instagram Credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Bot Configuration
UNFOLLOW_DAY=7
```

### 5. Run the Bot Locally

```bash
# Make sure your virtual environment is activated
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Run the bot
python index.py
```


### 8. Troubleshooting Local Setup

#### Common Issues:

**Python not found:**
```bash
# On Windows, try:
python
# or
py

# On macOS/Linux, try:
python3
```

**Permission denied (Linux/macOS):**
```bash
# Use python3 and pip3 instead of python and pip
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

**Virtual environment not activating:**
```bash
# On Windows, if Scripts folder doesn't exist:
python -m venv venv --clear

# On macOS/Linux, ensure you have the right path:
ls venv/bin/  # Should show activate script
```

**Package installation fails:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then try installing packages again
pip install -r requirements.txt
```

## 🔑 Session Setup

**⚠️ IMPORTANT: You must obtain an Instagram session dump before deploying with Docker!**

### Why Session Setup is Required

Instagram requires authentication to perform any actions. The bot needs a valid session to interact with Instagram's API safely and avoid getting blocked.

### How to Get Session Dump

1. **Clone the repository** and navigate to the project directory

2. **Set up environment variables** - Create a `.env` file with your Instagram credentials:
   ```env
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   UNFOLLOW_DAY=7
   ```

3. **Login via console** - Run the bot locally to authenticate and generate session.json

4. **Use the generated session.json** - After successful login, the session.json file will be created automatically

5. **Deploy with Docker** - Now you can use Docker Compose with the valid session.json file

## 🐳 Docker Deployment

### 1. Build and Start the Container

After setting up your session, deploy the bot using Docker Compose:

```bash
# Build and start the container
docker compose up --build
```

### 2. Run in Background (Detached Mode)

```bash
# Run the bot in the background
docker compose up -d --build
```

### 3. View Logs

```bash
# View real-time logs
docker compose logs -f

# View logs for specific service
docker compose logs instagram-follow-bot
```

### 4. Stop the Bot

```bash
# Stop the bot
docker compose down
```

## 🎯 Usage

### Basic Commands

```bash
# Start the bot
docker compose up

# Restart the bot
docker compose restart

# Stop the bot
docker compose down

# Rebuild and start
docker compose up --build

# View status
docker compose ps
```

### Environment Variables

Create a `.env` file in the project root for configuration:

```env
# Instagram Credentials (if not using session.json)
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
UNFOLLOW_DAY=7

```

## ⚙️ Configuration

### follows.json
Contains the list of users to follow or interaction targets:
```json
{
  "targets": ["username1", "username2"],
  "followed_users": [],
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### timeline.json
Stores timeline interaction data:
```json
{
  "interacted_posts": [],
  "last_timeline_check": "2024-01-01T00:00:00Z"
}
```


## 📊 Monitoring

### View Bot Activity

```bash
# Real-time logs
docker compose logs -f instagram-follow-bot

# Last 100 lines
docker compose logs --tail=100 instagram-follow-bot
```

### Check Container Status

```bash
# List running containers
docker compose ps

# Container resource usage
docker stats
```

## ⚠️ Important Notes

- **Rate Limiting**: Instagram has strict rate limits. The bot includes delays to avoid being blocked.
- **Account Safety**: Use a dedicated Instagram account for botting activities.
- **Terms of Service**: Ensure your usage complies with Instagram's Terms of Service.
- **Session Security**: Keep your `session.json` file secure and never commit it to version control.

## 🛡️ Security Best Practices

1. **Add session.json to .gitignore**:
   ```gitignore
   session.json
   .env
   *.log
   ```

2. **Use environment variables** for sensitive data instead of hardcoding credentials.

3. **Regularly rotate sessions** to maintain security.

## 📝 License

This project is licensed under the terms specified in the [LICENSE.md](LICENSE.md) file.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs: `docker compose logs -f`
3. Ensure your session.json is valid and up-to-date
4. Verify all dependencies are installed correctly

---

**Remember**: Always obtain a valid session dump before deploying with Docker! 🔑 
