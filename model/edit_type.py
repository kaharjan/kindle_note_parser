from datetime import datetime
#kahar added start
import re
import locale
pattern_1 = re.compile(u' Added on [A-Za-z]+, \d{1,2}')
pattern_2 = re.compile(u' Added on [A-Za-z]+, [A-Za-z]+')
pattern_3 = re.compile(u' 添加于 \d{4}')

#kahar added end

class EditType:
    """
    EditType interface for all types of user generated content on the kindle device
    Some include: Bookmarks, Notes and Highlights. More content could be available but I am not aware of it
    Attributes which it must contain: Date and content
    """

    def parse_edit_location(self, raw_data):
        """
        Parse edit Location or location range
        :param raw_data: String containing location
        :return: Location or location string value
        """

    def parse_edit_date(self, raw_data):
        """
        Parse edit date
        :param raw_data: String containing location
        :return: datetime object
        """


class HighlightType(EditType):
    """
    Created for Kindle Paperwhite gen 5.
    Highlight Edit class.
    Contains content of the highlight, location range of the highlight and the date
    """

    def __init__(self, highlight_string, content):
        self.content = content
        self.date = self.parse_edit_date(highlight_string)
        self.location = self.parse_edit_location(highlight_string)

    def parse_edit_date(self, data):
        """
        Example of input:
        - Your Highlight on Location 6778-6779 | Added on Monday, August 17, 2015 7:38:34 AM
        k:comment: or 17 August so I need to change the code

        :param data:
        :return:
        """
        date_part = data.split("|")
        added_time = ""
        if(pattern_1.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            added_time = datetime.strptime(date_part[-1]," Added on %A, %d %B %Y %H:%M:%S")
        elif(pattern_2.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            added_time = datetime.strptime(date_part[-1]," Added on %A, %B %d, %Y %I:%M:%S %p")
        elif(pattern_3.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
            added_time = datetime.strptime(date_part[-1]," 添加于 %Y年%m月%d日%A %p%H:%M:%S")
        else:
            print("{} can't be parsed".format(date_part[-1]))
        return added_time

        #return datetime.strptime(date_part[-1], " Added on %A, %B %d, %Y %I:%M:%S %p")

    def parse_edit_location(self, data):
        """
        Example of input:
        - Your Highlight on Location 6778-6779 | Added on Monday, August 17, 2015 7:38:34 AM

        - 您在位置 #486-487的标注 | 添加于 2021年6月22日星期二 下午9:26:14
        :param data:
        :return:
        """
        # loc_split = data.split("|")
        # if len(loc_split) > 2:
            # return loc_split[1].rstrip().lstrip().split(" ")[-1]
        # else:
            # return loc_split[0].split(" ")[5]

        loc_split = data.split("|")
        if len(loc_split) > 2:
            return loc_split[1].rstrip().lstrip().split(" ")[-1]
        else:
            #kahar add
            if("您" in loc_split[0]):
                # print("loc_split:",loc_split[0])
                return loc_split[0].split(" ")[2].strip("#").strip("的标注")
            else:
                # print("en loc:",loc_split[0])
                return loc_split[0].split(" ")[5]






class NoteType(EditType):
    """
    Created for Kindle Paperwhite gen 5.
    Highlight Edit class.
    Note Edit class
    Contains content of the Note, location of the note and the date
    """

    def __init__(self, edit_string, content):
        self.content = content
        self.date = self.parse_edit_date(edit_string)
        self.location = self.parse_edit_location(edit_string)

    def parse_edit_date(self, data):
        """
        Example of input:
        - Your Note on Location 4555 | Added on Wednesday, February 24, 2016 8:28:14 AM

        :param data:
        :return:
        """
        date_part = data.split("|")
        #return datetime.strptime(date_part[-1], " Added on %A, %B %d, %Y %I:%M:%S %p")

        added_time = ""
        if(pattern_1.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            added_time = datetime.strptime(date_part[-1]," Added on %A, %d %B %Y %H:%M:%S")
        elif(pattern_2.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            added_time = datetime.strptime(date_part[-1]," Added on %A, %B %d, %Y %I:%M:%S %p")
        elif(pattern_3.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
            added_time = datetime.strptime(date_part[-1]," 添加于 %Y年%m月%d日%A %p%H:%M:%S")
        else:
            print("{} can't be parsed".format(date_part[-1]))
        return added_time

    def parse_edit_location(self, data):
        """
        Example of input:
        - Your Note on Location 4555 | Added on Wednesday, February 24, 2016 8:28:14 AM
        kahar :
        - 您在位置 #380 的笔记 | 添加于 2021年6月22日星期二 下午7:28:15

        :param data:
        :return:
        """
        loc_split = data.split("|")
        if len(loc_split) > 2:
            return loc_split[1].rstrip().lstrip().split(" ")[-1]
        else:
            #kahar add
            if("您" in loc_split[0]):
                # print("loc_split:",loc_split[0])
                return loc_split[0].split(" ")[2].strip("#")
            else:
                # print("en loc:",loc_split[0])
                return loc_split[0].split(" ")[5]


class BookmarkType(EditType):
    """
    Created for Kindle Paperwhite gen 5.
    Highlight Edit class.
    Bookmark Edit class
    Contains location of the bookmark and the date
    """

    def __init__(self, bookmark_string):
        self.date = self.parse_edit_date(bookmark_string)
        self.location = self.parse_edit_location(bookmark_string)

    def parse_edit_date(self, data):
        """
        Example of input:
        - Your Bookmark on Location 3021 | Added on Wednesday, February 17, 2016 1:49:13 PM

        :param data:
        :return:
        """
        #k: changed
        #k:comment: or 17 August so I need to change the code

        date_part = data.split("|")
        added_time = ""
        if(pattern_1.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            added_time = datetime.strptime(date_part[-1]," Added on %A, %d %B %Y %H:%M:%S")
        elif(pattern_2.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            added_time = datetime.strptime(date_part[-1]," Added on %A, %B %d, %Y %I:%M:%S %p")
        elif(pattern_3.search(date_part[-1])):
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
            added_time = datetime.strptime(date_part[-1]," 添加于 %Y年%m月%d日%A %p%H:%M:%S")
        else:
            print("{} can't be parsed".format(date_part[-1]))
        return added_time



        #date_part = data.split("|")
        #return datetime.strptime(date_part[-1], " Added on %A, %B %d, %Y %I:%M:%S %p")

    def parse_edit_location(self, data):
        """
        Example of input:
        - Your Bookmark on Location 3021 | Added on Wednesday, February 17, 2016 1:49:13 PM
        - 您在位置 #2974 的书签 | 添加于 2021年4月12日星期一 下午11:14:02

        :param data:
        :return:
        """
        # loc_split = data.split("|")
        # if len(loc_split) > 2:
            # return loc_split[1].rstrip().lstrip().split(" ")[-1]
        # else:
            # return loc_split[0].split(" ")[5]

#kahar added
        loc_split = data.split("|")
        if len(loc_split) > 2:
            return loc_split[1].rstrip().lstrip().split(" ")[-1]
        else:
            #kahar add
            if("您" in loc_split[0]):
                # print("loc_split:",loc_split[0])
                return loc_split[0].split(" ")[2].strip("#")
            else:
                # print("en loc:",loc_split[0])
                return loc_split[0].split(" ")[5]



