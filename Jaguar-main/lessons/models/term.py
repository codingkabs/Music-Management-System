from django.db import models

# Create class for terms, with the start and end date
class Term(models.Model):
    # Represents order in year, e.g. is this second term out of the six terms in a year?
    order = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        date_format = "%d %B %Y"  # Date format of DAY/MONTH/YEAR, eg: "06 January 2023"

        formatted_start_date = self.start_date.strftime(date_format)
        formatted_end_date = self.end_date.strftime(date_format)

        term_name = f"Term {self.order} ({formatted_start_date} - {formatted_end_date})"

        return term_name
