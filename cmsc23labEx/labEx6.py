from abc import ABC, abstractmethod


class Date:
    def __init__(self, month: int, day: int, year: int):
        self.__month = month
        self.__day = day
        self.__year = year

    def mdyFormat(self) -> str:
        return str(self.__month) + "/" + str(self.__day) + "/" + str(self.__year)

    def getMonth(self) -> int:
        return self.__month

    def getDay(self) -> int:
        return self.__day

    def getYear(self) -> int:
        return self.__year


class Page:
    def __init__(self, sectionHeader: str, body: str):
        self.__sectionHeader = sectionHeader
        self.__body = body


class BorrowableItem(ABC):
    @abstractmethod
    def uniqueItemId(self) -> int:
        pass

    @abstractmethod
    def commonName(self) -> str:
        pass

    @abstractmethod
    def dueDays(self) -> int:
        pass


class Book(BorrowableItem):
    def __init__(self, bookId: int, title: str, author: str, publishDate: Date, pages: [Page]):
        self.__bookId = bookId
        self.__title = title
        self.__publishDate = publishDate
        self.__author = author
        self.__pages = pages

    def coverInfo(self) -> str:
        return "Title: " + self.__title + "\nAuthor: " + self.__author

    def uniqueItemId(self) -> int:
        return self.__bookId

    def commonName(self) -> str:
        return "Borrowed Item:" + self.__title + " by " + self.__author

    def dueDays(self) -> int:
        return 7


class Periodical(BorrowableItem):
    def __init__(self, periodicalID: int, title: str, issue: Date, pages: [Page]):
        self.__periodicalID = periodicalID
        self.__title = title
        self.__issue = issue
        self.__pages = pages

    def uniqueItemId(self) -> int:
        return self.__periodicalID

    def commonName(self) -> str:
        return self.__title + " issue: " + self.__issue.mdyFormat()

    def dueDays(self) -> int:
        return 1


class PC(BorrowableItem):
    def __init__(self, pcID: int):
        self.__pcID = pcID

    def uniqueItemId(self) -> int:
        return self.__pcID

    def commonName(self) -> str:
        return "PC" + self.__pcID

    def dueDays(self) -> int:
        return 0


class LibraryCard:
    def __init__(self, idNumber: int, name: str, borrowedItems: {BorrowableItem: Date}):
        self.__idNumber = idNumber
        self.__name = name
        self.__borrowedItems = borrowedItems

    def borrowItem(self, book: BorrowableItem, date: Date):
        self.__borrowedItems[book] = date

    def borrowerReport(self) -> str:
        r: str = self.__name + "\n"
        for borrowedItem in self.__borrowedItems:
            r = r + borrowedItem.commonName() + ", borrow date:" + \
                self.__borrowedItems[borrowedItem].mdyFormat() + "\n"
        return r

    def returnItem(self, b: BorrowableItem):
        del self.__borrowedItems[b]

    def penalty(self, b: BorrowableItem, today: Date) -> float:
        date = self.__borrowedItems[b]
        due_date = Date(date.getMonth(), date.getDay() +
                        b.dueDays(), date.getYear())
        return getDifference(due_date, today) * 3.5

    def itemsDue(self, today: Date) -> [BorrowableItem]:
        item_dues = [BorrowableItem]
        for item, date in self.__borrowedItems.items():
            due_date = Date(date.getMonth(), date.getDay() +
                            item.dueDays(), date.getYear())
            if getDifference(due_date, today) > 0:
                item_dues.append(item)
        return item_dues

    def totalPenalty(self, today: Date) -> float:
        total_dues = float
        for item, date in self.__borrowedItems.items():
            total_dues += self.penalty(item, today)
        return total_dues


# algorithm to get the number of days between two Date objects
monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def countLeapYears(date: Date):
    years = date.getYear()

    if date.getMonth() <= 2:
        years -= 1

    ans = int(years / 4)
    ans -= int(years / 100)
    ans += int(years / 400)
    return ans


def getDifference(date1: Date, date2: Date):
    num1 = date1.getYear() * 365 + date1.getDay()

    for i in range(0, date1.getMonth() - 1):
        num1 += monthDays[i]

    num1 += countLeapYears(date1)
    num2 = date2.getYear() * 365 + date2.getDay()

    for i in range(0, date2.getMonth() - 1):
        num2 += monthDays[i]

    num2 += countLeapYears(date2)
    return (num2 - num1)
