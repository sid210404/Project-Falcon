from app.data.instrument_service import InstrumentService

service = InstrumentService()

symbol = input("Enter Symbol: ").upper()

print()

print(service.get_details(symbol))