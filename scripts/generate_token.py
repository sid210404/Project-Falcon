from app.broker.kite_client import KiteBroker

# Paste your request_token here
REQUEST_TOKEN = "b0YyQPXO7YnG4UhQ3NW2Wv6H9M3QkGE2"

broker = KiteBroker()

access_token = broker.generate_session(REQUEST_TOKEN)

print("=" * 60)
print("ACCESS TOKEN")
print("=" * 60)
print(access_token)