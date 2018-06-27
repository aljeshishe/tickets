import datetime
import pprint
from operator import itemgetter


def parse(data):
    tickets = []
    itineraries = data.get("itineraries", [])
    legs = data.get("legs", [])
    carriers = data.get("carriers", [])
    agents = data.get("agents", [])
    places = data.get("places", [])

    for itinerary in itineraries:
        info = {}
        info['searchDate'] = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        firstitemSeller = itinerary['pricing_options'][0]['agent_ids'][0]
        info["price"] = int(itinerary['pricing_options'][0]['price']['amount'])
        firstitem = itinerary['id']
        info["id"] = firstitem

        for agent in agents:
            if firstitemSeller == agent["id"]:
                info['seller'] = agent["name"]

        for leg in legs:
            if leg["id"].find(firstitem) > -1:
                origin_place_id = leg["origin_place_id"]
                arrival_place_id = leg["destination_place_id"]
                firstitemCarrier = leg["operating_carrier_ids"][0]
                info['depart_date'] = leg['departure']
                info['arrive_date'] = leg["arrival"]
                info['stops'] = int(leg["stop_count"])
                for place in places:
                    if int(place["id"]) == int(origin_place_id):
                        info['depart_airport_code'] = place["display_code"]
                        info['depart_airport'] = place["name"]
                    if int(place["id"]) == int(arrival_place_id):
                        info['arrival_airport_code'] = place["display_code"]
                        info['arrival_airport'] = place["name"]
                for carrier in carriers:
                    if int(carrier["id"]) == int(firstitemCarrier):
                        info['airline'] = carrier["name"]

        tickets.append(info)

    pprint.pprint(sorted(tickets, key=itemgetter('price'), reverse=True))
    return tickets
