# gmaps-scrapi

## How to run:
1. run the flask service `python service.py`
2. fetch results using 
`curl -X POST http://127.0.0.1:5000/scrape -H "Content-Type: application/json" -d '{"query": "hotels+kochi"}'`
3. queries <= 15 would be in data.json
