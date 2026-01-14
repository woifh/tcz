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
