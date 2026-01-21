"""Tests for profile picture fields in API responses."""
import pytest
from datetime import date, time
from app import db
from app.models import Court, Reservation, Member


class TestAvailabilityProfilePictureFields:
    """Test profile picture fields in court availability API."""

    def test_availability_includes_profile_picture_fields_for_authenticated(self, client, test_member, app):
        """Test availability includes profile picture fields for authenticated users."""
        court_id = None
        with app.app_context():
            court = Court.query.first()
            court_id = court.id
            # Set up profile picture on test member
            member = Member.query.get(test_member.id)
            member.has_profile_picture = True
            member.profile_picture_version = 3
            db.session.commit()

            reservation = Reservation(
                court_id=court.id,
                date=date(2026, 12, 5),
                start_time=time(10, 0),
                end_time=time(11, 0),
                booked_for_id=test_member.id,
                booked_by_id=test_member.id,
                status='active'
            )
            db.session.add(reservation)
            db.session.commit()

        with client:
            client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = client.get('/api/courts/availability?date=2026-12-05')
            assert response.status_code == 200
            data = response.get_json()

            court_data = next((c for c in data['courts'] if c['court_id'] == court_id), None)
            assert court_data is not None
            slot = next((s for s in court_data['occupied'] if s['time'] == '10:00'), None)
            assert slot is not None

            assert 'booked_for_has_profile_picture' in slot['details']
            assert slot['details']['booked_for_has_profile_picture'] is True
            assert 'booked_for_profile_picture_version' in slot['details']
            assert slot['details']['booked_for_profile_picture_version'] == 3
            assert 'booked_by_has_profile_picture' in slot['details']
            assert slot['details']['booked_by_has_profile_picture'] is True
            assert 'booked_by_profile_picture_version' in slot['details']
            assert slot['details']['booked_by_profile_picture_version'] == 3

    def test_availability_profile_fields_with_no_profile_picture(self, client, test_member, app):
        """Test availability returns false for members without profile pictures."""
        court_id = None
        with app.app_context():
            court = Court.query.first()
            court_id = court.id
            # Ensure member has no profile picture
            member = Member.query.get(test_member.id)
            member.has_profile_picture = False
            member.profile_picture_version = 0
            db.session.commit()

            reservation = Reservation(
                court_id=court.id,
                date=date(2026, 12, 6),
                start_time=time(14, 0),
                end_time=time(15, 0),
                booked_for_id=test_member.id,
                booked_by_id=test_member.id,
                status='active'
            )
            db.session.add(reservation)
            db.session.commit()

        with client:
            client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = client.get('/api/courts/availability?date=2026-12-06')
            assert response.status_code == 200
            data = response.get_json()

            court_data = next((c for c in data['courts'] if c['court_id'] == court_id), None)
            slot = next((s for s in court_data['occupied'] if s['time'] == '14:00'), None)

            assert slot['details']['booked_for_has_profile_picture'] is False
            assert slot['details']['booked_for_profile_picture_version'] == 0

    def test_availability_hides_profile_fields_from_anonymous(self, client, test_member, app):
        """Test availability hides profile picture fields from anonymous users."""
        court_id = None
        with app.app_context():
            court = Court.query.first()
            court_id = court.id
            reservation = Reservation(
                court_id=court.id,
                date=date(2026, 12, 7),
                start_time=time(10, 0),
                end_time=time(11, 0),
                booked_for_id=test_member.id,
                booked_by_id=test_member.id,
                status='active'
            )
            db.session.add(reservation)
            db.session.commit()

        # Anonymous request
        response = client.get('/api/courts/availability?date=2026-12-07')
        assert response.status_code == 200
        data = response.get_json()

        court_data = next((c for c in data['courts'] if c['court_id'] == court_id), None)
        slot = next((s for s in court_data['occupied'] if s['time'] == '10:00'), None)

        # Details should be None for anonymous users
        assert slot['details'] is None


class TestReservationProfilePictureFields:
    """Test profile picture fields in reservation API."""

    def test_reservation_list_includes_booked_by_profile_fields(self, client, test_member, app):
        """Test reservation list includes booked_by profile picture fields."""
        with app.app_context():
            court = Court.query.first()
            member = Member.query.get(test_member.id)
            member.has_profile_picture = True
            member.profile_picture_version = 2
            db.session.commit()

            reservation = Reservation(
                court_id=court.id,
                date=date(2026, 12, 8),
                start_time=time(10, 0),
                end_time=time(11, 0),
                booked_for_id=test_member.id,
                booked_by_id=test_member.id,
                status='active'
            )
            db.session.add(reservation)
            db.session.commit()

        with client:
            client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = client.get('/api/reservations/')
            assert response.status_code == 200
            data = response.get_json()

            assert 'reservations' in data
            assert len(data['reservations']) > 0
            res = data['reservations'][0]

            # Check booked_for fields (already existed)
            assert 'booked_for_has_profile_picture' in res
            assert res['booked_for_has_profile_picture'] is True
            assert 'booked_for_profile_picture_version' in res
            assert res['booked_for_profile_picture_version'] == 2

            # Check new booked_by fields
            assert 'booked_by' in res
            assert 'booked_by_has_profile_picture' in res
            assert res['booked_by_has_profile_picture'] is True
            assert 'booked_by_profile_picture_version' in res
            assert res['booked_by_profile_picture_version'] == 2

    def test_reservation_different_booker_profile_fields(self, client, test_member, test_admin, app):
        """Test reservation shows different profile fields when booked_for != booked_by."""
        with app.app_context():
            court = Court.query.first()

            # Set up different profile states
            member = Member.query.get(test_member.id)
            member.has_profile_picture = True
            member.profile_picture_version = 5

            admin = Member.query.get(test_admin.id)
            admin.has_profile_picture = False
            admin.profile_picture_version = 0
            db.session.commit()

            # Admin books for member
            reservation = Reservation(
                court_id=court.id,
                date=date(2026, 12, 9),
                start_time=time(11, 0),
                end_time=time(12, 0),
                booked_for_id=test_member.id,
                booked_by_id=test_admin.id,
                status='active'
            )
            db.session.add(reservation)
            db.session.commit()

        with client:
            client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = client.get('/api/reservations/')
            data = response.get_json()

            res = next((r for r in data['reservations'] if r['date'] == '2026-12-09'), None)
            assert res is not None

            # booked_for (member) has profile picture
            assert res['booked_for_has_profile_picture'] is True
            assert res['booked_for_profile_picture_version'] == 5

            # booked_by (admin) has no profile picture
            assert res['booked_by_has_profile_picture'] is False
            assert res['booked_by_profile_picture_version'] == 0


class TestFavouritesProfilePictureFields:
    """Test profile picture fields in favourites API."""

    def test_favourites_includes_profile_picture_fields(self, client, test_member, test_admin, app):
        """Test favourites list includes profile picture fields."""
        with app.app_context():
            admin = Member.query.get(test_admin.id)
            admin.has_profile_picture = True
            admin.profile_picture_version = 5
            # Ensure admin is a full member so they appear in favourites
            admin.membership_type = 'full'
            admin.is_active = True
            db.session.commit()

            member = Member.query.get(test_member.id)
            member.favourites.append(admin)
            db.session.commit()

        with client:
            client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = client.get(f'/api/members/{test_member.id}/favourites')
            assert response.status_code == 200
            data = response.get_json()

            assert 'favourites' in data
            assert len(data['favourites']) > 0

            fav = data['favourites'][0]
            assert 'has_profile_picture' in fav
            assert fav['has_profile_picture'] is True
            assert 'profile_picture_version' in fav
            assert fav['profile_picture_version'] == 5

    def test_favourites_without_profile_picture(self, client, test_member, test_admin, app):
        """Test favourites list shows false for members without profile pictures."""
        with app.app_context():
            admin = Member.query.get(test_admin.id)
            admin.has_profile_picture = False
            admin.profile_picture_version = 0
            admin.membership_type = 'full'
            admin.is_active = True
            db.session.commit()

            member = Member.query.get(test_member.id)
            # Clear existing favourites first
            member.favourites = []
            db.session.commit()
            member.favourites.append(admin)
            db.session.commit()

        with client:
            client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = client.get(f'/api/members/{test_member.id}/favourites')
            data = response.get_json()

            fav = data['favourites'][0]
            assert fav['has_profile_picture'] is False
            assert fav['profile_picture_version'] == 0
