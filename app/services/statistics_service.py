"""Statistics service for member reservation analytics."""
from datetime import datetime
from sqlalchemy import func, or_, and_, extract
from sqlalchemy.sql import union_all
from app import db
from app.models import Member, Reservation, Court
import logging

logger = logging.getLogger(__name__)

# German month names
MONTH_NAMES_DE = {
    1: 'Jänner', 2: 'Februar', 3: 'März', 4: 'April',
    5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
}

# German day names
DAY_NAMES_DE = {
    0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag',
    4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'
}


class StatisticsService:
    """Service for generating member statistics from reservation data."""

    @staticmethod
    def get_member_statistics(member_id, year=None):
        """
        Generate comprehensive statistics for a member.

        Privacy constraint: Only includes data where the member is either
        booked_for or booked_by (direct involvement only).

        Args:
            member_id: UUID of the member
            year: Optional year filter (int). If None, returns all-time stats.

        Returns:
            tuple: (statistics dict or None, error message or None)
        """
        member = Member.query.get(member_id)
        if not member:
            return None, "Mitglied nicht gefunden"

        # Get available years for the dropdown
        available_years = StatisticsService._get_available_years(member_id)

        return {
            'member_id': str(member_id),
            'generated_at': datetime.utcnow().isoformat(),
            'selected_year': year,
            'available_years': available_years,
            'summary': StatisticsService._get_summary_stats(member_id, member, year),
            'partners': StatisticsService._get_partner_stats(member_id, year),
            'monthly_breakdown': StatisticsService._get_monthly_breakdown(member_id, year),
            'court_preferences': StatisticsService._get_court_preferences(member_id, year),
            'time_preferences': StatisticsService._get_time_preferences(member_id, year)
        }, None

    @staticmethod
    def _get_available_years(member_id):
        """Get list of years with booking data for the member."""
        results = db.session.query(
            extract('year', Reservation.date).label('year')
        ).filter(
            Reservation.booked_for_id == member_id,
            Reservation.status == 'active'
        ).distinct().order_by(
            extract('year', Reservation.date).desc()
        ).all()

        return [int(r.year) for r in results]

    @staticmethod
    def _get_summary_stats(member_id, member, year=None):
        """Get summary statistics for a member."""
        # Base filter for bookings where member is booked_for
        base_filter = [Reservation.booked_for_id == member_id]
        if year:
            base_filter.append(extract('year', Reservation.date) == year)

        # Total active bookings FOR this member
        total_bookings = Reservation.query.filter(
            *base_filter,
            Reservation.status == 'active'
        ).count()

        # Bookings made BY others FOR this member
        bookings_by_others = Reservation.query.filter(
            *base_filter,
            Reservation.booked_by_id != member_id,
            Reservation.status == 'active'
        ).count()

        # Cancellation stats
        cancelled_count = Reservation.query.filter(
            *base_filter,
            Reservation.status == 'cancelled'
        ).count()

        total_all_statuses = total_bookings + cancelled_count
        cancellation_rate = round((cancelled_count / total_all_statuses * 100), 1) if total_all_statuses > 0 else 0

        return {
            'total_bookings': total_bookings,
            'bookings_by_others': bookings_by_others,
            'cancellation_count': cancelled_count,
            'cancellation_rate': cancellation_rate,
            'member_since': member.created_at.strftime('%Y-%m-%d') if member.created_at else None
        }

    @staticmethod
    def _get_partner_stats(member_id, year=None):
        """
        Get players the member plays with most.

        Partners are determined by:
        1. Members I booked FOR (when I'm booked_by, they are booked_for)
        2. Members who booked FOR me (when I'm booked_for, they are booked_by)

        Excludes self-bookings (where booked_by == booked_for).
        """
        # Build year filter
        year_filter = []
        if year:
            year_filter.append(extract('year', Reservation.date) == year)

        # Case 1: People I booked for (I'm booked_by, they are booked_for)
        booked_for_others = db.session.query(
            Reservation.booked_for_id.label('partner_id')
        ).filter(
            Reservation.booked_by_id == member_id,
            Reservation.booked_for_id != member_id,
            Reservation.status == 'active',
            *year_filter
        )

        # Case 2: People who booked for me (I'm booked_for, they are booked_by)
        booked_by_others = db.session.query(
            Reservation.booked_by_id.label('partner_id')
        ).filter(
            Reservation.booked_for_id == member_id,
            Reservation.booked_by_id != member_id,
            Reservation.status == 'active',
            *year_filter
        )

        # Combine and count
        combined = union_all(booked_for_others, booked_by_others).subquery()

        partner_counts = db.session.query(
            combined.c.partner_id,
            func.count().label('play_count')
        ).group_by(combined.c.partner_id).order_by(func.count().desc()).limit(10).all()

        # Get member details for top partners
        top_partners = []
        for partner_id, count in partner_counts:
            partner = Member.query.get(partner_id)
            if partner and partner.is_active:
                # Get last played date
                last_played = StatisticsService._get_last_played_date(member_id, partner_id, year)

                top_partners.append({
                    'member_id': str(partner.id),
                    'name': partner.name,
                    'has_profile_picture': partner.has_profile_picture,
                    'profile_picture_version': partner.profile_picture_version,
                    'play_count': count,
                    'last_played': last_played.isoformat() if last_played else None
                })

        # Count unique partners
        unique_partner_ids = set(p[0] for p in partner_counts)

        return {
            'top_partners': top_partners,
            'total_unique_partners': len(unique_partner_ids)
        }

    @staticmethod
    def _get_last_played_date(member_id, partner_id, year=None):
        """Get the last date two members played together."""
        year_filter = []
        if year:
            year_filter.append(extract('year', Reservation.date) == year)

        return db.session.query(func.max(Reservation.date)).filter(
            or_(
                and_(Reservation.booked_by_id == member_id, Reservation.booked_for_id == partner_id),
                and_(Reservation.booked_for_id == member_id, Reservation.booked_by_id == partner_id)
            ),
            Reservation.status == 'active',
            *year_filter
        ).scalar()

    @staticmethod
    def _get_monthly_breakdown(member_id, year=None):
        """Get booking counts per month."""
        filters = [
            Reservation.booked_for_id == member_id,
            Reservation.status == 'active'
        ]
        if year:
            filters.append(extract('year', Reservation.date) == year)

        results = db.session.query(
            extract('year', Reservation.date).label('year'),
            extract('month', Reservation.date).label('month'),
            func.count(Reservation.id).label('count')
        ).filter(
            *filters
        ).group_by(
            extract('year', Reservation.date),
            extract('month', Reservation.date)
        ).order_by(
            extract('year', Reservation.date).desc(),
            extract('month', Reservation.date).desc()
        ).all()

        return [
            {
                'year': int(r.year),
                'month': int(r.month),
                'month_name': MONTH_NAMES_DE.get(int(r.month), ''),
                'count': r.count
            }
            for r in results
        ]

    @staticmethod
    def _get_court_preferences(member_id, year=None):
        """Get favorite courts."""
        filters = [
            Reservation.booked_for_id == member_id,
            Reservation.status == 'active'
        ]
        if year:
            filters.append(extract('year', Reservation.date) == year)

        results = db.session.query(
            Court.number,
            func.count(Reservation.id).label('count')
        ).join(Reservation, Reservation.court_id == Court.id).filter(
            *filters
        ).group_by(Court.number).order_by(func.count().desc()).all()

        total = sum(r.count for r in results)
        return [
            {
                'court_number': r.number,
                'count': r.count,
                'percentage': round(r.count / total * 100, 1) if total > 0 else 0
            }
            for r in results
        ]

    @staticmethod
    def _get_time_preferences(member_id, year=None):
        """Get favorite booking times and days."""
        filters = [
            Reservation.booked_for_id == member_id,
            Reservation.status == 'active'
        ]
        if year:
            filters.append(extract('year', Reservation.date) == year)

        # Time slot preferences
        time_results = db.session.query(
            Reservation.start_time,
            func.count(Reservation.id).label('count')
        ).filter(
            *filters
        ).group_by(Reservation.start_time).order_by(func.count().desc()).limit(5).all()

        total_time_bookings = sum(r.count for r in time_results)
        favorite_times = [
            {
                'time': r.start_time.strftime('%H:%M'),
                'count': r.count,
                'percentage': round(r.count / total_time_bookings * 100, 1) if total_time_bookings > 0 else 0
            }
            for r in time_results
        ]

        # Day of week preferences (using Python for DB compatibility)
        day_results = db.session.query(
            Reservation.date
        ).filter(
            *filters
        ).all()

        day_counts = {}
        for r in day_results:
            weekday = r.date.weekday()
            day_counts[weekday] = day_counts.get(weekday, 0) + 1

        total_days = sum(day_counts.values())
        favorite_days = [
            {
                'day': DAY_NAMES_DE[day],
                'day_index': day,
                'count': count,
                'percentage': round(count / total_days * 100, 1) if total_days > 0 else 0
            }
            for day, count in sorted(day_counts.items(), key=lambda x: -x[1])[:5]
        ]

        return {
            'favorite_time_slots': favorite_times,
            'favorite_days': favorite_days
        }
