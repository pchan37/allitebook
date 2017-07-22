import os
import signal
from io import OpenWrapper

from lib import BookInfoExtracter
from lib.Config import Config
from lib.utils import web
from lib.utils import file_tools
from lib.utils import interrupt


class AllitebookDownloader(object):

    def __init__(self, homepage):
        """
        A class for downloading books from www.allitebooks.com

        Download books from the last page to the first page of www.allitebooks.com and save
        the progress in a config file.

        Args:
            homepage (str): link to the homepage of the website

        Returns:
            AllitebookDownloader: an instance of the class to download books from
                www.allitebooks.com
        """
        self.config = self._initialize_config()
        self.blacklist = self._initialize_blacklist()
        self.total_number_of_pages = self._get_adjusted_total_pages(homepage)
        signal.signal(signal.SIGINT, self._save_progress)

    def _initialize_config(self):
        """
        Load the configuration file

        Load the configuration file ('Allitebook.ini') if possible.  Otherwise, create
        one with the default value if it doesn't already exists.

        Args:

        Returns:
            Config: instance of the config class containing the config values
        """
        config = Config.Config('Allitebook.ini')
        config.set_default_value('url', None)
        config.set_default_value('query', None)
        config.set_default_value('current_pages', 0)
        config.set_default_value('total_pages', None)
        return config

    def _initialize_blacklist(self):
        """
        Load the blacklist

        Populate self.blacklist with the content of 'blacklist.txt'; results in a list of
        urls to be skipped.

        Args:

        Returns:
            list: A list of urls to be skipped
        """
        blacklist = []
        if os.path.exists('blacklist.txt'):
            with open('blacklist.txt') as blacklist_file_handler:
                file_content = blacklist_file_handler.readlines()
                blacklist = map(str.strip, file_content)
        return blacklist

    def _save_progress(self, *args):
        """
        Save the current progress and terminate the program

        Temporarily block the KeyboardInterrupt signal (Ctrl-C), save the config values to
        the configuration file, and terminate the program.

        Args:
            *args: normally signum and frame, but might also have no value
                signum (int) : the number associated with the triggered signal
                frame (str): the stack frame when the signal was triggered

        Returns:

        """
        with interrupt.KeyboardInterruptBlocked():
            print 'Saving progress...'
            self.config.save()
            print 'Terminated...'
            if len(args):
                raise SystemExit(0)

    def _get_adjusted_total_pages(self, homepage):
        """
        Get the total number of pages and then adjust it based on past progress

        Extract the total number of pages of books from the website, so that we can
        start from the end.  Adjust the value based on progress already made (done by
        subtracting the pages completed from the current last page).

        Args:
            homepage (str): link to the homepage of a website

        Returns:
            int: the total number of pages
        """
        MARKER = 'title="Last Page'

        page_content = web.get_source(homepage)
        marker_index = page_content.find(MARKER)
        assert_message = 'Marker for finding total number of pages is not found!'
        interrupt.assert_extended(marker_index != -1, assert_message, self._save_progress)
        begin_index = page_content.find('>', marker_index) + 1
        end_index = page_content.find('<', begin_index)

        total_pages = int(page_content[begin_index:end_index])
        adjusted_pages_count = total_pages - self.config.get('total_pages') + self.config.get('current_pages')
        self.config.set('total_pages', total_pages)

        return adjusted_pages_count

    def _retrieve_book_info(self, book_link):
        """
        Retrieve the book category, pdf downlooad link, and book excerpt

        Attempt to retrieve the book category, pdf download link, and book excerpt.  Upon
        failure, catch the AssertionError, save current progress, and then raise
        AssertionError again.

        Args:
            book_link (str): the link for a particular book

        Returns:
            tuple: category of the book, download link, and book excerpt

        Raises:
            AssertionError: Occurs when the condition asserted is False, should never happen
        """
        try:
            book_info_extracter = BookInfoExtracter.BookInfoExtracter(book_link)
            category, pdf_download_link, summary = book_info_extracter.get_book_info()
            return category, pdf_download_link, summary
        except AssertionError:
            self._save_progress()
            raise

    def get_list_of_books_page(self, page):
        """
        Retrieve a list of books page

        From the given page, extract the links leading to each book and store the data in a list.
        This gives us a collection of links from which we can retrieve the relevant information and
        download the book.

        Args:
            page (str): link listing a set of books

        Returns:
            list: a list of links each of which leads to a webpage for a particular book
        """
        HTML_LINK_TAG = '<a href="'
        BOOK_SECTION_MARKER = '"entry-title"'

        list_of_books_page = []
        page_content = web.get_source(page)
        marker_index = page_content.find(BOOK_SECTION_MARKER)
        assert_message = 'Marker for finding book section not found!'
        interrupt.assert_extended(marker_index != -1, assert_message, self._save_progress)

        while marker_index != -1:
            beginning_marker_index = page_content.find(HTML_LINK_TAG, marker_index)
            assert_message = 'Marker for finding book link not found!'
            interrupt.assert_extended(beginning_marker_index != -1, assert_message, self._save_progress)
            begin_index = beginning_marker_index + len(HTML_LINK_TAG)
            end_index = page_content.find('"', begin_index)

            link = page_content[begin_index:end_index]
            list_of_books_page.append(str(link))
            marker_index = page_content.find(BOOK_SECTION_MARKER, end_index)

        list_of_books_page.reverse()
        try:
            index_of_last_processed_book_page = list_of_books_page.index(self.config.get('url'))
            list_of_books_page = list_of_books_page[index_of_last_processed_book_page + 1:]
        except ValueError:
            pass
        return list_of_books_page

    def get_path_to_save_file(self, category, pdf_link):
        """
        Retrieve the path for which the file should be saved

        Use the category as the base directory path and join it with the properly encoded
        filename. If the category is made up of a single directory name, the file would be
        dumped in the general section inside the given category.

        Args:
            category (str): the directory path the file would be dumped into
            pdf_link (str): the link to the PDF file, also contains the filename

        Returns:
            str: path which the file should be saved to
        """
        base_directory = os.path.join('allitebook/', category)
        directory_path = base_directory
        if category.count('/') == 1:
            directory_path = os.path.join(base_directory, 'general')

        filename = pdf_link[pdf_link.rfind('/') + 1:]
        file_tools.assure_directory_path_exists(directory_path)

        raw_encoded_full_path = os.path.join(directory_path, filename)
        proper_encoded_full_path = raw_encoded_full_path.replace(' ', '_')
        return proper_encoded_full_path

    def process_book_link(self, book_link):
        """
        Extract relevant information, download the file, and save it to proper destination

        Extract the book category, the PDF download link, and book summary from the given page.
        Download the file using the extracted PDF download link and save it to the appropriate
        directory.

        Args:
            book_link (str): the link for a particular book

        Returns:

        """
        category, pdf_download_link, summary = self._retrieve_book_info(book_link)
        pdf_file_content = web.download_page(pdf_download_link)
        book_filename = self.get_path_to_save_file(category, pdf_download_link)
        summary_filename = book_filename[:book_filename.rfind('.pdf')] + '.txt'

        if pdf_file_content is not None:
            with interrupt.KeyboardInterruptBlocked():
                with open(book_filename, 'a') as file_:
                    file_.write(pdf_file_content)
                with OpenWrapper(summary_filename, 'a', encoding='utf-8') as file_:
                    file_.write(summary)
                self.config.set('url', book_link)

    def start(self):
        """
        Start the whole process

        Start from the last page and count downward to the first page, downloading all the books
        on each page.

        Args:

        Returns:

        """
        for page_number in xrange(self.total_number_of_pages, 0, -1):
            page = 'http://www.allitebooks.com/page/{0}/'.format(page_number)
            list_of_books_page = self.get_list_of_books_page(page)
            for book_page in list_of_books_page:
                if book_page in self.blacklist:
                    continue
                print book_page
                self.process_book_link(book_page)
            self.config.set('current_pages', page_number)
        print 'Done!'
        self._save_progress()


def main():
    """
    Run the script
    """
    allitebook_downloader = AllitebookDownloader('http://www.allitebooks.com')
    allitebook_downloader.start()

if __name__ == '__main__':
    main()
