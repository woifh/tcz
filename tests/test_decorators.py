"""Tests for authorization decorators."""
import pytest
from flask import Flask, jsonify
from flask_login import login_user, logout_user
from app.decorators import login_required_json, admin_required, member_or_admin_required
from app.models import Member


@pytest.fixture
def test_app(app):
    """Create test routes and return app with test client."""

    @app.route('/test/json-protected')
    @login_required_json
    def json_protected():
        return jsonify({'message': 'success'})

    @app.route('/test/admin-only')
    @admin_required
    def admin_only():
        return jsonify({'message': 'admin access'})

    @app.route('/test/member/<id>')
    @member_or_admin_required
    def member_route(id):
        return jsonify({'message': f'member {id}'})

    return app


@pytest.fixture
def test_client(test_app):
    """Create test client AFTER routes are registered."""
    return test_app.test_client()


class TestLoginRequiredJson:
    """Test login_required_json decorator."""

    def test_unauthenticated_json_request(self, test_client, test_app):
        """Test unauthenticated JSON request returns 401."""
        response = test_client.get('/test/json-protected',
                            headers={'Accept': 'application/json'})
        assert response.status_code == 401
        assert b'Authentifizierung erforderlich' in response.data

    def test_authenticated_request_succeeds(self, test_client, test_app, test_member):
        """Test authenticated request succeeds."""
        with test_client:
            test_client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = test_client.get('/test/json-protected')
            assert response.status_code == 200
            assert b'success' in response.data


class TestAdminRequired:
    """Test admin_required decorator."""

    def test_unauthenticated_returns_401(self, test_client, test_app):
        """Test unauthenticated request returns 401."""
        response = test_client.get('/test/admin-only',
                            headers={'Accept': 'application/json'})
        assert response.status_code == 401

    def test_non_admin_returns_403(self, test_client, test_app, test_member):
        """Test non-admin user returns 403."""
        with test_client:
            test_client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = test_client.get('/test/admin-only',
                                headers={'Accept': 'application/json'})
            assert response.status_code == 403
            assert b'keine Berechtigung' in response.data

    def test_admin_succeeds(self, test_client, test_app, test_admin):
        """Test admin user succeeds."""
        with test_client:
            test_client.post('/auth/login', data={
                'email': test_admin.email,
                'password': 'admin123'
            })
            response = test_client.get('/test/admin-only')
            assert response.status_code == 200
            assert b'admin access' in response.data


class TestMemberOrAdminRequired:
    """Test member_or_admin_required decorator."""

    def test_unauthenticated_returns_401(self, test_client, test_app):
        """Test unauthenticated request returns 401."""
        response = test_client.get('/test/member/1',
                            headers={'Accept': 'application/json'})
        assert response.status_code == 401

    def test_own_member_id_succeeds(self, test_client, test_app):
        """Test accessing own member ID succeeds."""
        with test_app.app_context():
            # Create a test member within app context
            member = Member(
                firstname='Test',
                lastname='User',
                email='testuser@example.com',
                role='member'
            )
            member.set_password('password123')
            from app import db
            db.session.add(member)
            db.session.commit()
            member_id = member.id
            member_email = member.email

        with test_client:
            test_client.post('/auth/login', data={
                'email': member_email,
                'password': 'password123'
            })
            response = test_client.get(f'/test/member/{member_id}')
            assert response.status_code == 200

    def test_different_member_id_returns_403(self, test_client, test_app, test_member):
        """Test accessing different member ID returns 403."""
        with test_client:
            test_client.post('/auth/login', data={
                'email': test_member.email,
                'password': 'password123'
            })
            response = test_client.get('/test/member/999',
                                headers={'Accept': 'application/json'})
            assert response.status_code == 403

    def test_admin_can_access_any_member(self, test_client, test_app):
        """Test admin can access any member ID."""
        with test_app.app_context():
            # Create admin and member within app context
            from app import db
            admin = Member(
                firstname='Admin',
                lastname='User',
                email='admintest@example.com',
                role='administrator'
            )
            admin.set_password('admin123')
            member = Member(
                firstname='Regular',
                lastname='User',
                email='regularuser@example.com',
                role='member'
            )
            member.set_password('password123')
            db.session.add_all([admin, member])
            db.session.commit()
            admin_email = admin.email
            member_id = member.id

        with test_client:
            test_client.post('/auth/login', data={
                'email': admin_email,
                'password': 'admin123'
            })
            response = test_client.get(f'/test/member/{member_id}')
            assert response.status_code == 200
