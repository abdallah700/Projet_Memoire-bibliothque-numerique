# bookstore/cron.py

from django.utils import timezone

from .models import Reservation, CancelledReservation


class CancelExpiredReservations(CronJobBase):
    RUN_EVERY_MINS = 1  # run every minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bookstore.cancel_expired_reservations'  # a unique code

    def do(self):
        now = timezone.now()
        expired_reservations = Reservation.objects.filter(expiration_date__lte=now)
        for reservation in expired_reservations:
            CancelledReservation.objects.create(
                user=reservation.user,
                book=reservation.book,
                added_at=reservation.added_at,
            )
            reservation.book.nbr_exemplaire += 1
            reservation.book.save()
            reservation.delete()
