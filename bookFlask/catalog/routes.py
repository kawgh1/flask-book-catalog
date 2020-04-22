from bookFlask.catalog import main
from bookFlask import db
from bookFlask.catalog.models import Book, Publication
from flask import render_template, flash, request,redirect,url_for
from flask_login import login_required
from bookFlask.catalog.forms import EditBookForm, CreateBookForm


@main.route('/')
def display_books():

    books = Book.query.all()
    return render_template('home.html', books=books)


@main.route('/display/publisher/<publisher_id>')
def display_publisher(publisher_id):

    # publisher equals the the publisher_ID the user clicked on
    publisher = Publication.query.filter_by(id=publisher_id).first()

    # publisher_books equals all the books that have that publisher's ID in the Book table
    publisher_books = Book.query.filter_by(pub_id=publisher.id).all()

    # return the publisher.html page with publisher as publisher and books as books
    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books)


@main.route('/book/delete/<book_id>', methods = ['GET', 'POST'])
# login_required means these methods are only available to registered users who are logged in
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    # Now we need a POST request since we are making changes to the server
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash('book deleted successfully!')
        return redirect(url_for('main.display_books'))

    # if it's not a POST request, then we display the delete_book.html page
    return render_template('delete_book.html', book=book, book_id=book_id)


# need the EditBookForm import for this method to work
@main.route('/edit/book/<book_id>', methods=['GET', 'POST'])
@login_required

#Y YOU WILL NOTICE ON THIS METHOD, AFTER SUCCESSFUL UPDATE, THE BOOK
# IS MOVED TO THE LAST ITEM ON THE PAGE AT THE BOTTOM
# BELIEVE THIS IS BECAUSE THE METHOD DOES NOT TELL THE MAIN PAGE TO
# RESORT THE BOOKS - HOW TO MAKE STAY IN PLACE?

def edit_book(book_id):
    book = Book.query.get(book_id)
    # since we have a form, we need to create a form instance
    form = EditBookForm(obj=book)
    # if it's a POST request and the data to update by the user is valid
    # we'll display the main page with the NEW updated book fields below
    if form.validate_on_submit():
        # here we are just reassigning the book attributes to whatever
        # the user has put in the html forms
        book.title = form.title.data
        book.format = form.format.data
        book.num_pages = form.num_pages.data
        db.session.add(book)
        db.session.commit()
        flash('Book Updated Sucessfully!')
        return redirect(url_for('main.display_books'))

    # if it's a GET request we'll display the form with the book data on edit_book.html
    return render_template('edit_book.html', form=form)





@main.route('/create/book/<pub_id>', methods=['GET', 'POST'])
@login_required
# need the CreateBookForm import for this method to work
def create_book(pub_id):

    form = CreateBookForm()
    form.pub_id.data = pub_id # the db autopopulates this as well as
    # if it's a POST request and the data to update by the user is valid
    # we'll display the main page with the NEW book fields below
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, avg_rating=form.avg_rating.data,
                    book_format=form.format.data, image=form.img_url.data, num_pages=form.num_pages.data,
                    pub_id=form.pub_id.data)

        db.session.add(book)
        db.session.commit()
        flash('Book Added Successfully!')

        return redirect(url_for('main.display_publisher', publisher_id=pub_id))

    # If it's a GET request we display the form on create_book.html
    return render_template('create_book.html', form=form, pub_id=pub_id)


# The 404 error handling can be done in either the catalog/routes or the auth/routes, doesn't matter, same result
# Prof did it in the auth/routes with @at.app_errorhandler(404)

# since we are calling this on the app itself,
# this error handler method/message is available to all packages and pages on the site
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404