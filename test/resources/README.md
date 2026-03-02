## In this folder we have real world responses for requests with the following parameters

Some of this is pseudo-code in the sense that I don't actually know if marketIds are in quotes and of course datetime functions are evaluated and not sent as literal text. 

**The purpose of this is to explain responses and help create mock services**

**listMarketBook:**

        market_book_params = {
            "marketIds": ["1.254675032"],
            "priceProjection": {
                "priceData": ["EX_BEST_OFFERS"]
            }
        }

**listEvents:**
 
is a collection of responses for two hockey searches and one soccer search. The API returns only one response, not all of them together like they are in the file.

Hockey games are with eventTypeId 7524, soccer games are eventTypeId 1. You will recognize soccer events as they are all Freiburg games. Note that search for Freiburg did indeed return a list, not only one event.

    event_filter = {
        "filter": {
            "eventTypeIds": [7524],
            "textQuery": "detroit",
            "marketStartTime": {
                "from": (datetime.datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

        event_filter = {
        "filter": {
            "eventTypeIds": [1],
            "textQuery": "Freiburg",
            "marketStartTime": {
                "from": (datetime.datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

**listMarketCatalogue:**

    market_filter = {
        "filter": {
            "eventIds": [1.254675032],
            "marketTypeCodes": ["RT_MATCH_ODDS","MATCH_ODDS"]
        },
        "maxResults": "1",
        "marketProjection": ["RUNNER_DESCRIPTION"]
    }