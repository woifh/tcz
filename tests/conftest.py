"""Pytest configuration and fixtures.

This module uses Factory Boy for test data generation. See tests/factories.py
for available factories:

    from tests.factories import MemberFactory, CourtFactory, ReservationFactory

Example usage in tests:
    member = MemberFactory()                    # Basic member
    admin = MemberFactory(admin=True)           # Admin user
    member = MemberFactory(email='custom@x.com') # Override fields
"""
import pytest
from app import create_app, db
from app.models import Member, Court, BlockReason
from flask_mailman import Mail
from tests.factories import MemberFactory, CourtFactory, BlockReasonFactory


@pytest.fixture
def app():
    """Create application for testing.

    Pre-creates:
    - 6 courts (numbers 1-6)
    - System admin (system@example.com)
    - 5 default block reasons
    """
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Create courts (use direct creation for fixed setup data)
        for i in range(1, 7):
            court = Court(number=i)
            db.session.add(court)

        # Create a default admin for block reasons
        admin = Member(
            firstname='System',
            lastname='Admin',
            email='system@example.com',
            role='administrator'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

        # Create default block reasons
        default_reasons = ['Maintenance', 'Weather', 'Tournament', 'Championship', 'Tennis Course']
        for reason_name in default_reasons:
            reason = BlockReason(
                name=reason_name,
                is_active=True,
                created_by_id=admin.id
            )
            db.session.add(reason)

        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


class MemberData:
    """Simple data holder for member info that doesn't require session.

    Used by fixtures to return member data without SQLAlchemy session issues.
    Consider using MemberFactory directly in tests for more flexibility.
    """
    def __init__(self, id, email, firstname, lastname, role):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role

    @property
    def name(self):
        """Return full name like the Member model does."""
        return f"{self.firstname} {self.lastname}"


@pytest.fixture
def test_member(app):
    """Create a test member and return its data.

    Uses MemberFactory. Password is 'password123'.
    For more control, use MemberFactory directly in your test.
    """
    with app.app_context():
        member = MemberFactory(
            firstname='Test',
            lastname='Member',
            email='test@example.com',
        )
        return MemberData(
            id=member.id,
            email=member.email,
            firstname=member.firstname,
            lastname=member.lastname,
            role=member.role
        )


@pytest.fixture
def test_admin(app):
    """Create a test admin and return its data.

    Uses MemberFactory with admin=True. Password is 'admin123'.
    For more control, use MemberFactory directly in your test.
    """
    with app.app_context():
        admin = MemberFactory(
            admin=True,
            firstname='Test',
            lastname='Admin',
            email='admin@example.com',
        )
        # Override default password for backward compatibility with existing tests
        admin.set_password('admin123')
        db.session.commit()
        return MemberData(
            id=admin.id,
            email=admin.email,
            firstname=admin.firstname,
            lastname=admin.lastname,
            role=admin.role
        )


@pytest.fixture
def mail(app):
    """Create mail instance for testing."""
    from flask_mailman import Mail
    mail = Mail(app)
    return mail


@pytest.fixture
def database(app):
    """Provide database access within app context."""
    return db
