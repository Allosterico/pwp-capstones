class User(object):
    def __init__(self, name, email):
        # Constructor
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User {user_name}'s email has been updated to {email}".format(user_name = self.name, email = self.email))

    def __repr__(self):
        #As part of the very last exercise, I have chosen, among other things, to make the representations take some Grammar into account
        return "User {} has email {} and has read {} {}".format(self.name, self.email, len(self.books), "books" if len(self.books) < 1 else "book")

    def __eq__(self, other_user):
        return  self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        #If the user has not read any books, the average rating cannot be calculated.
        if len(self.books) == 0:
            raise UserRatingError
        else:
            book_count = 0
            rating_total = 0
            num_of_books_not_rated = 0
            for book_key, rating in self.books.items():
                #The rating must be an int or float.
                if type(rating) == int or type(rating) == float:
                    book_count += 1
                    rating_total += rating
                else:
                #It is assumed, that if the rating is not an int or float, it is None. Therefore the book has not been rated and should not be included in the average calculation.
                    num_of_books_not_rated += 1
                    book_count += 1
            if book_count > num_of_books_not_rated:
                return rating_total / (book_count - num_of_books_not_rated)
            else:
                raise UserRatingError


# As part of the very last exercise, I have chosen, among other things, include a number of exceptions in order to control how the program should act when given an input of incorrect data type.
class UserRatingError(Exception):
    pass

class BookRatingError(Exception):
    pass

class InputError(Exception):
    pass


class Book(object):
    def __init__(self, title, isbn):
        if type(title) == str:
            self.title = title
        else:
            raise InputError

        if type(isbn) == int:
            self.isbn = isbn
        else:
            raise InputError

        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        if type(new_isbn) == int:
            self.isbn = new_isbn
            print("new ISBN has been set to {}".format(self.isbn))
        else:
            raise InputError

    def add_rating(self, rating):
        if (type(rating) == int or type(rating) == float) and 0 <= rating <= 4:
            self.ratings.append(rating)
        else:
            raise InputError

    def __eq__(self,other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        rating_sum = 0
        rating_count = 0
        #If the book has no ratings yet, the average cannot be calculated and an error is raised
        if len(self.ratings) == 0:
            raise BookRatingError
        else:
            for rating in self.ratings:
                rating_sum += rating
                rating_count += 1
            return rating_sum / rating_count


    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "Book with title {}".format(self.title)



class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        # As part of the very last exercise, I have chosen, among other things, to make the representations take some Grammar into account
        vowels = ["a", "e", "i", "o", "u"]
        return "{}, {} {} manual on {}".format(self.title, "an" if self.level[0] in vowels else "a", self.level, self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self,title, isbn):
        try:
            return Book(title, isbn)
        except InputError:
            # As part of the very last exercise, I have chosen, among other things, include a number of exceptions in order to control how the program should act when given an input of incorrect data type.
            print("Make sure, that the input is of the correct data type. No book was created")

    def create_novel(self, title, author, isbn):
        try:
            return Fiction(title, author,isbn)
        except InputError:
            # As part of the very last exercise, I have chosen, among other things, include a number of exceptions in order to control how the program should act when given an input of incorrect data type.
            print("Make sure, that the input is of the correct type. No novel was created")

    def create_non_fiction(self, title, subject, level, isbn):
        try:
            return Non_Fiction(title, subject, level, isbn)
        except InputError:
            # As part of the very last exercise, I have chosen, among other things, include a number of exceptions in order to control how the program should act when given an input of incorrect data type.
            print("Make sure, that the input is of the correct type. No novel was created")

    def add_book_to_user(self, book, email, rating = None):
        if email in list(self.users.keys()):
            user = self.users[email]
            user.read_book(book, rating)
            if (type(rating) == int or type(rating) == float) and 0 <= rating <= 4:
                book.add_rating(rating)
            if book in list(self.books.keys()):
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {}".format(email))

    def add_user(self, name, email, user_books = None):
        user = User(name, email)
        self.users[email] = user
        if type(user_books) == list:
            for book in user_books:
                self.add_book_to_user(book, email)

    def change_user_email(self,existing_email, new_email):
        try:
            user = self.users[existing_email]
            user.change_email(new_email)
            self.users[new_email] = self.users.pop(existing_email)
        except KeyError:
            print("No user with email '{}'".format(existing_email))

    def print_catalog(self):
        print("---Now printing catalogue---")
        for book, num_read in self.books.items():
            print(book)
        print("---Finished printing catalogue---")

    def print_users(self):
        print("---Now printing users---")
        for user, ratings in self.users.items():
            print(user)
        print("---Finished printing users---")

    def most_read_book(self):
        most_read_value = -1
        for book, num_read in self.books.items():
            if num_read > most_read_value:
                most_read = book
                most_read_value = num_read
        return most_read

    def highest_rated_book(self):
        highest_rate = -1
        #This loop iterates through all of the key:val pairs of the books in TomeRater
        for book, num_read in self.books.items():
            try:
                if book.get_average_rating() > highest_rate:
                    highest_rate = book.get_average_rating()
                    highest_rated = book
            #This error is raised if a book has not been rated. It is no problem, the iteration just continues
            except BookRatingError:
                pass
        #If no books have yet been rated, the highest rate will still be -1,
        if highest_rate == -1:
            print("No books have yet been rated")
        else:
            return highest_rated

    def most_positive_user(self):
        highest_rating = -1
        for (email, user) in self.users.items():
            try:
                if user.get_average_rating() > highest_rating:
                    highest_rating = user.get_average_rating()
                    most_positive = user
            except UserRatingError:
                pass
        #If no users have yet rated any books (highest rating == -1), the most positive user cannot be found
        if highest_rating == -1:
            print("No users have yet rated any books")
        else:
            return most_positive
