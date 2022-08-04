from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes,scrap_data_announcements,scrap_data_pointers,scrap_symbols

symbols=scrap_symbols()
symbols=["ACTION"]
for symbol in symbols:
    # przynależności do indeksów
    indexes = scrap_data_indexes(symbol)
    # wskaźniki giełdowe
    pointers = scrap_data_pointers(symbol)
    # komunikaty
    announcements = scrap_data_announcements(symbol)
    print(indexes)
    print(pointers)
    print(announcements)
