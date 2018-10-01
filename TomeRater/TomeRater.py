class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User {}'s email has been updated to {}".format(self.name,self.email))

    def __repr__(self):
        return "User {} has email {} and has read {} books".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        return  self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        book_count = 0
        rating = 0
        for book_key in self.books.keys():
            if self.books[book_key] != None:
                book_count += 1
                rating += self.books[book_key]
        return rating / book_count


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("new ISBN has been set to {}".format(self.isbn))

    def add_rating(self, rating):
        if type(rating) == int or type(rating) == float:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self,other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        rating_sum = 0
        rating_count = 0
        for rating in self.ratings:
            rating_sum += rating
            rating_count += 1
        return rating_sum / rating_count

    def __hash__(self):
        return hash((self.title, self.isbn))



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
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self,title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author,isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating = None):
        if email in list(self.users.keys()):
            user = self.users[email]
            user.read_book(book, rating)
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
        if user_books != None:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.keys():
            print(user)

    def highest_rated_book(self):
        highest_rate = 0
        for book in self.books.keys():
            if book.get_average_rating() > highest_rate:
                highest_rate = book.get_average_rating()
                highest_rated_book_temp = book
        return highest_rated_book_temp

    def most_positive_user(self):
        highest_rate = 0
        for user in self.users.keys():
            if user.get_average_rating() > highest_rate:
                highest_rate = user.get_average_rating()
                most_positive_user_temp = user
        return most_positive_user_temp

tobias = User("Tobias", "sdf@sadf.dk")
book1 = Book("ksjnd", 1234)
book1.add_rating(4.34)
print(book1.ratings)
book2 = Fiction("Mix Max", "Tobias Hansen", 1234)
print(book2)
book3 = Non_Fiction("Pølsemix", "Food", "Advanced",1234)
print(book3)

tobias.read_book(book1, 2)
tobias.read_book(book2)

print(tobias.get_average_rating())

Tome1 = TomeRater()
book4 = Tome1.create_book("Flex", 2345)