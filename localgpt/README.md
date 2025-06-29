# Step 1: Create a GCP VM
Go to Google Cloud Console → Compute Engine > VM Instances.

Click “Create Instance”.

Set the following:

Name: ollama-instance

Region & Zone: your preferred

Machine Type: Choose at least e2-standard-4 (4 vCPU, 16GB RAM). For better performance, use n2-standard-8 or higher.

Boot disk:

OS: Ubuntu 22.04 LTS

Disk size: at least 50GB SSD

Under Firewall, check Allow HTTP and HTTPS if you plan to expose it externally.

Click Create.

# Step 2: Install Ollama and LLM Models
--install ollama

curl -fsSL https://ollama.com/install.sh | sh

--pull nomic-embed-text

ollama pull nomic-embed-text

--pull llama model

ollama pull llama3.2:3b

# Step 3: Install Python and venv
# Update and install pip/virtualenv
sudo apt update && sudo apt install python3-pip -y

sudo apt install python3-virtualenv

# Clone or upload your app (e.g., via Git or SCP)
git clone https://github.com/your-username/your-streamlit-repo.git
cd your-streamlit-repo

# Create and activate virtual environment
virtualenv venv

source venv/bin/activate

# Install requirements
pip install -r requirements.txt

#Step 4: Run Streamlit App
Update ~/.streamlit/config.toml to allow external access:

mkdir -p ~/.streamlit

cat <<EOF > ~/.streamlit/config.toml  
[server]  
headless = true  
enableCORS = false  
port = 8501  
address = "0.0.0.0"  
EOF  
