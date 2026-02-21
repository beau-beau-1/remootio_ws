# Remootio WebSocket Integration for Home Assistant

This integration allows you to control Remootio 3 garage doors via the **plain WebSocket API** (firmware 2.51) in Home Assistant.

## Features
- Open, close, stop commands
- Real-time door state updates
- Plain WS connection (port 8080)
- Firmware 2.51 safe AES-HMAC authentication

## Installation via HACS
1. Go to **HACS → Integrations → Custom Repositories → Add**
2. Add the repository (or upload the zip) and select **Integration**
3. Install the integration
4. Restart Home Assistant
5. Configure with **host**, **port** (usually 8080), **API Key**, and **API Secret**

## Notes
- Make sure your Remootio 3 has **Local WebSocket enabled**
- This integration is designed for **firmware 2.51** with plain WS (unencrypted)
- Debug logs appear in **Home Assistant Core logs** if authentication or connection fails
