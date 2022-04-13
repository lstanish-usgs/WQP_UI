import urllib.parse

from bs4 import BeautifulSoup
from flask import request, make_response
import markdown
from markdown.extensions.toc import TocExtension
import pandas as pd

from . import app, session


def create_request_resp_log_msg(response):
    """
    Generate a string for logging results of web service requests
    from the requests package.

    :param requests.Response response: a requests Response object
    :return: a string that can be used in a logging statement
    :rtype: str

    """
    msg = 'Status Code: {0}, URL: {1}, Response headers: {2}'.format(response.status_code,
                                                                     response.url,
                                                                     response.headers)
    return msg


def get_markdown(md_path):
    """
    Load text from static markdown files
    :param md_path: the path of associated markdown file
    :return: the markdown converted to HTML
    """
    md = markdown.Markdown(
        extensions=[TocExtension(baselevel=1), 'markdown.extensions.tables', 'markdown.extensions.md_in_html'],
        output_format="html5"
    )
    with open(md_path, 'r') as f:
        text = f.read()
        html = md.convert(text)

        # Create sidebar from md.toc
        # Remove final div in the feed
        sidebar_toc = BeautifulSoup(md.toc, 'html.parser')

        feed_div = sidebar_toc.find('div', class_='toc')
        child_divs = feed_div.find('ul')
        links = str(child_divs).replace('<li>', '<li class=\'usa-sidenav__item\'>')
        final = links.replace('<ul>', '<ul class=\'usa-sidenav\'>', 1)
        table_of_contents = final.replace('<ul>', '<ul class=\'usa-sidenav__sublist\'>')

        # Create page body
        body = BeautifulSoup(html, 'html.parser')

        # For every image, add static root to src
        for img in body.findAll('img'):
            root_path = app.config['STATIC_ROOT']

            if root_path.endswith('/'):
                img['src'] = app.config['STATIC_ROOT'] + img['src']
            else:
                img['src'] = app.config['STATIC_ROOT'] + '/' + img['src']

        return {'body': body, 'toc': table_of_contents}


def geoserver_proxy_request(target_url, cert_verification):
    """
    :param target_url:
    :param cert_verification:
    :return:
    """
    if request.method == 'GET':
        resp = session.get(target_url + '?' + request.query_string.decode("utf-8"), verify=cert_verification)
        # This fixed an an ERR_INVALID_CHUNKED_ENCODING when the app was run on the deployment server.
        if 'transfer-encoding' in resp.headers:
            del resp.headers['transfer-encoding']
        # This fixed an net::ERR_CONTENT_DECODING_FAILED
        if 'content-encoding' in resp.headers:
            del resp.headers['content-encoding']

    else:
        resp = session.post(target_url, data=request.data, headers=request.headers, verify=cert_verification)
        if 'content-encoding' in resp.headers:
            del resp.headers['content-encoding']
    msg = create_request_resp_log_msg(resp)
    app.logger.info(msg)
    return make_response(resp.content, resp.status_code, resp.headers.items())


def retrieve_lookups(code_uri, params=None):
    """
    :param code_uri: string - The part of the url that identifies what kind of information to lookup. Should start with a slash
    :param params: dict - Any query parameters other than the mimeType that should be sent with the lookup
    :return: list of dictionaries representing the json object returned by the code lookup. Return None if
        the information can not be retrieved
    """
    local_params = dict(params or {})
    local_params['mimeType'] = 'json'
    resp = session.get(app.config['CODES_ENDPOINT'] + code_uri, params=local_params)
    msg = create_request_resp_log_msg(resp)
    if resp.status_code == 200:
        app.logger.debug(msg)
        lookups = resp.json()
    else:
        app.logger.info(msg)
        lookups = None
    return lookups


def retrieve_providers():
    """
    :return: list of strings - one string for each provider. Return None if the information can't be retrieved
    """
    provider_lookups = retrieve_lookups('/providers')
    if provider_lookups:
        try:
            providers = [code['value'] for code in provider_lookups.get('codes')]
        except TypeError as e:
            app.logger.warning(repr(e))
            providers = None
    else:
        providers = None
    return providers


def retrieve_organization(provider, org_id):
    """
    :param org_id: string identifying a WQP organization value
    :return: dictionary containing id and name properties if such an org exists, an empty
        dictionary if no such org exists or None if no information can be retrieved.
    """
    organization_lookups = retrieve_lookups('/organization', {'text': org_id})
    if organization_lookups:
        try:
            org_codes = organization_lookups.get('codes')
            # org_id must be exact match to value and provider must be in the provider value
            provider_org_codes = [org_code for org_code in org_codes if provider in org_code.get('providers', '').split(' ')]
            organization = {}
            for code in provider_org_codes:
                if code.get('value', '') == org_id:
                    organization = {'id' : org_id, 'name': code.get('desc', '')}
                    break
        except TypeError as e:
            app.logger.warning(repr(e))
            organization = None
    else:
        organization = None
    return organization


def retrieve_organizations(provider):
    """
    :param provider: string - retrieve organizations belonging to provider
    :return: list of dictionaries or None. Each dictionary contains id and name keys representing an organization.
        None is returned if no information can be retrieved.
    """

    organization_lookups = retrieve_lookups('/organization')
    if organization_lookups:
        try:
            org_codes = organization_lookups.get('codes')
            provider_org_codes = [org_code for org_code in org_codes if provider in org_code.get('providers', '').split(' ')]
            organizations = [{'id': org_code.get('value', ''), 'name' : org_code.get('desc', '')} for org_code in provider_org_codes]
        except TypeError as e:
            app.logger.warning(repr(e))
            organizations = None

    else:
        organizations = None
    return organizations


def retrieve_county(country, state, county):
    """
    :param country: string - two letter country abbreviation
    :param state string - states fips code
    :param county: - county fips code

    :return: dictionary - with StateName and CountyName properties, an empty dictionary if no county exists or
        None if no information can be retrieved
    """
    statecode = country + ':' + state
    countycode = statecode + ':' + county
    county_lookups = retrieve_lookups('/countycode', {'statecode': statecode, 'text': countycode})

    if county_lookups and 'recordCount' in county_lookups:
        if county_lookups.get('recordCount') == 1 and 'codes' in county_lookups:
            country_state_county = county_lookups.get('codes', [{}])[0].get('desc', '').split(',')
            if len(country_state_county) > 2:
                county_data = {'StateName': country_state_county[1], 'CountyName': country_state_county[2]}
            else:
                county_data = {}
        else:
            county_data = {}
    else:
        county_data = None

    return county_data


def retrieve_sites_geojson(provider, org_id):
    """
    :param provider: string
    :param org_id: string
    :return: python object representing the geojson object containing the sites which are in the provider and org_id.
        Return an empty object if the org_id does not exist in provider.
        Return None if the information can not be retrieved.
    """
    resp = session.get(
        app.config['SEARCH_QUERY_ENDPOINT'] + 'Station/search',
        params={
            'organization': org_id,
            'providers': provider,
            'mimeType': 'geojson',
            'sorted': 'no',
            'minresults': 1,  # exclude stations with no results
            'uripage': 'yes'  # This is added to distinguish from normal web service queries
        }
    )
    if resp.status_code == 200:
        sites = resp.json()
    elif resp.status_code == 400:
        sites = {}
    else:
        msg = create_request_resp_log_msg(resp)
        app.logger.warning(msg)
        sites = None
    return sites


def retrieve_site(provider_id, organization_id, site_id):
    """
    :param provider_id: string
    :param organization_id: string
    :param site_id: string
    :return: dictionary representing the requested site, empty dictionary if no site exists, or None if the site data can not be returned.
    """

    resp = session.get(app.config['SEARCH_QUERY_ENDPOINT'] + 'Station/search',
                       params={'organization': organization_id,
                               'providers' : provider_id,
                               'siteid': site_id,
                               'mimeType' : 'tsv',
                               'sorted': 'no',
                               'uripage': 'yes'})  # This is added to distinguish from normal web service queries
    msg = create_request_resp_log_msg(resp)
    if resp.status_code == 200 and resp.text:
        app.logger.debug(msg)
        resp_lines = resp.text.split('\n')
        if len(resp_lines) > 1:
            headers = resp_lines[0].split('\t')
            site = dict(zip(headers, resp_lines[1].split('\t')))

        else:
            site = {}

    elif resp.status_code == 400:
        app.logger.info(msg)
        site = {}

    else:
        app.logger.warning(msg)
        site = None
    return site


def get_summary_with_pandas_package(url):
    """
    Helper function, uses Pandas CVS function to open a CSV file and convert to a Pandas DataFrame
    :param url: The URL of the CSV file to download
    :return: Pandas Dataframe with contents of CSV file
    """
    return pd.read_csv(url)


def get_summary_dataframe(period_of_record_summary_data):
    """
    Function does the following -
    1) The data call returns mostly unneeded data, so starts by keeping only the needed columns.
    2) Adds new columns for the start and end years of the period of record by grabbing the minimum and maximum values
        for each characteristic group from the YearSummarized. Note: Every 'year summarized' has its own row in the
        data at this point. The 'startYear' and 'endYear' values will be the same for every row in within a group
        of 'characteristicType' rows of the same type.
    3) Uses the min function to keep only one row in each characteristic group.
    4) Cleans up by dropping the unneeded 'YearSummarized' column.
    :param period_of_record_summary_data: a Pandas DataFrame containing period of record information for data groups
    :return: Pandas Dataframe grouped by CharacteristicType with columns for start and end of period of record
    """

    if len(period_of_record_summary_data.index) >= 1:
        period_of_record_summary_data = period_of_record_summary_data[['CharacteristicType', 'YearSummarized']]
        period_of_record_summary_data['startYear'] = \
            period_of_record_summary_data.groupby('CharacteristicType')['YearSummarized'].transform('min')
        period_of_record_summary_data['endYear'] = \
            period_of_record_summary_data.groupby('CharacteristicType')['YearSummarized'].transform('max')
        one_row_for_each_characteristic_group = \
            period_of_record_summary_data.groupby('CharacteristicType').min('YearSummarized')
        characteristic_group_summary = one_row_for_each_characteristic_group.drop('YearSummarized', 1)
    else:
        characteristic_group_summary = None

    return characteristic_group_summary


def get_site_summary_data_with_period_of_record(site_id):
    """
    A coordinating function that gets a CSV file from Water Quality Portal, converts it to a Pandas Dataframe, removes
    the extraneous data, finds the start and end of the period of record and returns the Dataframe
    :param site_id: An identifier for the monitoring location
    :return: Pandas Dataframe grouped by CharacteristicType with columns for start and end of period of record
    """
    summary_csv_url = f"{app.config['SITE_SUMMARY_ENDPOINT']}?siteid={urllib.parse.quote(site_id)}&dataProfile=periodOfRecord&" \
                      f"summaryYears=all&mimeType=csv&zip=no"
    period_of_record_summary_data = get_summary_with_pandas_package(summary_csv_url)
    return get_summary_dataframe(period_of_record_summary_data)
