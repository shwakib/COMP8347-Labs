from myapp.models import Member, Publisher, Book, Order

# a. List all Members whose last name is ‘Jones’
Member.objects.filter(last_name='Jones')
# b. List all Publishers with headquarters in ‘USA’
Publisher.objects.filter(country='USA')
# c. List all Members that live in ‘Windsor’
Member.objects.filter(city='Windsor')
# d. List all Members that live on an ‘Avenue’ and live in AB province
Member.objects.filter(address__contains='Avenue', province='AB')
# e. List all the Members that have borrowed the book 'A New World'
Member.objects.filter(borrowed_books__title='A New World').distinct()
# f. List the Books that cost more than $100.00
Book.objects.filter(price__gt=100.00)
# g. List the Members that do NOT live in province AB
Member.objects.exclude(province='AB')
# h. List the Orders placed by a client whose first_name is ‘Mary’
Order.objects.filter(member__first_name='Mary')
# i. List the Members whose member status are ‘Premium Member’
Member.objects.filter(status=2)
# j. List the Books that have between 100 and 280 pages (inclusive) and belong to category ‘Science&Tech’
Book.objects.filter(num_pages__range=(100,280), category='S')
# k. Get the first name of the Member of the Order with pk=1
k_firstName = Member.objects.get(pk=Order.objects.get(pk=1).member.pk).first_name

# l. List all Books that the Member with username ‘bill’ is currently borrowing
Book.objects.filter(member__username="bill",  order__status=1).distinct()

# m. List all the Members who live in AB and have auto_renew enabled
Member.objects.filter(province='AB', auto_renew=True)

# n. List the Books that ‘mary’ has purchased
Book.objects.filter(order__books__member=(Member.objects.filter(username="Mary")).first(), order__status=0)

# o. List the city where the headquarters of the publisher of the book borrowed by ‘alan’ is located
Publisher.objects.filter(pk__in=Book.objects.filter(order__books__member=(Member.objects.filter(username="alan").first())).distinct().values("publisher")).values("city")

# get publishers name who's book price is greater than 100
Book.objects.filter(price__gt=100.00).distinct().values("publisher__name")
