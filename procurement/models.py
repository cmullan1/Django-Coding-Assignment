from django.db import models
from django.utils.timezone import now as timezone_now

MONTH = 30 * 24 * 60 * 60
WEEK = 7 * 24 * 60 * 60
DAY = 24 * 60 * 60
HOUR = 60 * 60
MINUTE = 60


class DashboardModel(models.Model):
    """
    Abstract base model for things which will be displayed on the dashboard, adds in created and updated fields,
    and provides a convenience method which provides a nicely formatted string of the time since update.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def time_since_update(self):
        update_delta = timezone_now() - self.updated
        seconds_since_update = update_delta.seconds

        if seconds_since_update / MONTH >= 1:
            quantity = seconds_since_update / MONTH
            units = 'months' if quantity > 1 else 'month'

        elif seconds_since_update / WEEK >= 1:
            quantity = seconds_since_update / WEEK
            units = 'weeks' if quantity > 1 else 'week'

        elif seconds_since_update / DAY >= 1:
            quantity = seconds_since_update / DAY
            units = 'days' if quantity > 1 else 'day'

        elif seconds_since_update / HOUR >= 1:
            quantity = seconds_since_update / HOUR
            units = 'hours' if quantity > 1 else 'hour'

        elif seconds_since_update / MINUTE >= 1:
            quantity = seconds_since_update / MINUTE
            units = 'minutes' if quantity > 1 else 'minute'

        else:
            return "updated just now"

        # Ensure the quantity output is rounded to 2 decimal places
        base_string = 'updated {quantity:.2f} {units} ago'
        return base_string.format(quantity=quantity, units=units)


class Supplier(DashboardModel):
    """
    Model which represents an individual or organisation which supplies components
    """
    name = models.CharField(max_length=255)
    # CMM -- Moved the representative name and email to the the Representative model
    #representative_name = models.CharField(max_length=255, null=True, blank=True)
    #representative_email = models.EmailField(max_length=255, null=True, blank=True)
    is_authorized = models.BooleanField()
    
    """
    CMM -- Added ordering by name for consistency with the other model classes and
    to order the displayed suppliers alphabetically
    """
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return '{}'.format(self.name)


"""
CMM -- Added the Representative model class to allow each supplier to have more than
       one representative
"""
class Representative(DashboardModel):
    """
    CMM -- Model which represents a supplier's representative.
    """
    representative_name = models.CharField(max_length=255)
    representative_email = models.EmailField(max_length=255, null=True, blank=True)

    """
    CMM -- Added the supplier as a foreign key.  Allowed cascading deletes (if the supplier is deleted, 
           associated representatives are also deleted.
    """
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    class Meta:
        ordering = ("representative_name",)

    def __str__(self):
        return '{}'.format(self.representative_name)


class Component(DashboardModel):
    """
    Model which represents items which may be supplied.
    """
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50)
    suppliers = models.ManyToManyField(Supplier, related_name='components', blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return '{} ({})'.format(
            self.name,
            self.sku
        )
