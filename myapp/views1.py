# # Import necessary classes
# from django.http import HttpResponse
# from .models import Publisher, Book, Member, Order
# from django.shortcuts import get_object_or_404
#
#
# # deprecated view file
# # Create your views here.
# def index(request):
#     response = HttpResponse()
#     book_list = Book.objects.all().order_by('id')[:10]
#
#     heading_1 = '<p>' + 'List of available books: ' + '</p>'
#     response.write(heading_1)
#
#     section_1 = '<table><thead><th>Id</th><th>Book Name</th><th>Publisher Name</th></thead><tbody>'
#     for book in book_list:
#         section_1 += '<tr>'
#         section_1 += '<td>' + str(book.pk) + '</td>'
#         section_1 += '<td>' + book.title + '</td>'
#         section_1 += '<td>' + book.publisher.name + '</td>'
#         section_1 += '</tr>'
#
#     section_1 += '</tbody></table>'
#
#     response.write(section_1)
#     response.write("<br/>")
#     response.write("<br/>")
#
#     publisher_list = Publisher.objects.order_by("-city")
#
#     section_2 = '<table><thead><th>Id</th><th>Name</th><th>City</th></thead><tbody>'
#     for pub in publisher_list:
#         section_2 += '<tr>'
#         section_2 += '<td>' + str(pub.pk) + '</td>'
#         section_2 += '<td>' + pub.name + '</td>'
#         section_2 += '<td>' + pub.city + '</td>'
#         section_2 += '</tr>'
#     section_2 += '</tbody></table>'
#
#     response.write(section_2)
#
#     return response
#
#
# def about(request):
#     response = HttpResponse()
#     about_heading = '<p>' + 'This is an eBook APP.' + '</p>'
#     response.write(about_heading)
#
#     return response
#
#
# def detail(request, book_id):
#     books = get_object_or_404(Book, pk=book_id)
#     response = HttpResponse()
#     title = '<p>' + 'Title: ' + books.title.upper() + '</p>'
#     price = '<p>' + 'Price: $' + str(books.price) + '</p>'
#     publisher = '<p>' + 'Publisher: ' + books.publisher.name + '</p>'
#
#     response.write(title)
#     response.write(price)
#     response.write(publisher)
#
#     return response
