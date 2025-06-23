from pyngrok import ngrok

# Specify the port your API is running on
port = 8000

# Start the ngrok tunnel
public_url = ngrok.connect(port)
print(f"Your API is publicly available at: {public_url}")

# Keep the script running
input("Press Enter to terminate the tunnel...")
