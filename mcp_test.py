import asyncio
from weather import get_forecast, get_alerts

async def main():
    print("Getting forecast for Cape Town...")
    forecast = await get_forecast(-33.9249, 18.4241)
    print(forecast)

    print("\nGetting alerts for Western Cape (ZA)...")
    alerts = await get_alerts("WC")  # Note: NWS alerts use US state codes, this will likely return no alerts
    print(alerts)

asyncio.run(main())
