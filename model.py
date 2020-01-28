import logging
from datetime import datetime, date

import time
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import get_history

from db import engine, Session

log = logging.getLogger(__name__)

Base = declarative_base()



class Ticket(Base):
    __tablename__ = 'ticket'
    depart_airport_code = Column(String(3), primary_key=True)
    arrive_airport_code = Column(String(3), primary_key=True)
    depart_date_time = Column(DateTime(), primary_key=True)
    arrive_date_time = Column(DateTime(), primary_key=True)
    airline = Column(String(20), primary_key=True)
    stop_count = Column(Integer, primary_key=True)

    duration = Column(Integer)
    price = Column(Integer)
    search_date_time = Column(DateTime())

    def __str__(self):
        return 'Ticket[%s(%s)->%s(%s) %s %s %s]' % (self.depart_airport_code, self.depart_date_time.strftime('%m-%d %H-%M'),
                                                    self.arrive_airport_code, self.arrive_date_time.strftime('%m-%d %H-%M'),
                                                    self.duration, self.stop_count, self.price)

    __repr__ = __str__


headers = {
    "cookie": "traveller_context=52ca03c6-63a2-4d51-a625-a73cb2a082e9; ssab=AAExperiment_V8:::a&AD_CPM_Urgency_Metric_Experiment_V2:::b&AEP_SEOPageUniversalLinksExperiment_TR_V3:::on&AFS_DayView_Firebase_NPS_V10:::off&ATBT_Spring_Clean_Carhire_Search_Controls_V17:::b&Ads_UseESIAds_V1:::b&Car_AATest_V4:::a&CountriesFooterLinkValues_AddcountryforBRmarket_07_07_2016_55_49_V1:::b&DEAL_Default_To_Two_Guests_V3:::b&FLUX787_QuoteBlacklist_V2:::a&FLUX_GDT2791_SendPriceTraceToMixpanel_V6:::b&FlightsAndroidProdTest_V1:::b&FlightsHeroStraplineLower_PRE_PRODHeroimagechangefortheUSmarket_03_05_2016_00_40_V1:::a&FlightsiOSProdTest_V2:::b&Fss_NewSearchControls_V6:::c&Fss_springclean_datepicker_V5:::b&GDT3332_UseAWSBrowseServiceEndPointOnShelves_V14:::b&HNT_Android_TID_Exponential_Backoff_V5:::on&Hfe_OfficialPartner_It2_V2:::b&Hfe_PricePerNight_V2:::b&Hotel_Sorting_Impact_Factors_V7:::b&Hsc_ChildrenAgeView_V10:::b&Hsc_MexicanToAS2_V4:::b&Mexico_Etnio_Interview_Screener_01_V1:::b&OTR_ImageShare_UseDeepLinkGenerator_V9:::on&STARK_iOS_UseWalletAssetServiceForLoyaltyCards_V7:::on&TCS_Send_Searching_Email_V4:::b&Trex_OCFlexSuggestions_V23:::a&Trex_OCSearchControls_V41:::b&Trex_OCSearchControls_DayView_V9:::b&TripsTopicPage_Hidethetopicpage_27_02_2018_34_33_V1:::b&UseSkippyLogging_V3:::b&UtidTravellerIdentity_V11:::b&VES_Android_CountryEverywhereFeed_V12:::on&WPT_React16_upgrade_V2:::a&WPT_SkipRequestAshx_V2:::a&Web_Migration_flights_day_view_V7:::b&appinsp_VES_USE_BROWSE_PROXY_V4:::on&branch_banner_oc_version_V28:::new&dbook_cath_trafficcontrol_all_web_V2:::a&dbook_drag_trafficcontrol_all_web_V2:::a&dbook_flot_trafficcontrol_ru_web_V2:::a&dbook_sune_trafficcontrol_web_V3:::a&dbook_tkru_trafficcontrol_ru_web_V2:::a&fbw_transliterate_names_V1:::a&fps_lus_client_quote_service_split_traffic_V225:::b&fps_lus_qes_split_traffic_V22:::a&fps_lus_qss_automatic_rules_V19:::a&fps_lus_send_quotes_to_slipstream_V25:::noexperiment&fps_mbmd_V11:::b&fps_quoteretrieval_aws_V115:::aws&fps_route_summary_traffic_shift_V6:::b&fss_Thor_TrafficTest_V30:::b&glu_springCleanRollout_V2:::a&rts_magpie_soow_data_collection_V5:::budget&rts_wta_shadowtraffic_V367:::b&scaffold_wireup_dont_delete_V1:::b; abgroup=72986736; ssculture=locale:::ru-RU&market:::RU&currency:::RUB; akaas_flights_day_view=1532355788~rv=31~id=43917b56c7b2dec1498227dba1f8954d; scanner=currency:::RUB&adultsV2:::1&childrenV2&from:::MOSC&to:::LED&fromCy:::RU&toCy:::RU&legs:::MOSC|2018-09-01|LED&oym:::1809&oday:::01&wy:::0&tripType:::one-way&cabinclass:::Economy&preferDirects; ASP.NET_SessionId=9lo12bkkv; firstvisit=overlay:::show; preferences=3d368559a26f40b287e8fbf82ba038de; ver=28; settings=acql:::true; acq=b0536e32-4d85-414f-b310-7a1c3ec3dd64|b0536e32-4d85-414f-b310-7a1c3ec3dd64; X-Mapping-rrsqbjcb=xsfzfc7gj3fhyzj1idgotbviqx2wmz9j; _ga=GA1.2.2035660979.1529763780; _gid=GA1.2.1175734101.1529763780; _gat=1; _gat_uatracker=1; mp_2434748954c30ccc5017faa456fa3d38_mixpanel=%7B%22distinct_id%22%3A%20%221642d06d5ef63c-09d427d092baf9-5b183a13-1fa400-1642d06d5f0901%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22User%20Locale%22%3A%20%22RU-RU%22%2C%22User%20Market%22%3A%20%22RU%22%2C%22User%20Currency%22%3A%20%22RUB%22%2C%22New%20User%22%3A%20true%2C%22Internal%20User%22%3A%20%22%22%2C%22Mobile%22%3A%20%22FALSE%22%2C%22Tablet%22%3A%20%22FALSE%22%2C%22OS%20Version%22%3A%20%22NT%206.1%22%2C%22Device%20Model%22%3A%20%22CHROME%20-%20WINDOWS%22%2C%22Browser%20Version%22%3A%20%2267.0.3396.87%22%2C%22Microsite%22%3A%20%22SOL%22%2C%22Cookie%20Policy%20Alert%20Acknowledged%22%3A%20false%7D",
    "x-skyscanner-devicedetection-istablet": "false",
    "origin": "https://www.skyscanner.ru",
    "accept-encoding": "gzip, deflate, br",
    "x-skyscanner-mixpanelid": "1642d06d5ef63c-09d427d092baf9-5b183a13-1fa400-1642d06d5f0901",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "x-skyscanner-traveller-context": "52ca03c6-63a2-4d51-a625-a73cb2a082e9",
    "x-skyscanner-viewid": "5e0b6c29-940c-42c3-bb4c-132b64d9e38d",
    "x-requested-with": "XMLHttpRequest",
    "content-length": "297",
    "skyscanner-utid": "52ca03c6-63a2-4d51-a625-a73cb2a082e9",
    "x-distil-ajax": "azezcavtdrrxfqrtbw",
    "x-skyscanner-channelid": "website",
    "x-skyscanner-devicedetection-ismobile": "false",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "content-type": "application/json; charset=UTF-8",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "referer": "https://www.skyscanner.ru/transport/flights/mosc/led/180901/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home",
}
url = 'https://www.skyscanner.ru/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner&' \
      'response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs%3B_flights_availability&force_fps=aws'


def task(date, depart, arrive, requests, max_price=15000, max_stops=3):
    if depart == arrive:
        return
    for m in range(1, 10):
        try:
            log.info('Processing {} {} {} try {}'.format(depart, arrive, date, m))
            data = {"market": "RU",
                    "currency": "RUB",
                    "locale": "ru-RU",
                    "cabin_class": "economy",
                    "prefer_directs": False,
                    "trip_type": "one-way",
                    "legs": [{"origin": depart, "destination": arrive, "date": date.strftime('%Y-%m-%d')}],
                    "adults": 1,
                    "child_ages": [],
                    "options": {"include_unpriced_itineraries": True, "include_mixed_booking_options": True}}
            log.debug('post: {} data: {}'.format(url, data))
            # with open('start', 'w') as f:
            #     f.write(json.dumps(data, indent=2))
            response = requests.post(url, json=data, headers=headers)
            if response.status_code != 200:
                log.debug('response {}'.format(response.status_code))
                continue
            data = response.json()
            session_id = data['context']['session_id']
            if is_pending(data):
                for i in range(1, 10):
                    time.sleep(10)
                    log.info('Processing {} {} {} try {}'.format(depart, arrive, date, i))
                    log.debug('post: {}'.format(url))
                    response = requests.get('https://www.skyscanner.ru/g/conductor/v1/fps3/search/{}'
                                            '?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs%3B_flights_availability&'
                                            'force_fps=aws&_=1529877736386'.format(session_id),
                                            headers={'x-gateway-servedby': response.headers['x-gateway-servedby'],
                                                     'x-skyscanner-channelid': 'website',
                                                     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
                    data = response.json()
                    if response.status_code != 200:
                        log.debug('response {}'.format(response.status_code))
                        continue
                    if not is_pending(data):
                        break
            store(filter_out(parse(data, Ticket), max_price, max_stops))
            return
        except Exception as ex:
            log.exception('Exception')
        log.info('Error processing {} {} {} try {}'.format(depart, arrive, date, m))


def filter_out(tickets, max_price, max_stops):
    prev_len = len(tickets)
    tickets = list(filter(lambda ticket: ticket.stop_count < max_stops and ticket.price < max_price, tickets))
    log.info('Filtering out before:{} after:{}'.format(prev_len, len(tickets)))
    return tickets


def is_pending(data):
    agents = data.get('agents')
    if not agents:
        log.warning('got capcha')
        return 1
    agents_pending = [agent['update_status'] == 'pending' for agent in agents].count(True)
    log.info('itineraries:{} legs:{} carriers:{} agents:{}(pending:{}) places:{}'.format(len(data["itineraries"]), len(data["legs"]), len(data["carriers"]),
                                                                                         len(agents), agents_pending, len(data["places"])))
    return agents_pending


def store(tickets):
    session = Session()
    try:
        #log.info('Storing {} tickets'.format(len(tickets)))
        for ticket in tickets:
            changes = changeset(session.merge(ticket))
            changes.pop("search_date_time", None)
            if changes:
                log.info('{} updated {} '.format(ticket, ' '.join(['{}(old:{} new:{} {:+.2f})'.format(k, w[0], w[1], w[1]/w[0]*100-100) for k, w in changes.items()])))
            session.commit()
    except Exception:
        log.exception('Exception')
        session.rollback()
    finally:
        session.close()


def parse(data, ticket_class):
    itineraries = data["itineraries"]
    legs = {leg['id']: leg for leg in data["legs"]}
    carriers = {carrier['id']: carrier for carrier in data["carriers"]}
    places = {place['id']: place for place in data["places"]}
    tickets = []
    for itinerary in itineraries:
        ticket = ticket_class()
        tickets.append(ticket)
        ticket.search_date_time = datetime.now()
        ticket.price = int(itinerary['pricing_options'][0]['price']['amount'])
        ticket.id = itinerary['id']
        leg = legs[ticket.id]
        ticket.depart_date_time = datetime.strptime(leg['departure'], "%Y-%m-%dT%H:%M:%S")
        ticket.arrive_date_time = datetime.strptime(leg["arrival"], "%Y-%m-%dT%H:%M:%S")
        ticket.stop_count = int(leg["stop_count"])
        ticket.duration = int(leg["duration"])

        depart_place = places[leg["origin_place_id"]]
        arrive_place = places[leg["destination_place_id"]]
        ticket.depart_airport_code = depart_place["display_code"]
        ticket.arrive_airport_code = arrive_place["display_code"]

        ticket.airline = ' '.join(carriers[marketing_id]['display_code'] for marketing_id in leg["marketing_carrier_ids"])

    return tickets


def changeset(obj):
    changes = {}
    for prop in obj.__mapper__.iterate_properties:
        history = get_history(obj, prop.key)
        if history.has_changes():
            old_value = history.deleted[0] if history.deleted else None
            new_value = history.added[0] if history.added else None
            if old_value and new_value:
                changes[prop.key] = (old_value, new_value)
    return changes


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    import requests

    task(date(2019, 4, 22), 'LED', 'PRG', requests)
