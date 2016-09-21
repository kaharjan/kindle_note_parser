import os
import re


class Export:
    def export(self, book, folder_path):
        """
        Exports data collected from kindle file to the wanted format
        :param folder_path: File where the document will be exported
        :param books: List of books generated by the raw_parser.py
        :return:
        """
        raise NotImplementedError

    def format_filename(self, name):
        """

        :param name:
        :return:

        """
        return re.sub('[^a-zA-Z0-9 \n\.]', '', name).lower().replace(" ", "_")


class ExportTex(Export):
    """
    Exports to .tex file (Latex)
    """

    def __init__(self, template_path, author_name):
        """
        Creates list of lines from the template file
        :param template_path: Path to the .tex template file
        :param author_name: Name of the author which will be written on the document (NOT NAME OF THE BOOK'S AUTHOR)
        """
        with open(template_path, 'r') as file:
            self.template = file.readlines()
            self.author = author_name

    def export(self, book, folder_path):

        with open(os.path.join(folder_path, self.format_filename(book.book_name)
                + ".tex"), "w") as file:

            for index, template in enumerate(self.template):
                if "book_title" in template:
                    # Replace book title
                    template = template.replace("book_title", book.book_name)
                    file.write(template)

                elif "author_name" in template:
                    template = template.replace("author_name", self.author)
                    file.write(template)

                elif template.startswith("#"):
                    # Insert content
                    if not book.highlights_list:
                        continue

                    file.write("\\begin{itemize}\n")

                    for highlight in book.highlights_list:
                        file.write(
                            "\\item {" + escape_special(
                                string=str(highlight.content))
                            + " (\\textit{Location " + highlight.location + "})}\n")

                    file.write("\\end{itemize}\n")

                elif template.startswith("$"):
                    file.write("\\begin{itemize}\n")

                    start, end = book.start_finish_reading_date()
                    file.write("\\item{Started reading book on: " + str(
                        start.date()) + "}\n")
                    file.write("\\item{Finished reading book on: " + str(
                        end.date()) + "}\n")

                    file.write("\\end{itemize}\n")

                else:
                    file.write(template)


class ExportPlain(Export):
    """
    Exports data into a txt format
    """

    def __init__(self, author_name):
        """
        Creates list of lines from the template file
        :param author_name: Name of the author which will be written on the document (NOT NAME OF THE BOOK'S AUTHOR)
        """
        self.author = author_name

    def export(self, book, folder_path):
        start, end = book.start_finish_reading_date()

        with open(os.path.join(folder_path,
                               self.format_filename(book.book_name) + ".txt"),
                  "w") as file:
            file.write("Book name: " + book.book_name + '\n\n')

            file.write("Notes Author: " + self.author + '\n\n')

            file.write("Started reading: " + str(start.date()) + '\n')
            file.write("Finished reading: " + str(end.date()) + '\n\n')
            file.write("Book notes\n\n")

            for highlight in book.highlights_list:
                file.write(
                    "- " + highlight.content + " Location (" +
                    highlight.location + ")\n")


class ExportMarkdown(Export):
    """
    Exports data into a markdown format
    """

    def __init__(self, template_path, author_name):
        """
        Creates list of lines from the template file
        :param template_path: Path to the .md template file
        :param author_name: Name of the author which will be written on the
        document (NOT NAME OF THE BOOK'S AUTHOR)
        """
        with open(template_path, 'r') as file:
            self.template = file.readlines()
            self.author = author_name

    def export(self, book, folder_path):
        start, end = book.start_finish_reading_date()

        with open(os.path.join(folder_path, self.format_filename(book.book_name)
                + ".md"), "w") as file:

            for index, template in enumerate(self.template):
                if "book_title" in template:
                    # Replace book title
                    template = template.replace("book_title", book.book_name)
                    file.write(template)

                elif "author_name" in template:
                    template = template.replace("author_name", self.author)
                    file.write(template)

                elif template.startswith("$"):
                    # Insert content
                    if not book.highlights_list:
                        continue

                    for highlight in book.highlights_list:
                        file.write(
                            "* " + highlight.content + "*Location (+" + highlight.location + ')*\n')

                elif "date_start" in template:
                    template = template.replace("date_start", str(start.date()))
                    file.write(template + '\n')

                elif "date_end" in template:
                    template = template.replace("date_end", str(end.date()))
                    file.write(template + '\n')

                else:
                    file.write(template)


def escape_special(string):
    """
    Escape special characters in TeX language.
    Backslash is added to every special character
    :return: String with escaped special characters
    """
    replacement = {"{", "}", "$", "#", "&", "_", "%"}
    for rep in replacement:
        string = string.replace(rep, "\\" + rep)
    return string
