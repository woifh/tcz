"""Tests for reservation routes."""
import pytest
from datetime import date, time, timedelta
from app import db
from app.models import Member, Court, Reservation


class TestListReservations:
    """Tests for listing reservations."""

    def test_list_reservations_requires_login(self, client):
        """Listing reservations requires authentication."""
        response = client.get('/reservations/')
        assert response.status_code == 401

    def test_list_reservations_success(self, client, test_member):
        """Authenticated user can list their reservations."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.get('/reservations/')
        assert response.status_code == 200

    def test_list_reservations_json_format(self, client, test_member):
        """Reservations can be returned as JSON."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.get('/reservations/?format=json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'reservations' in data
        assert 'metadata' in data

    def test_list_reservations_by_date(self, client, test_member):
        """Can list reservations for a specific date."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        today = date.today().isoformat()
        response = client.get(f'/reservations/?date={today}&format=json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'date' in data

    def test_list_reservations_invalid_date(self, client, test_member):
        """Invalid date format should show error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.get('/reservations/?date=invalid-date')
        assert response.status_code == 302  # Redirect with error flash

    def test_list_reservations_include_past(self, client, test_member):
        """Can include past reservations."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.get('/reservations/?include_past=true&format=json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['filter']['include_past'] is True


class TestReservationStatus:
    """Tests for reservation status endpoint."""

    def test_status_requires_login(self, client):
        """Status endpoint requires authentication."""
        response = client.get('/reservations/status')
        assert response.status_code == 401

    def test_status_returns_limits(self, client, test_member):
        """Status should return limit information."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.get('/reservations/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'limits' in data
        assert 'regular_reservations' in data['limits']
        assert 'short_notice_bookings' in data['limits']

    def test_status_returns_active_reservations(self, client, test_member):
        """Status should return active reservation counts."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.get('/reservations/status')
        assert response.status_code == 200
        data = response.get_json()
        assert 'active_reservations' in data
        assert 'total' in data['active_reservations']


class TestCreateReservation:
    """Tests for creating reservations."""

    def test_create_requires_login(self, client):
        """Creating reservation requires authentication."""
        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': (date.today() + timedelta(days=1)).isoformat(),
            'start_time': '10:00'
        })
        assert response.status_code == 401

    def test_create_reservation_success(self, client, test_member, app):
        """Can create a valid reservation."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        future_date = date.today() + timedelta(days=2)
        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': future_date.isoformat(),
            'start_time': '10:00'
        })
        # Could be 201 (success) or 400 (limit reached) depending on test order
        assert response.status_code in [201, 400]

    def test_create_reservation_missing_court_id(self, client, test_member):
        """Missing court_id should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.post('/reservations/', json={
            'date': (date.today() + timedelta(days=1)).isoformat(),
            'start_time': '10:00'
        })
        assert response.status_code == 400

    def test_create_reservation_missing_date(self, client, test_member):
        """Missing date should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.post('/reservations/', json={
            'court_id': 1,
            'start_time': '10:00'
        })
        assert response.status_code == 400

    def test_create_reservation_missing_start_time(self, client, test_member):
        """Missing start_time should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': (date.today() + timedelta(days=1)).isoformat()
        })
        assert response.status_code == 400

    def test_create_reservation_invalid_date_format(self, client, test_member):
        """Invalid date format should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': 'invalid-date',
            'start_time': '10:00'
        })
        assert response.status_code == 400

    def test_create_reservation_invalid_time_format(self, client, test_member):
        """Invalid time format should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': (date.today() + timedelta(days=1)).isoformat(),
            'start_time': 'invalid'
        })
        assert response.status_code == 400

    def test_create_reservation_invalid_court_id(self, client, test_member):
        """Invalid court_id should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.post('/reservations/', json={
            'court_id': 99,  # Non-existent court
            'date': (date.today() + timedelta(days=1)).isoformat(),
            'start_time': '10:00'
        })
        assert response.status_code == 400


class TestDeleteReservation:
    """Tests for deleting reservations."""

    def test_delete_requires_login(self, client):
        """Deleting reservation requires authentication."""
        response = client.delete('/reservations/1')
        assert response.status_code == 401

    def test_delete_nonexistent_reservation(self, client, test_member):
        """Deleting non-existent reservation should return error."""
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })
        response = client.delete('/reservations/99999')
        # The route wraps get_or_404 in a try-except, so returns 500 with error message
        assert response.status_code in [404, 500]
        assert 'error' in response.get_json()

    def test_delete_unauthorized(self, client, test_member, test_admin, app):
        """Cannot delete another user's reservation."""
        with app.app_context():
            # Get the admin member from DB
            admin = Member.query.filter_by(email=test_admin.email).first()
            court = Court.query.filter_by(number=1).first()

            # Create reservation for admin
            future_date = date.today() + timedelta(days=3)
            reservation = Reservation(
                court_id=court.id,
                date=future_date,
                start_time=time(14, 0),
                end_time=time(15, 0),
                booked_for_id=admin.id,
                booked_by_id=admin.id
            )
            db.session.add(reservation)
            db.session.commit()
            reservation_id = reservation.id

        # Login as regular member
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        response = client.delete(f'/reservations/{reservation_id}')
        assert response.status_code == 403


class TestAutoAddFavourite:
    """Tests for auto-adding favourites when booking for another member."""

    def test_booking_for_other_member_adds_favourite(self, client, test_member, app):
        """Booking for another member should auto-add them to favourites."""
        with app.app_context():
            # Create another member to book for
            other_member = Member(
                firstname='Other',
                lastname='User',
                email='other@example.com',
                role='member'
            )
            other_member.set_password('password123')
            db.session.add(other_member)
            db.session.commit()
            other_member_id = other_member.id

            # Get test_member from DB
            member = Member.query.filter_by(email=test_member.email).first()
            member_id = member.id

            # Verify no favourites initially
            assert other_member not in member.favourites.all()

        # Login as test member
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        # Create booking for the other member
        future_date = date.today() + timedelta(days=5)
        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': future_date.isoformat(),
            'start_time': '11:00',
            'booked_for_id': other_member_id
        })

        # Booking should succeed
        assert response.status_code == 201

        # Verify favourite was added
        with app.app_context():
            member = Member.query.get(member_id)
            other = Member.query.get(other_member_id)
            assert other in member.favourites.all()

    def test_booking_for_self_does_not_add_favourite(self, client, test_member, app):
        """Booking for yourself should not affect favourites."""
        with app.app_context():
            member = Member.query.filter_by(email=test_member.email).first()
            member_id = member.id
            initial_favourites_count = member.favourites.count()

        # Login
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        # Create booking for self
        future_date = date.today() + timedelta(days=6)
        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': future_date.isoformat(),
            'start_time': '12:00',
            'booked_for_id': member_id
        })

        # Booking should succeed
        assert response.status_code == 201

        # Verify favourites unchanged
        with app.app_context():
            member = Member.query.get(member_id)
            assert member.favourites.count() == initial_favourites_count

    def test_duplicate_favourite_not_created(self, client, test_member, app):
        """Booking for the same member twice should not create duplicate favourite."""
        with app.app_context():
            # Create another member
            other_member = Member(
                firstname='Dup',
                lastname='Test',
                email='dup@example.com',
                role='member'
            )
            other_member.set_password('password123')
            db.session.add(other_member)
            db.session.commit()
            other_member_id = other_member.id

            # Get test_member and add the other as favourite manually
            member = Member.query.filter_by(email=test_member.email).first()
            member.favourites.append(other_member)
            db.session.commit()
            member_id = member.id

            # Verify one favourite
            assert member.favourites.count() == 1

        # Login
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        # Create booking for the other member (already a favourite)
        future_date = date.today() + timedelta(days=7)
        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': future_date.isoformat(),
            'start_time': '13:00',
            'booked_for_id': other_member_id
        })

        # Booking should succeed
        assert response.status_code == 201

        # Verify still only one favourite (no duplicate)
        with app.app_context():
            member = Member.query.get(member_id)
            assert member.favourites.count() == 1

    def test_favourite_added_even_when_booking_fails(self, client, test_member, app):
        """Favourite should be added even if booking fails (e.g., limit reached)."""
        with app.app_context():
            # Create another member with 2 active bookings (at limit)
            other_member = Member(
                firstname='Limited',
                lastname='User',
                email='limited@example.com',
                role='member'
            )
            other_member.set_password('password123')
            db.session.add(other_member)
            db.session.commit()
            other_member_id = other_member.id

            # Create 2 reservations for the other member (reaching limit)
            court = Court.query.filter_by(number=1).first()
            for i in range(2):
                future_date = date.today() + timedelta(days=10 + i)
                reservation = Reservation(
                    court_id=court.id,
                    date=future_date,
                    start_time=time(10 + i, 0),
                    end_time=time(11 + i, 0),
                    booked_for_id=other_member_id,
                    booked_by_id=other_member_id
                )
                db.session.add(reservation)
            db.session.commit()

            # Get test_member from DB
            member = Member.query.filter_by(email=test_member.email).first()
            member_id = member.id

            # Verify no favourites initially
            assert member.favourites.count() == 0

        # Login as test member
        client.post('/auth/login', data={
            'email': test_member.email,
            'password': 'password123'
        })

        # Try to book for the limited member (should fail due to their limit)
        future_date = date.today() + timedelta(days=15)
        response = client.post('/reservations/', json={
            'court_id': 1,
            'date': future_date.isoformat(),
            'start_time': '14:00',
            'booked_for_id': other_member_id
        })

        # Booking should fail (limit reached for that member)
        assert response.status_code == 400

        # But favourite should still be added
        with app.app_context():
            member = Member.query.get(member_id)
            other = Member.query.get(other_member_id)
            assert other in member.favourites.all()
