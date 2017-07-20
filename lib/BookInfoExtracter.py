import bs4

from utils import web

class BookInfoExtracter(object):

    def __init__(self, url):
        """
        A class to extract information about a book given the url

        Given the url, provide methods for extracting the book category, the pdf
        download link, and the book summary.

        Args:
            url (str): link to extract information from

        Returns:
            BookInfoExtracter: an instance of the class
        """
        self.url = url
        self.page_content = web.get_source(url)

    def _get_book_category(self):
        """
        Get the category

        From the page source, extract the first category that the book belongs to by using
        hardcoded pointers.

        Args:

        Returns:
            str: the category that the book belongs to
        """
        BEGINNING_MARKER = '.com/'
        ENDING_MARKER = 'rel="category"'

        ending_marker_index = self.page_content.find(ENDING_MARKER)
        assert ending_marker_index != -1, 'Ending marker for retrieving category not found!'

        beginning_marker_index = self.page_content.rfind(BEGINNING_MARKER, 0, ending_marker_index)
        assert beginning_marker_index != -1, 'Beginning marker for retrieving category not found!'

        begin_index = beginning_marker_index + len(BEGINNING_MARKER)
        end_index = self.page_content.find('"', begin_index)
        category = self.page_content[begin_index:end_index]
        return category

    def _get_book_pdf_download_link(self):
        """
        Get the pdf download link

        From the page source, extract the pdf download link for the book by using
        hardcoded pointers.

        Args:

        Returns:
            str: the url link from which the book can be downloaded as a pdf
        """
        MARKER = 'http://file.allitebooks.com'

        marker_index = self.page_content.find(MARKER)
        assert marker_index != -1, 'Marker for retrieving pdf link not found!'
        begin_index = marker_index
        end_index = self.page_content.find('"', marker_index)
        link = self.page_content[begin_index:end_index]
        return link

    def _get_book_summary(self):
        """
        Get the summary

        From the page source, extract the book description using hardcoded pointers.

        Args:

        Returns:
            unicode str: a book excerpt
        """
        BEGINNING_MARKER = '<h3>Book Description:</h3>'
        ENDING_MARKER = '<div class='

        beginning_marker_index = self.page_content.find(BEGINNING_MARKER)
        assert beginning_marker_index != -1, 'Beginning marker for retrieving summary not found!'
        begin_index = beginning_marker_index + len(BEGINNING_MARKER)

        ending_marker_index = self.page_content.find(ENDING_MARKER, beginning_marker_index)
        assert ending_marker_index != -1, 'Ending marker for retrieving summary not found!'
        end_index = ending_marker_index + len(ENDING_MARKER)

        relevant_content = self.page_content[begin_index:end_index]
        soup = bs4.BeautifulSoup(relevant_content, 'html.parser')
        text = soup.get_text().strip()
        summary = text.replace('\n\n', '\n')
        return summary

    def get_book_info(self):
        """
        Get the category, pdf download link, and summary

        Retrieve the category the book belongs to, the link from which a pdf version can be
        downloaded, and a book excerpt.

        Args:

        Returns:
            tuple: category of the book, download link, and book excerpt
        """
        category = self._get_book_category()
        pdf_download_link = self._get_book_pdf_download_link()
        summary = self._get_book_summary()
        return category, pdf_download_link, summary
