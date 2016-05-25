import os


class Export:
    def export(self, book, folder_path):
        """
        Exports data collected from kindle file to the wanted format
        :param folder_path: File where the document will be exported
        :param books: List of books generated by the raw_parser.py
        :return:
        """
        raise NotImplementedError


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

        with open(os.path.join(folder_path, book.book_name + ".tex"), "w") as file:

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
                                str(highlight.content)) + " (\\textit{Location " + highlight.location + "})}\n")

                    file.write("\\end{itemize}\n")

                elif template.startswith("$"):
                    file.write("\\begin{itemize}\n")

                    start, end = book.get_start_and_end_reading_dates()
                    file.write("\\item{Started reading book on: " + str(start.date()) + "}\n")
                    file.write("\\item{Finished reading book on: " + str(end.date()) + "}\n")

                    file.write("\\end{itemize}\n")

                else:
                    file.write(template)


class ExportPlain(Export):
    def __init__(self, author_name):
        """
        Creates list of lines from the template file
        :param author_name: Name of the author which will be written on the document (NOT NAME OF THE BOOK'S AUTHOR)
        """
        self.author = author_name

    def export(self, book, folder_path):
        start, end = book.get_start_and_end_reading_dates()

        with open(os.path.join(folder_path, book.book_name + ".txt"), "w") as file:
            file.write("Book name: " + book.book_name + '\n\n')

            file.write("Started reading: " + str(start.date()) + '\n')
            file.write("Finished reading: " + str(end.date()) + '\n\n')
            file.write("Book notes\n\n")

            for highlight in book.highlights_list:
                file.write("- " + highlight.content + " Location (" + highlight.location + ")\n")


class ExportMarkdown(Export):
    def __init__(self, template_path, author_name):
        """
        Creates list of lines from the template file
        :param template_path: Path to the .md template file
        :param author_name: Name of the author which will be written on the document (NOT NAME OF THE BOOK'S AUTHOR)
        """
        with open(template_path, 'r') as file:
            self.template = file.readlines()
            self.author = author_name

    def export(self, book, folder_path):
        start, end = book.get_start_and_end_reading_dates()

        with open(os.path.join(folder_path, book.book_name + ".md"), "w") as file:

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
                        file.write("* " + highlight.content + "*Location (+" + highlight.location + ')*\n')

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
    Escape special characters in tex format
    :return:
    """
    replacement = {"{", "}", "$", "#"}
    for rep in replacement:
        string = string.replace(rep, "\\" + rep)
    return string
