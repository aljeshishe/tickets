import datetime
import json
import pprint
import socket
import time
from operator import itemgetter

import requests
from proxies import Proxies
import logging

import skyscanner
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger('proxies').setLevel(logging.WARNING)


headers = {"cookie": "traveller_context=52ca03c6-63a2-4d51-a625-a73cb2a082e9; ssab=AAExperiment_V8:::a&AD_CPM_Urgency_Metric_Experiment_V2:::b&AEP_SEOPageUniversalLinksExperiment_TR_V3:::on&AFS_DayView_Firebase_NPS_V10:::off&ATBT_Spring_Clean_Carhire_Search_Controls_V17:::b&Ads_UseESIAds_V1:::b&Car_AATest_V4:::a&CountriesFooterLinkValues_AddcountryforBRmarket_07_07_2016_55_49_V1:::b&DEAL_Default_To_Two_Guests_V3:::b&FLUX787_QuoteBlacklist_V2:::a&FLUX_GDT2791_SendPriceTraceToMixpanel_V6:::b&FlightsAndroidProdTest_V1:::b&FlightsHeroStraplineLower_PRE_PRODHeroimagechangefortheUSmarket_03_05_2016_00_40_V1:::a&FlightsiOSProdTest_V2:::b&Fss_NewSearchControls_V6:::c&Fss_springclean_datepicker_V5:::b&GDT3332_UseAWSBrowseServiceEndPointOnShelves_V14:::b&HNT_Android_TID_Exponential_Backoff_V5:::on&Hfe_OfficialPartner_It2_V2:::b&Hfe_PricePerNight_V2:::b&Hotel_Sorting_Impact_Factors_V7:::b&Hsc_ChildrenAgeView_V10:::b&Hsc_MexicanToAS2_V4:::b&Mexico_Etnio_Interview_Screener_01_V1:::b&OTR_ImageShare_UseDeepLinkGenerator_V9:::on&STARK_iOS_UseWalletAssetServiceForLoyaltyCards_V7:::on&TCS_Send_Searching_Email_V4:::b&Trex_OCFlexSuggestions_V23:::a&Trex_OCSearchControls_V41:::b&Trex_OCSearchControls_DayView_V9:::b&TripsTopicPage_Hidethetopicpage_27_02_2018_34_33_V1:::b&UseSkippyLogging_V3:::b&UtidTravellerIdentity_V11:::b&VES_Android_CountryEverywhereFeed_V12:::on&WPT_React16_upgrade_V2:::a&WPT_SkipRequestAshx_V2:::a&Web_Migration_flights_day_view_V7:::b&appinsp_VES_USE_BROWSE_PROXY_V4:::on&branch_banner_oc_version_V28:::new&dbook_cath_trafficcontrol_all_web_V2:::a&dbook_drag_trafficcontrol_all_web_V2:::a&dbook_flot_trafficcontrol_ru_web_V2:::a&dbook_sune_trafficcontrol_web_V3:::a&dbook_tkru_trafficcontrol_ru_web_V2:::a&fbw_transliterate_names_V1:::a&fps_lus_client_quote_service_split_traffic_V225:::b&fps_lus_qes_split_traffic_V22:::a&fps_lus_qss_automatic_rules_V19:::a&fps_lus_send_quotes_to_slipstream_V25:::noexperiment&fps_mbmd_V11:::b&fps_quoteretrieval_aws_V115:::aws&fps_route_summary_traffic_shift_V6:::b&fss_Thor_TrafficTest_V30:::b&glu_springCleanRollout_V2:::a&rts_magpie_soow_data_collection_V5:::budget&rts_wta_shadowtraffic_V367:::b&scaffold_wireup_dont_delete_V1:::b; abgroup=72986736; ssculture=locale:::ru-RU&market:::RU&currency:::RUB; akaas_flights_day_view=1532355788~rv=31~id=43917b56c7b2dec1498227dba1f8954d; scanner=currency:::RUB&adultsV2:::1&childrenV2&from:::MOSC&to:::LED&fromCy:::RU&toCy:::RU&legs:::MOSC|2018-09-01|LED&oym:::1809&oday:::01&wy:::0&tripType:::one-way&cabinclass:::Economy&preferDirects; ASP.NET_SessionId=9lo12bkkv; firstvisit=overlay:::show; preferences=3d368559a26f40b287e8fbf82ba038de; ver=28; settings=acql:::true; acq=b0536e32-4d85-414f-b310-7a1c3ec3dd64|b0536e32-4d85-414f-b310-7a1c3ec3dd64; X-Mapping-rrsqbjcb=xsfzfc7gj3fhyzj1idgotbviqx2wmz9j; _ga=GA1.2.2035660979.1529763780; _gid=GA1.2.1175734101.1529763780; _gat=1; _gat_uatracker=1; mp_2434748954c30ccc5017faa456fa3d38_mixpanel=%7B%22distinct_id%22%3A%20%221642d06d5ef63c-09d427d092baf9-5b183a13-1fa400-1642d06d5f0901%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22User%20Locale%22%3A%20%22RU-RU%22%2C%22User%20Market%22%3A%20%22RU%22%2C%22User%20Currency%22%3A%20%22RUB%22%2C%22New%20User%22%3A%20true%2C%22Internal%20User%22%3A%20%22%22%2C%22Mobile%22%3A%20%22FALSE%22%2C%22Tablet%22%3A%20%22FALSE%22%2C%22OS%20Version%22%3A%20%22NT%206.1%22%2C%22Device%20Model%22%3A%20%22CHROME%20-%20WINDOWS%22%2C%22Browser%20Version%22%3A%20%2267.0.3396.87%22%2C%22Microsite%22%3A%20%22SOL%22%2C%22Cookie%20Policy%20Alert%20Acknowledged%22%3A%20false%7D",
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
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        "content-type": "application/json; charset=UTF-8",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "referer": "https://www.skyscanner.ru/transport/flights/mosc/led/180901/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home",
        }

response = requests.post('https://www.skyscanner.ru/dataservices/flights/pricing/v3.0/search?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=deeplink;segment&pageindex=0&pagesize=1',
                         data='{"adults":"1","cabin_class":"economy","children":"0","infants":"0","currency":"RUB","locale":"ru-RU","market":"RU","legs":[{"origin":"MOSC","destination":"LED","date":"2018-09-03","return_date":""}],"options":{"agent_include":["tkru"],"cached_prices_only":false}}',
                         headers=headers)
print(response)
with open('search', 'wb') as f:
    f.write(response.content)


headers={"Host" : "www.skyscanner.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.skyscanner.ru/transport/flights/mosc/led/180909/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home",
        "X-Distil-Ajax": "eeezzzufafevaqaqdyfavv, azezcavtdrrxfqrtbw",
        "Content-Type": "application/json; charset=utf-8",
        "X-Skyscanner-ChannelId": "website",
        "X-Skyscanner-MixPanelId": "46990b68-5e29-4773-aec7-069206f2a718",
        "X-Skyscanner-DeviceDetection-IsMobile": "false",
        "X-Skyscanner-DeviceDetection-IsTablet": "false",
        "X-Skyscanner-ViewId": "46990b68-5e29-4773-aec7-069206f2a718",
        "X-Skyscanner-Traveller-Context": "53b99db7-3c8d-4ea3-b060-4f6a1ec3f70f",
        "Skyscanner-UTID": "53b99db7-3c8d-4ea3-b060-4f6a1ec3f70f",
        "X-Gateway-ServedBy": "gw53.skyscanner.net",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "X-Mapping-rrsqbjcb=0; akaas_flights-home=1532350775~rv=60~id=e41a6779c15f1c7a4b2bc8da2b0a2a1e; traveller_context=53b99db7-3c8d-4ea3-b060-4f6a1ec3f70f; ssab=TurnFeatureTests:::on&Ads_UseESIAds_V1:::b&fps_route_summary_traffic_shift_V6:::b&fps_lus_qes_split_traffic_V22:::b&ray_test_raything_27_06_2017_20_14_V1:::b&fps_lus_qss_automatic_rules_V19:::a&dbook_tkru_trafficcontrol_ru_web_V2:::a&fps_mbmd_V11:::b&Fss_springclean_datepicker_V5:::b&UtidTravellerIdentity_V11:::b&Car_AATest_V4:::b&appinsp_VES_USE_BROWSE_PROXY_V4:::on&glu_springCleanRollout_V2:::a&WPT_SkipRequestAshx_V2:::a&fss_Thor_TrafficTest_V30:::b&dbook_flot_trafficcontrol_ru_web_V2:::a&WPT_React16_upgrade_V2:::a&OTR_ImageShare_UseDeepLinkGenerator_V9:::on&Trex_OCFlexSuggestions_V23:::a&rts_magpie_soow_current_V19:::currentrules&UseSkippyLogging_V3:::b&dbook_cath_trafficcontrol_all_web_V2:::a&raymond_test_14_08_17_V1:::b&Hfe_OfficialPartner_It2_V2:::b&AD_CPM_Urgency_Metric_Experiment_V2:::a&scaffold_wireup_dont_delete_V1:::b&FLUX_GDT2791_SendPriceTraceToMixpanel_V6:::b&Trex_OCSearchControls_V41:::b&Web_Migration_flights_day_view_V7:::a&Web_Migration_home_V10:::b&Web_Migration_month_view_V12:::b&fps_lus_client_quote_service_split_traffic_V225:::b&Hotel_Sorting_Impact_Factors_V7:::c&AAExperiment_V8:::a&fps_lus_send_quotes_to_slipstream_V25:::noexperiment&Fss_NewSearchControls_V6:::c&dbook_drag_trafficcontrol_all_web_V2:::a&Trex_OCSearchControls_DayView_V9:::b&Hsc_MexicanToAS2_V4:::b&ATBT_Spring_Clean_Carhire_Search_Controls_V17:::b&FLUX787_QuoteBlacklist_V2:::b&Hfe_PricePerNight_V2:::b&DEAL_Default_To_Two_Guests_V3:::b&fps_quoteretrieval_aws_V115:::aws&rts_wta_shadowtraffic_V367:::b&Hsc_ChildrenAgeView_V10:::b&TAME_Screenshot_Shares_V1:::b&GDT3332_UseAWSBrowseServiceEndPointOnShelves_V14:::a&branch_banner_oc_version_V28:::new&dbook_sune_trafficcontrol_web_V3:::a&fbw_transliterate_names_V1:::b&TCS_Send_Searching_Email_V4:::b; abgroup=15766617; ssculture=locale:::ru-RU&market:::RU&currency:::RUB; scanner=currency:::RUB&legs:::MOSC%7C2018-09-09%7CLED&to:::LED&oym:::1809&oday:::09&wy:::0&tripType:::OneWayTrip&adults:::1&originalAdults:::1&adultsV2:::1&children:::0&originalChildren:::0&infants:::0&originalInfants:::0&charttype:::1&rtn:::false&preferDirects:::false&includeOnePlusStops:::true&cabinclass:::Economy&ncr:::false&lang:::RU&outboundAlts:::false&inboundAlts:::false&from:::MOSC&usrplace:::RU&fromCy:::RU&toCy:::RU&iym:::&iday:::; ASP.NET_SessionId=wuf71ynr4; firstvisit=overlay:::show; preferences=8471d569f04c4c86b8ec59a532edcaa3; ver=28; settings=acql:::true; acq=99de6cc3-efe6-4b15-abc7-290c6614f81e|99de6cc3-efe6-4b15-abc7-290c6614f81e; akaas_month-view=1532300162~rv=88~id=3ff4f467f9aee7e4815debf5ce1d82dd; akaas_flights-to-city-airport=1532299598~rv=91~id=d74b7471b7de99ab2b0b26a4f23e52f4; X-Mapping-rrsqbjcb=xsfzfc7gj3fhyzj1idgotbviqx2wmz9j; X-Mapping-fpkkgdlh=E07AE8F9D4982DCC13DBCDFD087E69F9; ssassociate=; akaas_flights_day_view=1532352539~rv=82~id=e944d3bbbe2535e31915983d015c06ad; DAPROPS=\"bjs.webGl:1|bjs.geoLocation:1|bjs.webSqlDatabase:0|bjs.indexedDB:1|bjs.webSockets:1|bjs.localStorage:1|bjs.sessionStorage:1|bjs.webWorkers:1|bjs.applicationCache:1|bjs.supportBasicJavaScript:1|bjs.modifyDom:1|bjs.modifyCss:1|bjs.supportEvents:1|bjs.supportEventListener:1|bjs.xhr:1|bjs.supportConsoleLog:1|bjs.json:1|bjs.deviceOrientation:0|bjs.deviceMotion:1|bjs.touchEvents:0|bjs.querySelector:1|bjs.battery:0|bhtml.canvas:1|bhtml.video:1|bhtml.audio:1|bhtml.svg:1|bhtml.inlinesvg:1|bcss.animations:1|bcss.columns:1|bcss.transforms:1|bcss.transitions:1|idisplayColorDepth:24|bcookieSupport:1|sdevicePixelRatio:1|sdeviceAspectRatio:16/9|bflashCapable:0|baccessDom:1|buserMedia:1\"; D_IID=E3979077-34D9-36F2-A452-B275A69E6964; D_UID=9A52FBF8-5BB5-3D9A-A4DE-53D85B711E7F; D_ZID=ADA6C94C-3D37-3C2A-866A-94C611F532E1; D_ZUID=66F68B8E-F73D-3405-999D-C2FDECA8FA56; D_HID=AA351C16-6F53-34A5-AF6E-54438674F872; D_SID=5.19.160.173:qXZt4vUgUKhdDBvTODicEk/G1ZIj5lzXer22gcU/T7g; akaas_skippy_aws_migration=1532301070~rv=29~id=03becd0d9c041d0363cff88b78925f2a; akaas_skippy_tags=1532301069~rv=72~id=685ea27d1eb009955fb332dc535febb8; X-Mapping-indojeag=67A627FEEA0ECEE5A2A10B355E036061; has_app=; utm_source=",
        "Connection": "keep-alive"}
response = requests.get('https://www.skyscanner.ru/g/conductor/v1/fps3/search/7c16982e-215b-465c-8eb0-51963cb5589?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query;deeplink;segment;stats;fqs;pqs;_flights_availability&force_fps=aws&_=1529760530262',
             headers=headers)
print(response)
with open('search', 'wb') as f:
    f.write(response.content)
parse(response.json())
proxies = Proxies()



for i in range(1000):
    proxy = proxies.get()
    log.info('Got proxy {}'.format(proxy))
    try:
        start = time.time()
        response = requests.get('http://ya.ru',
                                proxies={'http': 'http://%s:%s' % (proxy.host, proxy.port)},
                                timeout=(5, 10),
                                headers={'User-Agent': 'PxBroker/0.2.0/5954'})

        seconds = time.time() - start
        log.info('Using %s %s %s %3.3f' % (proxy, response.status_code, len(response.content), seconds))
        proxies.put_back(proxy, seconds)
        response.raise_for_status()
    except (socket.timeout, requests.exceptions.RequestException):
        log.exception('Got exception')
        proxies.put_back(proxy, 100)


# urllib3.exceptions.ConnectTimeoutError
# urllib3.exceptions.MaxRetryError
# requests.exceptions.ConnectTimeout
# ConnectionRefusedError
# urllib3.exceptions.NewConnectionError
# requests.exceptions.ProxyError
# urllib3.exceptions.ReadTimeoutError
# requests.exceptions.ReadTimeout
# ConnectionResetError
# http.client.RemoteDisconnected
# requests.exceptions.HTTPError: 503 Server Error: