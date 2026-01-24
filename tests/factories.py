"""Factory Boy factories for test data generation."""
import uuid
from datetime import date, time

import factory
from factory.alchemy import SQLAlchemyModelFactory
from werkzeug.security import generate_password_hash

from app import db
from app.models import (
    Member, Court, Reservation, Block, BlockReason,
    Notification, DeviceToken
)


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory with SQLAlchemy session configuration."""

    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'commit'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to use current db.session."""
        cls._meta.sqlalchemy_session = db.session
        return super()._create(model_class, *args, **kwargs)


class MemberFactory(BaseFactory):
    """Factory for Member model."""

    class Meta:
        model = Member

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    firstname = factory.Sequence(lambda n: f'Test{n}')
    lastname = factory.Sequence(lambda n: f'User{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    role = 'member'
    is_active = True
    membership_type = 'full'
    fee_paid = True

    @factory.lazy_attribute
    def password_hash(self):
        """Generate password hash for default password 'password123'."""
        return generate_password_hash('password123', method='pbkdf2:sha256')

    class Params:
        admin = factory.Trait(
            role='administrator',
            firstname='Admin',
        )
        teamster = factory.Trait(
            role='teamster',
            firstname='Teamster',
        )
        inactive = factory.Trait(
            is_active=False,
        )
        sustaining = factory.Trait(
            membership_type='sustaining',
        )
        unpaid = factory.Trait(
            fee_paid=False,
        )


class CourtFactory(BaseFactory):
    """Factory for Court model."""

    class Meta:
        model = Court

    number = factory.Sequence(lambda n: (n % 6) + 1)


class BlockReasonFactory(BaseFactory):
    """Factory for BlockReason model."""

    class Meta:
        model = BlockReason

    name = factory.Sequence(lambda n: f'Test Reason {n}')
    is_active = True
    teamster_usable = False
    is_temporary = False
    created_by = factory.SubFactory(MemberFactory, admin=True)


class ReservationFactory(BaseFactory):
    """Factory for Reservation model."""

    class Meta:
        model = Reservation

    court = factory.SubFactory(CourtFactory)
    date = factory.LazyFunction(date.today)
    start_time = factory.LazyFunction(lambda: time(10, 0))
    end_time = factory.LazyFunction(lambda: time(11, 0))
    booked_by = factory.SubFactory(MemberFactory)
    booked_for = factory.LazyAttribute(lambda o: o.booked_by)
    status = 'active'
    is_short_notice = False

    @factory.lazy_attribute
    def court_id(self):
        """Get court_id from court relation."""
        return self.court.id if self.court else None

    @factory.lazy_attribute
    def booked_by_id(self):
        """Get booked_by_id from booked_by relation."""
        return self.booked_by.id if self.booked_by else None

    @factory.lazy_attribute
    def booked_for_id(self):
        """Get booked_for_id from booked_for relation."""
        return self.booked_for.id if self.booked_for else None

    class Params:
        cancelled = factory.Trait(
            status='cancelled',
        )
        suspended = factory.Trait(
            status='suspended',
        )
        short_notice = factory.Trait(
            is_short_notice=True,
        )


class BlockFactory(BaseFactory):
    """Factory for Block model."""

    class Meta:
        model = Block

    court = factory.SubFactory(CourtFactory)
    date = factory.LazyFunction(date.today)
    start_time = factory.LazyFunction(lambda: time(8, 0))
    end_time = factory.LazyFunction(lambda: time(12, 0))
    reason_obj = factory.SubFactory(BlockReasonFactory)
    created_by = factory.SubFactory(MemberFactory, admin=True)
    details = None
    batch_id = None

    @factory.lazy_attribute
    def court_id(self):
        """Get court_id from court relation."""
        return self.court.id if self.court else None

    @factory.lazy_attribute
    def reason_id(self):
        """Get reason_id from reason_obj relation."""
        return self.reason_obj.id if self.reason_obj else None

    @factory.lazy_attribute
    def created_by_id(self):
        """Get created_by_id from created_by relation."""
        return self.created_by.id if self.created_by else None


class NotificationFactory(BaseFactory):
    """Factory for Notification model."""

    class Meta:
        model = Notification

    recipient = factory.SubFactory(MemberFactory)
    type = 'booking_confirmation'
    message = factory.Sequence(lambda n: f'Test notification message {n}')
    read = False

    @factory.lazy_attribute
    def recipient_id(self):
        """Get recipient_id from recipient relation."""
        return self.recipient.id if self.recipient else None


class DeviceTokenFactory(BaseFactory):
    """Factory for DeviceToken model."""

    class Meta:
        model = DeviceToken

    member = factory.SubFactory(MemberFactory)
    token = factory.Sequence(lambda n: f'device_token_{n}_{uuid.uuid4().hex[:8]}')
    platform = 'ios'
    is_active = True

    @factory.lazy_attribute
    def member_id(self):
        """Get member_id from member relation."""
        return self.member.id if self.member else None
