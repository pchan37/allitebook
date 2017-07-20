import bs4
import urllib2

from lib.Logging import Logger

web_logger = Logger.Logger('web.log')

def get_source(link, bs4_format=False):
    '''
    Retrieve the page source

    Retrieve the source of the given link as a BeautifulSoup object or simple text.

    Args:
        link (str): the url to retrieve the source for
        bs4_format (bool, optional): toggle to return as BeautifulSoup object or
            not, defaults to False

    Returns:
        BeautifulSoup: the source of the page if bs4_format is True
        str: the source of the page if bs4_format is False
    '''
    proper_encoded_link = link.replace(' ', '%20')
    request = urllib2.Request(proper_encoded_link, headers={'User-Agent': 'Mozilla/5.0'})
    connection = urllib2.urlopen(request)
    page_content = connection.read()
    if bs4_format:
        return bs4.BeautifulSoup(page_content, 'html.parser')
    else:
        return page_content

_1KB = 1024
_1MB = 1024 * _1KB
def download_page(download_link, CHUNK_SIZE=_1MB):
    '''
    Download file

    Download the file from the given download link in chunks.  In the case of
    HTTPErrors or URLErrors, log the error and return None.

    Args:
        download_link (str): the url to retrieve the file from
        CHUNK_SIZE (int, optional): size of each data chunk, defaults to 1 MB

    Returns:
        str: content of the downloaded file
        None: file was not downloaded due to HTTPError or URLError

    Raises:
        Exception: Something went terribly wrong...
    '''
    try:
        proper_encoded_download_link = download_link.replace(' ', '%20')
        request = urllib2.Request(proper_encoded_download_link)
        connection = urllib2.urlopen(request)
        file_content = ''
        while True:
            file_chunk = connection.read(CHUNK_SIZE)
            if file_chunk:
                file_content += file_chunk
            else:
                break
        return file_content
    except urllib2.HTTPError as http_error:
        log_message = '{0}, {1}: {2}\n'.format(http_error.code, http_error.reason, download_link)
        web_logger.log_error(log_message)
        return None
    except urllib2.URLError as url_error:
        log_message = '{0}: {1}\n'.format(url_error.reason, download_link)
        web_logger.log_error(log_message)
        return None
    except Exception as e:
        print 'Something is up...'
        raise
