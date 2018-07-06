import json
import time

import requests
from model import parse, Ticket, is_pending
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
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
    # ":path": "/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs%3B_flights_availability&force_fps=aws",
    "skyscanner-utid": "52ca03c6-63a2-4d51-a625-a73cb2a082e9",
    "x-distil-ajax": "azezcavtdrrxfqrtbw",
    "x-skyscanner-channelid": "website",
    "x-skyscanner-devicedetection-ismobile": "false",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "content-type": "application/json; charset=UTF-8",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "referer": "https://www.skyscanner.ru/transport/flights/mosc/led/180901/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home",
    # ":authority": "www.skyscanner.ru",
    # ":scheme": "https",
    # ":method": "POST"
}

response = requests.post(
    'https://www.skyscanner.ru/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs%3B_flights_availability&force_fps=aws',
    json={"market": "RU",
          "currency": "RUB",
          "locale": "ru-RU",
          "cabin_class": "economy",
          "prefer_directs": False,
          "trip_type": "one-way",
          "legs": [{'origin': 'MOSC', 'destination': 'CIA', 'date': '2018-07-30'}],
          "adults": 1,
          "child_ages": [],
          "options": {"include_unpriced_itineraries": False, "include_mixed_booking_options": True}},
    headers=headers)

log.info(response)
data = response.json()
with open('start', 'w') as f:
    f.write(json.dumps(data, indent=2))
while is_pending(data):
    time.sleep(10)
    headers = {
        'x-gateway-servedby': response.headers['x-gateway-servedby'],
        'x-skyscanner-channelid': 'website',
    }
    session_id = data['context']['session_id']
    response = requests.get('https://www.skyscanner.ru/g/conductor/v1/fps3/search/{}?geo_schema=skyscanner&carrier_schema=skyscanner'
                            '&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs%3B_flights_availability&force_fps=aws&_=1529877736386'.format(session_id),
        headers=headers)
    print(response)
    data = response.json()
    with open('conductor', 'w') as f:
        f.write(json.dumps(data, indent=2))
log.info('found %s' % (len(parse(data, Ticket))))
