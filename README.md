# 🌦️ MCP Weather Server

This project builds a simple **MCP weather server** using Python, then connects it to an MCP-compatible host like **Claude for Desktop**.


---

## ✅ Requirements

- **Python 3.10+** → [Download here](https://www.python.org/downloads/)
- **VS Code** with the Python extension → [Download here](https://code.visualstudio.com/)
- **Claude for Desktop** → [Download here](https://claude.ai/download)

---

## 🛠️ Step-by-Step Setup

### ✅ Step 1: Install `uv` (Python package manager)

Open **PowerShell** (as Administrator) and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

⚠️ Restart your terminal afterwards to activate the `uv` command.

---

### ✅ Step 2: Create and Set Up the Project

- Create a new folder (name it anything).
- Open the folder in **VS Code**.
- Open the terminal and run the following:

```bash
# Initialize a new MCP project
uv init weather
cd weather

# Create and activate virtual environment
uv venv
.venv\Scripts\activate

# Install required packages
uv add mcp[cli] httpx

# Create the server file
new-item weather.py
```

---

### ✅ Step 3: Build the MCP Weather Server

After running the above commands, a `weather.py` file will be created.

Paste the following code into `weather.py`:

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Helper function
async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# Alert formatter
def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# Alert tool
@mcp.tool()
async def get_alerts(state: str) -> str:
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

# Forecast tool
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

# Start server
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

---

### ✅ Step 4: Run the Server

Run the following command in your terminal:

```bash
uv run weather.py
```

✅  If the server is running properly, the terminal will stay idle — this means it’s listening for commands.

---

## 💻 Connect to Claude for Desktop

### ✅ Step 5.1: Install Claude

👉 [Download Claude for Desktop](https://claude.ai/download)

---

### ✅ Step 5.2: Configure Claude

1. Press `Windows + R`, then type:

```bash
%AppData%\Claude
```

2. Inside the `Claude` folder:
   - Create a file named: `claude_desktop_config.json`
   - Open it in **VS Code**
   - Paste the following (update paths to match your system):

```json
{
  "mcpServers": {
    "weather": {
      "command": "C:\\Users\\oluya\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\Users\\oluya\\python_mcp\\weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

⚠️ Make sure the paths are correct for your system to avoid errors.

---

## ✅ Now You’re All Set!

Let’s test the tools inside Claude.

- Let’s make sure Claude for Desktop is picking up the two tools we’ve exposed in our weather server. You can do this by looking for the “Search and tools”  icon:
- 
![image](https://github.com/user-attachments/assets/aced2efc-1717-46f0-ae8e-a2c0204b47d3)

After clicking on the slider icon, you should see two tools listed:

![image](https://github.com/user-attachments/assets/dea7a9c5-3050-461e-97aa-9d5cccfe3921)

---

## 🌍 Test using CLAUDE I will ask for the CAPE TOWN weather 


![image](https://github.com/user-attachments/assets/fdcc7903-ca96-416b-8a6b-3e55c219a787)

> **Note:** The server currently only checks the weather for **Cape Town**, as it has been hardcoded for this location. To support other locations, you would need to integrate an external API — some of which may require a paid subscription.

---

## 🗽 Example: Test New York (Expected to Fail)

❌ You’ll see that it doesn’t work unless the logic is updated to support broader locations:

![image](https://github.com/user-attachments/assets/8a87b80c-3f08-4e7a-aca8-f8cf3e7bc2e5)




