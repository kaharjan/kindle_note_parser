import datetime


class Book:
    def __init__(self):
        self.highlights_list = []
        self.bookmarks_list = []
        self.notes_list = []
        self.book_name = ""
        self.start_reading_date = datetime.datetime.now().date()
        self.end_reading_date = datetime.datetime.now().date()

    def bookmarks_count(self):
        """
        Returns number of all bookmarks in the book
        :return: Number of bookmarks
        """
        return len(self.bookmarks_list)

    def highlights_count(self):
        """
        Returns number of all highlights in the book
        :return: Number of highlights
        """
        return len(self.highlights_list)

    def notes_count(self):
        """
        Returns number of all notes in the book
        :return: Number of notes
        """
        return len(self.notes_list)

    def start_finish_reading_date(self):
        """
        Extracts first and last bookmark date. Dates are sorted in chronological order and then extracted.
        :return: First and last date from the bookmark list
        """
        # print("bookmarks:") #kahar added
        # print(self.bookmarks_list) #kahar added
        print("notes=",self.notes_count())
        dates_n = [item.date for item in self.notes_list]
        print("highlights=",self.highlights_count())
        dates_h = [item.date for item in self.highlights_list]
        print("bookmarks=",self.bookmarks_count())
        dates_b = [item.date for item in self.bookmarks_list]
        dates = dates_n + dates_h + dates_b
        print("all mark's len=",len(dates))
        if(len(dates)>1):
            # dates = [item.date for item in self.bookmarks_list]
            dates.sort()
            # print(dates)
            return dates[0], dates[-1]
        elif(len(dates)==1):
            return datetime.datetime(1900,1,1),dates[0]

        else:
            return datetime.datetime(1900,1,1),datetime.datetime(1900,1,1)
