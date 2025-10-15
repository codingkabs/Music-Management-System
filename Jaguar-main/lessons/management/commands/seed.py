import random
from datetime import date, datetime

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker

from lessons.helpers import get_invoice_amount
from lessons.models import Invoice, LessonRequest, Teacher, User


class Command(BaseCommand):
    """Seed the database with the initial data."""

    # NOTE: Using the SHA with `create` makes the command a lot faster than using the plaintext with `create_user`.
    DEFAULT_PASSWORD_SHA = "pbkdf2_sha256$390000$Z9f11UhWReNZAE3Qs9gXoP$DbIx8EkwJi0ER4wtLQyAuRTTzAv9tExXNh5PZxsJZ78="

    def __init__(self):
        """Setup Faker and Python's random number generator.
        
        - Configures Faker to generate people from the UK, Germany,
          Italy and France.
        - Sets Faker and Python's default seeds to 1 to guarantee
          the same results each time the command is run.
        """
        super().__init__()
        self.faker = Faker(["en_GB", "de_DE", "it_IT", "fr_FR"])
        Faker.seed(1)
        random.seed(1)

    def add_objects_to_database(self, model_name, objects, exceptions=[]):
        """Add a collection of objects to the database.

        :param model_name: The name of the model that the objects belong to.
        :param objects: A list of dictionaries which describe the field-value
                        structure of each object.
        :parma exceptions: The names of any fields we don't want to consider
                           when checking to see if the object already exists
                           in the database.
        """
        model = apps.get_model(app_label="lessons", model_name=model_name)

        for obj in objects:
            # Generates copy of `obj` dictionary without fields specified in `exceptions` list
            obj_without_exceptions = {k: v for k, v in obj.items() if k not in exceptions}

            if model.objects.filter(**obj_without_exceptions).exists() == False:
                model.objects.create(**obj)

    def create_terms(self):
        """Create the six initial terms described in the brief.
        """
        terms = [{
            "order": 1,
            "start_date": "2022-09-01",
            "end_date": "2022-10-21"
        }, {
            "order": 2,
            "start_date": "2022-10-31",
            "end_date": "2022-12-16"
        }, {
            "order": 3,
            "start_date": "2023-01-03",
            "end_date": "2023-02-10"
        }, {
            "order": 4,
            "start_date": "2023-02-20",
            "end_date": "2023-03-31"
        }, {
            "order": 5,
            "start_date": "2023-04-17",
            "end_date": "2023-05-26"
        }, {
            "order": 6,
            "start_date": "2023-06-05",
            "end_date": "2023-07-21"
        }]

        self.add_objects_to_database("Term", terms)

    def create_teachers(self, number):
        """Generate an arbitrary number of teachers.

        :param number: The number of teachers.
        """
        teachers = []

        for _ in range(number):
            teachers.append({
                "first_name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
            })

        self.add_objects_to_database("Teacher", teachers)

    def create_students(self, number):
        """Generate an arbitrary number of students, including the
           "John Doe" user used for marking purposes.

        :param number: The number of users to generate. Must be 1 as it
                       always includes the "John Doe" user.
        """
        if number < 1:
            raise ValueError("Number of students must be >= 1.")

        students = [{
            "email": "john.doe@example.org",
            "password": self.DEFAULT_PASSWORD_SHA,
            "first_name": "John",
            "last_name": "Doe",
            "role": "Student",
        }]

        for _ in range(number - 1):
            students.append({
                "email": self.faker.email(),
                "password":
                    self.DEFAULT_PASSWORD_SHA,  # Reuse the same password because we have no way of knowing a random one
                "first_name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "role": "Student",
            })

        self.add_objects_to_database("User", students, exceptions=["password"])

    def create_administrators(self):
        """Create the administrator account described in the brief along with
           an additional one.
        """
        administrators = [{
            "email": "petra.pickles@example.org",
            "password": self.DEFAULT_PASSWORD_SHA,
            "first_name": "Petra",
            "last_name": "Pickles",
            "role": "Administrator",
        }, {
            "email": "orville.still@example.org",
            "password": self.DEFAULT_PASSWORD_SHA,
            "first_name": "Orville",
            "last_name": "Still",
            "role": "Administrator",
        }]

        self.add_objects_to_database("User", administrators, exceptions=["password"])

    def create_director(self):
        """Create the director account described in the brief."""
        directors = [{
            "email": "marty.major@example.org",
            "password": self.DEFAULT_PASSWORD_SHA,
            "first_name": "Marty",
            "last_name": "Major",
            "role": "Director",
        }]

        self.add_objects_to_database("User", directors, exceptions=["password"])

    def random_boolean(self):
        """Return a random Boolean."""
        return bool(random.randint(0, 1))

    def create_lesson_requests(self):
        """Generate a lesson request for each student, which is
           unfulfilled to begin with.
        """
        lesson_requests = []

        for user in User.objects.filter(role="Student"):
            # Either have nothing for further information or a 5-word sentence.
            further_information = random.choice([None, self.faker.sentence(nb_words=5)])

            lesson_requests.append({
                "is_available_on_monday": self.random_boolean(),
                "is_available_on_tuesday": self.random_boolean(),
                "is_available_on_wednesday": self.random_boolean(),
                "is_available_on_thursday": self.random_boolean(),
                "is_available_on_friday": self.random_boolean(),
                "no_of_lessons": random.randint(1, 10),
                "lesson_interval_in_days": random.choice([7, 14]),
                "lesson_duration_in_mins": random.choice([30, 45, 60]),
                "further_information": further_information,
                "user": user,
                "is_fulfilled": False,
            })

        self.add_objects_to_database("LessonRequest", lesson_requests, exceptions=["is_fulfilled"])

    def create_lessons_for_lesson_request(self, lesson_request):
        """Generate the lessons to fulfill a given lesson request.

        :param lesson_request: The lesson request to fulfill.
        """
        lessons = []

        for _ in range(lesson_request.no_of_lessons):
            new_date = self.faker.date_between(date(day=1, month=9, year=2022), date(day=21, month=7, year=2023))

            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])

            new_datetime = datetime(new_date.year, new_date.month, new_date.day, hour, minute, tzinfo=timezone.utc)

            lessons.append({
                "teacher": random.choice(Teacher.objects.all()),
                "datetime": new_datetime,
                "duration": lesson_request.lesson_duration_in_mins,
                "further_information": lesson_request.further_information,
                "user": lesson_request.user,
                "lesson_request": lesson_request,
            })

        self.add_objects_to_database("Lesson", lessons)

    def create_invoice_for_fulfilled_lesson_request(self, lesson_request):
        """Create an invoice for the lesson request specified.

        :param lesson_request: The lesson request to generate an invoice for.
        """
        invoice = {
            "lesson_request": lesson_request,
            "user": lesson_request.user,
        }

        self.add_objects_to_database("Invoice", [invoice])

    def fulfill_some_lesson_requests(self, number):
        """Set an arbitary number of lesson requests to be fulfilled, and
           generate lessons to fulfill them along with invoices.

        :param number: The number of lesson requests to fulfill.
        :raises ValueError: If the number of requested lessons to fulfill
                            exceeds the number that exist.
        """
        if LessonRequest.objects.all().count() < number:
            raise ValueError("Cannot fulfill more lesson requests than there are lesson requests.")

        # Have to order by `id` because Django QuerySets are unordered by
        # default which means [:number] would possibly get different requests
        # each time the command is run.
        lesson_requests = LessonRequest.objects.all().order_by("id")[:number]

        for lesson_request in lesson_requests:
            # Create the lessons
            self.create_lessons_for_lesson_request(lesson_request)

            # Fulfill the request
            lesson_request.is_fulfilled = True
            lesson_request.save()

            # Create an invoice for fulfilled request
            self.create_invoice_for_fulfilled_lesson_request(lesson_request)

    # NOTE: For some reason that I couldn't figure out, `random.uniform()`
    #       returns a float that is different each time despite setting
    #       the same seed for random, so I had to make a custom function
    #       that uses `random.randint()` internally.
    def randfloat(self, lower_bound, upper_bound):
        """Generate a random float between `lower_bound` and `upper_bound`.

        :param lower_bound: The lower bound.
        :param upper_bound: The upper bound.
        :return: A random float between the lower and upper bounds.
        """
        return random.randint(lower_bound * 100, upper_bound * 100) / 100.0

    def create_payments(self, number):
        """Create full and partial payments for an arbitrary number of invoices.

        :param number: The number of invoices to create payments for.
        :raises ValueError: If the no. of payments exceeds the no. of invoices
                            for which one could possibly make payments.
        """
        if Invoice.objects.all().count() < number:
            raise ValueError("Cannot create more payments than there are invoices for payments.")

        # Have to order by `id` because Django QuerySets are unordered by
        # default which means [:number] would possibly get different requests
        # each time the command is run.
        invoices = Invoice.objects.all().order_by("id")[:number]

        payments = []

        for invoice in invoices:
            invoice_amount = float(get_invoice_amount(invoice)[1:])  # Strip £ away

            # There is a 1/3 chance each of the user underpaying, paying the right amount
            # or overpaying. For the purposes of seeding, it's assumed a user would only
            # ever overpay by double the amount hence the `* 2`.
            amount_paid = random.choice([
                self.randfloat(0, invoice_amount),  # Underpaid
                invoice_amount,  # Paid right amount
                self.randfloat(invoice_amount, invoice_amount * 2)  # Overpaid
            ])

            # NOTE: Not sure whether "The associated payment should have been made." part
            #       in the brief meant John Doe made a full payment, so there's an exception
            #       for him to be on the safe side.
            if (invoice.user.email == "john.doe@example.org"):
                amount_paid = invoice_amount

            payments.append({"user": invoice.user, "invoice": invoice, "amount_paid": amount_paid})

        self.add_objects_to_database("Payment", payments)

    def handle(self, *args, **options):
        print("Seeding initial data...")

        try:
            self.create_terms()
            self.create_teachers(number=10)
            self.create_students(number=100)
            self.create_administrators()
            self.create_director()
            self.create_lesson_requests()
            self.fulfill_some_lesson_requests(number=70)
            self.create_payments(number=30)

            print("Data was successfully seeded.")
        except:
            raise CommandError("Unable to seed initial data.")