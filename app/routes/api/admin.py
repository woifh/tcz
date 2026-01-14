"""
API Admin Module

Admin routes for member management, blocks, and settings.
JWT-only authentication with admin/teamster role requirements.
"""

from datetime import datetime
from flask import request, jsonify
from flask_login import current_user

from app import db
from app.models import Member, Block, Court, BlockReason
from app.services.member_service import MemberService
from app.services.block_service import BlockService
from app.services.settings_service import SettingsService
from app.decorators.auth import jwt_admin_required, jwt_teamster_or_admin_required
from app.constants.messages import ErrorMessages, SuccessMessages
from . import bp


# ----- Member Management Routes (Admin Only) -----

@bp.route('/admin/members/', methods=['GET'])
@jwt_admin_required
def list_members():
    """List all active members."""
    members, error = MemberService.get_all_members(include_inactive=False)
    if error:
        return jsonify({'error': error}), 500

    return jsonify({
        'members': [m.to_dict(include_admin_fields=True) for m in members]
    })


@bp.route('/admin/members/', methods=['POST'])
@jwt_admin_required
def create_member():
    """Create a new member."""
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
            admin_id=current_user.id
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': SuccessMessages.MEMBER_CREATED,
            'member': member.to_dict(include_admin_fields=True)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/members/<id>', methods=['GET'])
@jwt_admin_required
def get_member(id):
    """Get member details."""
    member, error = MemberService.get_member(id)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(member.to_dict(include_admin_fields=True))


@bp.route('/admin/members/<id>', methods=['PUT'])
@jwt_admin_required
def update_member(id):
    """Update a member."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    try:
        updates = {}
        allowed_fields = [
            'firstname', 'lastname', 'email', 'password', 'role',
            'membership_type', 'fee_paid', 'street', 'city', 'zip_code', 'phone',
            'notifications_enabled', 'notify_own_bookings', 'notify_other_bookings',
            'notify_court_blocked', 'notify_booking_overridden'
        ]

        for field in allowed_fields:
            if field in data:
                value = data[field]
                if field == 'fee_paid':
                    if isinstance(value, str):
                        updates[field] = value.lower() in ('true', '1', 'yes')
                    else:
                        updates[field] = bool(value)
                elif field.startswith('notif'):
                    updates[field] = bool(value)
                elif field == 'password' and value:
                    updates[field] = value
                elif field != 'password':
                    updates[field] = value

        member, error = MemberService.update_member(
            member_id=id,
            updates=updates,
            admin_id=current_user.id
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': SuccessMessages.MEMBER_UPDATED,
            'member': member.to_dict(include_admin_fields=True)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/members/<id>', methods=['DELETE'])
@jwt_admin_required
def delete_member(id):
    """Delete a member."""
    force = request.args.get('force', 'false').lower() == 'true'

    try:
        success, error = MemberService.delete_member(
            member_id=id,
            admin_id=current_user.id,
            force=force
        )

        if not success:
            return jsonify({'error': error}), 400

        return jsonify({'message': SuccessMessages.MEMBER_DELETED})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/members/<id>/deactivate', methods=['POST'])
@jwt_admin_required
def deactivate_member(id):
    """Deactivate a member account."""
    try:
        success, error = MemberService.deactivate_member(
            member_id=id,
            admin_id=current_user.id
        )

        if not success:
            return jsonify({'error': error}), 400

        return jsonify({'message': SuccessMessages.MEMBER_DEACTIVATED})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/members/<id>/reactivate', methods=['POST'])
@jwt_admin_required
def reactivate_member(id):
    """Reactivate a member account."""
    try:
        success, error = MemberService.reactivate_member(
            member_id=id,
            admin_id=current_user.id
        )

        if not success:
            return jsonify({'error': error}), 400

        return jsonify({'message': SuccessMessages.MEMBER_REACTIVATED})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----- Block Management Routes (Teamster or Admin) -----

@bp.route('/admin/blocks/', methods=['GET'])
@jwt_teamster_or_admin_required
def get_blocks():
    """Get blocks with optional filtering."""
    try:
        date_range_start = request.args.get('date_range_start')
        date_range_end = request.args.get('date_range_end')
        court_ids = request.args.getlist('court_ids', type=int)
        reason_ids = request.args.getlist('reason_ids', type=int)

        query = Block.query

        if date_range_start:
            start_date = datetime.strptime(date_range_start, '%Y-%m-%d').date()
            query = query.filter(Block.date >= start_date)

        if date_range_end:
            end_date = datetime.strptime(date_range_end, '%Y-%m-%d').date()
            query = query.filter(Block.date <= end_date)

        if court_ids:
            query = query.filter(Block.court_id.in_(court_ids))

        if reason_ids:
            query = query.filter(Block.reason_id.in_(reason_ids))

        blocks = query.order_by(Block.date.asc(), Block.start_time.asc()).all()

        return jsonify({
            'blocks': [b.to_dict() for b in blocks]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/blocks/', methods=['POST'])
@jwt_teamster_or_admin_required
def create_blocks():
    """Create block(s) for one or multiple courts."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    try:
        # Get court_ids
        court_ids = data.get('court_ids', [])
        if isinstance(court_ids, str):
            court_ids = [int(x) for x in court_ids.split(',')]
        elif not court_ids and 'court_id' in data:
            court_ids = [int(data['court_id'])]

        if not court_ids:
            return jsonify({'error': 'court_ids erforderlich'}), 400

        court_ids = [int(x) for x in court_ids]
        date_str = data['date']
        start_time_str = data['start_time']
        end_time_str = data['end_time']
        reason_id = int(data['reason_id'])
        details = data.get('details', '').strip() or None

        # Validate teamsters can only use teamster-usable reasons
        if current_user.is_teamster() and not current_user.is_admin():
            reason = BlockReason.query.get(reason_id)
            if not reason:
                return jsonify({'error': 'Ungültiger Sperrungsgrund'}), 400
            if not reason.teamster_usable:
                return jsonify({'error': 'Sie haben keine Berechtigung, diesen Sperrungsgrund zu verwenden'}), 403

        block_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        from app.utils.timezone_utils import get_berlin_date_today
        today = get_berlin_date_today()
        if block_date < today:
            return jsonify({'error': 'Sperrungen können nicht für vergangene Tage erstellt werden'}), 400

        blocks, error = BlockService.create_multi_court_blocks(
            court_ids=court_ids,
            date=block_date,
            start_time=start_time,
            end_time=end_time,
            reason_id=reason_id,
            details=details,
            admin_id=current_user.id
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': f'{len(blocks)} Sperrung{"en" if len(blocks) > 1 else ""} erfolgreich erstellt',
            'block_count': len(blocks),
            'batch_id': blocks[0].batch_id if blocks else None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/blocks/<batch_id>', methods=['GET'])
@jwt_teamster_or_admin_required
def get_batch(batch_id):
    """Get all blocks in a batch."""
    try:
        blocks = Block.query.filter_by(batch_id=batch_id).all()

        if not blocks:
            return jsonify({'error': 'Batch nicht gefunden'}), 404

        first_block = blocks[0]
        reason = BlockReason.query.get(first_block.reason_id)

        return jsonify({
            'batch_id': batch_id,
            'date': first_block.date.isoformat(),
            'start_time': first_block.start_time.strftime('%H:%M'),
            'end_time': first_block.end_time.strftime('%H:%M'),
            'reason_id': first_block.reason_id,
            'reason_name': reason.name if reason else 'Unbekannt',
            'details': first_block.details,
            'court_ids': [b.court_id for b in blocks],
            'blocks': [b.to_dict() for b in blocks]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/blocks/<batch_id>', methods=['PUT'])
@jwt_teamster_or_admin_required
def update_batch(batch_id):
    """Update all blocks in a batch."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    try:
        new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        new_start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        new_end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        new_reason_id = int(data['reason_id'])
        new_details = data.get('details', '').strip() or None

        new_court_ids = data.get('court_ids', [])
        if isinstance(new_court_ids, str):
            new_court_ids = [int(x) for x in new_court_ids.split(',')]
        else:
            new_court_ids = [int(x) for x in new_court_ids]

        from app.utils.timezone_utils import get_berlin_date_today
        today = get_berlin_date_today()
        if new_date < today:
            return jsonify({'error': 'Sperrungen können nicht für vergangene Tage bearbeitet werden'}), 400

        if new_start_time >= new_end_time:
            return jsonify({'error': 'Endzeit muss nach Startzeit liegen'}), 400

        existing_blocks = Block.query.filter_by(batch_id=batch_id).all()
        if not existing_blocks:
            return jsonify({'error': 'Batch nicht gefunden'}), 404

        # Teamsters can only update their own batches
        if current_user.is_teamster() and not current_user.is_admin():
            if not all(block.created_by_id == current_user.id for block in existing_blocks):
                return jsonify({'error': 'Sie können nur Ihre eigenen Sperrungen bearbeiten'}), 403

        existing_court_ids = [block.court_id for block in existing_blocks]
        courts_to_keep = set(existing_court_ids) & set(new_court_ids)
        courts_to_delete = set(existing_court_ids) - set(new_court_ids)
        courts_to_add = set(new_court_ids) - set(existing_court_ids)

        # Delete blocks for removed courts
        for block in existing_blocks:
            if block.court_id in courts_to_delete:
                db.session.delete(block)

        # Update existing blocks
        for block in existing_blocks:
            if block.court_id in courts_to_keep:
                success, error = BlockService.update_single_instance(
                    block_id=block.id,
                    date=new_date,
                    start_time=new_start_time,
                    end_time=new_end_time,
                    reason_id=new_reason_id,
                    details=new_details,
                    admin_id=current_user.id
                )
                if error:
                    db.session.rollback()
                    return jsonify({'error': f'Fehler beim Aktualisieren: {error}'}), 400

        # Create new blocks for added courts
        for court_id in courts_to_add:
            new_block = Block(
                court_id=court_id,
                date=new_date,
                start_time=new_start_time,
                end_time=new_end_time,
                reason_id=new_reason_id,
                details=new_details,
                created_by_id=current_user.id,
                batch_id=batch_id
            )
            db.session.add(new_block)
            db.session.flush()
            BlockService.cancel_conflicting_reservations(new_block)

        db.session.commit()

        total_blocks = len(courts_to_keep) + len(courts_to_add)
        return jsonify({'message': f'{total_blocks} Sperrungen erfolgreich aktualisiert'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/blocks/<batch_id>', methods=['DELETE'])
@jwt_teamster_or_admin_required
def delete_batch(batch_id):
    """Delete all blocks in a batch."""
    try:
        blocks = Block.query.filter_by(batch_id=batch_id).all()

        if not blocks:
            return jsonify({'error': 'Batch nicht gefunden'}), 404

        # Teamsters can only delete their own batches
        if current_user.is_teamster() and not current_user.is_admin():
            if not all(block.created_by_id == current_user.id for block in blocks):
                return jsonify({'error': 'Sie können nur Ihre eigenen Sperrungen löschen'}), 403

        success, error = BlockService.delete_batch(batch_id, current_user.id)

        if success:
            return jsonify({'message': 'Batch erfolgreich gelöscht'})
        return jsonify({'error': error}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----- Settings Routes (Admin Only) -----

@bp.route('/admin/settings/payment-deadline', methods=['GET'])
@jwt_admin_required
def get_payment_deadline():
    """Get current payment deadline settings."""
    deadline = SettingsService.get_payment_deadline()
    days_until = SettingsService.days_until_deadline()
    unpaid_count = SettingsService.get_unpaid_member_count()

    return jsonify({
        'deadline': deadline.isoformat() if deadline else None,
        'days_until': days_until,
        'unpaid_count': unpaid_count,
        'is_past': SettingsService.is_past_payment_deadline()
    })


@bp.route('/admin/settings/payment-deadline', methods=['POST'])
@jwt_admin_required
def set_payment_deadline():
    """Set payment deadline."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    deadline_str = data.get('deadline')

    if not deadline_str:
        success, error = SettingsService.clear_payment_deadline(current_user.id)
        if success:
            return jsonify({'message': SuccessMessages.PAYMENT_DEADLINE_CLEARED})
        return jsonify({'error': error}), 400

    try:
        deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': ErrorMessages.PAYMENT_DEADLINE_INVALID_DATE}), 400

    success, error = SettingsService.set_payment_deadline(deadline_date, current_user.id)

    if success:
        return jsonify({
            'message': SuccessMessages.PAYMENT_DEADLINE_SET,
            'deadline': deadline_date.isoformat()
        })
    return jsonify({'error': error}), 400


@bp.route('/admin/settings/payment-deadline', methods=['DELETE'])
@jwt_admin_required
def clear_payment_deadline():
    """Clear payment deadline."""
    success, error = SettingsService.clear_payment_deadline(current_user.id)

    if success:
        return jsonify({'message': SuccessMessages.PAYMENT_DEADLINE_CLEARED})
    return jsonify({'error': error}), 400
