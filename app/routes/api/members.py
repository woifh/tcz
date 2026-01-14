"""
API Members Module

Member search and favourites management for mobile apps.
"""

from flask import request, jsonify
from flask_login import current_user

from app import db
from app.models import Member
from app.services.member_service import MemberService
from app.decorators.auth import jwt_or_session_required
from . import bp


@bp.route('/members/search', methods=['GET'])
@jwt_or_session_required
def search_members():
    """Search for members by name or email."""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'error': 'Suchbegriff erforderlich'}), 400

    try:
        results = MemberService.search_members(query, current_user.id)

        return jsonify({
            'results': [m.to_dict() for m in results],
            'count': len(results)
        })
    except Exception:
        return jsonify({'error': 'Suchfehler. Bitte versuchen Sie es erneut.'}), 500


@bp.route('/members/<id>/favourites', methods=['GET'])
@jwt_or_session_required
def get_favourites(id):
    """Get user's favourites."""
    try:
        member = Member.query.get_or_404(id)

        if member.id != current_user.id:
            return jsonify({'error': 'Sie haben keine Berechtigung für diese Aktion'}), 403

        favourites = member.favourites.all()

        return jsonify({
            'favourites': [
                fav.to_dict()
                for fav in favourites
                if fav.membership_type == 'full' and fav.is_active
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/members/<id>/favourites', methods=['POST'])
@jwt_or_session_required
def add_favourite(id):
    """Add a favourite member."""
    try:
        member = Member.query.get_or_404(id)

        if member.id != current_user.id:
            return jsonify({'error': 'Sie haben keine Berechtigung für diese Aktion'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON body required'}), 400

        favourite_id = data.get('favourite_id')
        if not favourite_id:
            return jsonify({'error': 'favourite_id ist erforderlich'}), 400

        favourite = Member.query.get_or_404(favourite_id)

        if favourite.id == member.id:
            return jsonify({'error': 'Sie können sich nicht selbst als Favorit hinzufügen'}), 400

        if favourite in member.favourites.all():
            return jsonify({'error': 'Mitglied ist bereits ein Favorit'}), 400

        member.favourites.append(favourite)
        db.session.commit()

        return jsonify({
            'message': 'Favorit erfolgreich hinzugefügt',
            'favourite': favourite.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/members/<id>/favourites/<fav_id>', methods=['DELETE'])
@jwt_or_session_required
def remove_favourite(id, fav_id):
    """Remove a favourite member."""
    try:
        member = Member.query.get_or_404(id)

        if member.id != current_user.id:
            return jsonify({'error': 'Sie haben keine Berechtigung für diese Aktion'}), 403

        favourite = Member.query.get_or_404(fav_id)

        if favourite not in member.favourites.all():
            return jsonify({'error': 'Mitglied ist kein Favorit'}), 404

        member.favourites.remove(favourite)
        db.session.commit()

        return jsonify({'message': 'Favorit erfolgreich entfernt'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ----- Member Profile Routes -----

@bp.route('/members/<id>', methods=['GET'])
@jwt_or_session_required
def get_member_profile(id):
    """Get member profile (own profile or admin access)."""
    try:
        member = Member.query.get_or_404(id)

        # Users can only view their own profile (admins use /api/admin/members/<id>)
        if member.id != current_user.id and not current_user.is_admin():
            return jsonify({'error': 'Sie haben keine Berechtigung für diese Aktion'}), 403

        include_admin = current_user.is_admin()
        return jsonify(member.to_dict(include_admin_fields=include_admin))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/members/<id>', methods=['PUT'])
@jwt_or_session_required
def update_member_profile(id):
    """Update member profile."""
    try:
        member = Member.query.get_or_404(id)

        # Users can only update their own profile
        if member.id != current_user.id and not current_user.is_admin():
            return jsonify({'error': 'Sie haben keine Berechtigung für diese Aktion'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON body required'}), 400

        # Fields users can update on their own profile
        allowed_fields = ['firstname', 'lastname', 'email', 'phone', 'street', 'city', 'zip_code',
                          'notifications_enabled', 'notify_own_bookings', 'notify_other_bookings',
                          'notify_court_blocked', 'notify_booking_overridden']

        # Admin-only fields
        admin_fields = ['role', 'membership_type', 'fee_paid', 'is_active']

        updates = {}
        for field in allowed_fields:
            if field in data:
                updates[field] = data[field]

        # Include admin fields if user is admin
        if current_user.is_admin():
            for field in admin_fields:
                if field in data:
                    updates[field] = data[field]

        # Handle password separately
        if 'password' in data and data['password']:
            updates['password'] = data['password']

        member_result, error = MemberService.update_member(
            member_id=id,
            updates=updates,
            admin_id=current_user.id if current_user.is_admin() else None
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': 'Profil erfolgreich aktualisiert',
            'member': member_result.to_dict(include_admin_fields=current_user.is_admin())
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/members/', methods=['POST'])
@jwt_or_session_required
def create_member_by_admin():
    """Create a new member (admin only)."""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin-Berechtigung erforderlich'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    try:
        member, error = MemberService.create_member(
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role', 'member'),
            membership_type=data.get('membership_type', 'full'),
            street=data.get('street'),
            city=data.get('city'),
            zip_code=data.get('zip_code'),
            phone=data.get('phone'),
            admin_id=current_user.id,
            notifications_enabled=bool(data.get('notifications_enabled', True)),
            notify_own_bookings=bool(data.get('notify_own_bookings', True)),
            notify_other_bookings=bool(data.get('notify_other_bookings', True)),
            notify_court_blocked=bool(data.get('notify_court_blocked', True)),
            notify_booking_overridden=bool(data.get('notify_booking_overridden', True))
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': 'Mitglied erfolgreich erstellt',
            'member': member.to_dict(include_admin_fields=True)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/members/<id>', methods=['DELETE'])
@jwt_or_session_required
def delete_member_by_admin(id):
    """Delete a member (admin only)."""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin-Berechtigung erforderlich'}), 403

    force = request.args.get('force', 'false').lower() == 'true'

    try:
        success, error = MemberService.delete_member(
            member_id=id,
            admin_id=current_user.id,
            force=force
        )

        if not success:
            return jsonify({'error': error}), 400

        return jsonify({'message': 'Mitglied erfolgreich gelöscht'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/members/<id>/deactivate', methods=['POST'])
@jwt_or_session_required
def deactivate_member_by_admin(id):
    """Deactivate a member (admin only)."""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin-Berechtigung erforderlich'}), 403

    try:
        success, error = MemberService.deactivate_member(
            member_id=id,
            admin_id=current_user.id
        )

        if not success:
            return jsonify({'error': error}), 400

        return jsonify({'message': 'Mitglied erfolgreich deaktiviert'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/members/<id>/reactivate', methods=['POST'])
@jwt_or_session_required
def reactivate_member_by_admin(id):
    """Reactivate a member (admin only)."""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin-Berechtigung erforderlich'}), 403

    try:
        success, error = MemberService.reactivate_member(
            member_id=id,
            admin_id=current_user.id
        )

        if not success:
            return jsonify({'error': error}), 400

        return jsonify({'message': 'Mitglied erfolgreich reaktiviert'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
