"""
Admin Series Module

Contains recurring block series management routes.
"""

from datetime import datetime, date
from flask import request, jsonify
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required
from app.models import BlockSeries
from app.services.block_service import BlockService
from . import bp


@bp.route('/blocks/series', methods=['GET'])
@login_required
@admin_required
def list_recurring_series():
    """List all recurring block series (admin only)."""
    try:
        series = BlockSeries.query.all()
        
        return jsonify({
            'series': [
                {
                    'id': serie.id,
                    'name': serie.name,
                    'start_date': serie.start_date.isoformat(),
                    'end_date': serie.end_date.isoformat(),
                    'start_time': serie.start_time.strftime('%H:%M'),
                    'end_time': serie.end_time.strftime('%H:%M'),
                    'recurrence_pattern': serie.recurrence_pattern,
                    'recurrence_days': serie.recurrence_days,
                    'reason_id': serie.reason_id,
                    'reason_name': serie.reason_obj.name if serie.reason_obj else 'Unknown',
                    'sub_reason': serie.sub_reason,
                    'court_selection': [1, 2, 3, 4, 5, 6],  # This would come from blocks
                    'total_instances': len(serie.blocks),
                    'active_instances': len([b for b in serie.blocks if b.date >= date.today()]),
                    'is_active': len([b for b in serie.blocks if b.date >= date.today()]) > 0,
                    'created_by': serie.created_by.name,
                    'created_at': serie.created_at.isoformat()
                }
                for serie in series
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/blocks/series', methods=['POST'])
@login_required
@admin_required
def create_recurring_series():
    """Create recurring block series (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        court_ids = data.get('court_ids', [])
        if isinstance(court_ids, str):
            court_ids = [int(x) for x in court_ids.split(',')]
        elif isinstance(court_ids, list):
            court_ids = [int(x) for x in court_ids]
        
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        recurrence_pattern = data.get('recurrence_pattern')
        recurrence_days = data.get('recurrence_days', [])
        reason_id = int(data.get('reason_id'))
        sub_reason = data.get('sub_reason', '').strip() or None
        series_name = data.get('series_name', '').strip()
        
        # Validate required fields
        if not all([court_ids, start_date_str, end_date_str, start_time_str, end_time_str, recurrence_pattern, reason_id, series_name]):
            return jsonify({'error': 'Alle Pflichtfelder sind erforderlich'}), 400
        
        # Parse dates and times
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        
        # Create recurring series
        blocks, error = BlockService.create_recurring_block_series(
            court_ids=court_ids,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            recurrence_pattern=recurrence_pattern,
            recurrence_days=recurrence_days,
            reason_id=reason_id,
            sub_reason=sub_reason,
            admin_id=current_user.id,
            series_name=series_name
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': f'Wiederkehrende Serie erfolgreich erstellt: {len(blocks)} Sperrungen',
            'series_name': series_name,
            'blocks_created': len(blocks)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/blocks/series/<int:series_id>', methods=['PUT'])
@login_required
@admin_required
def update_entire_series(series_id):
    """Update entire recurring series (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        updates = {}
        if 'start_time' in data:
            updates['start_time'] = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            updates['end_time'] = datetime.strptime(data['end_time'], '%H:%M').time()
        if 'reason_id' in data:
            updates['reason_id'] = int(data['reason_id'])
        if 'sub_reason' in data:
            updates['sub_reason'] = data['sub_reason'].strip() or None
        
        updates['admin_id'] = current_user.id
        
        success, error = BlockService.update_entire_series(series_id, **updates)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Gesamte Serie erfolgreich aktualisiert'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/blocks/series/<int:series_id>/future', methods=['PUT'])
@login_required
@admin_required
def update_future_series(series_id):
    """Update future instances of recurring series (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        from_date_str = data.get('from_date')
        if not from_date_str:
            return jsonify({'error': 'from_date ist erforderlich'}), 400
        
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        
        updates = {}
        if 'start_time' in data:
            updates['start_time'] = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            updates['end_time'] = datetime.strptime(data['end_time'], '%H:%M').time()
        if 'reason_id' in data:
            updates['reason_id'] = int(data['reason_id'])
        if 'sub_reason' in data:
            updates['sub_reason'] = data['sub_reason'].strip() or None
        
        updates['admin_id'] = current_user.id
        
        success, error = BlockService.update_future_series(series_id, from_date, **updates)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Zukünftige Instanzen erfolgreich aktualisiert'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/blocks/series/<int:series_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_series(series_id):
    """Delete recurring series with options (admin only)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        option = data.get('option', 'all')  # 'single', 'future', or 'all'
        from_date = None
        
        if option in ['single', 'future']:
            from_date_str = data.get('from_date')
            if not from_date_str:
                return jsonify({'error': 'from_date ist für diese Option erforderlich'}), 400
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        
        success, error = BlockService.delete_series_options(series_id, option, from_date)
        
        if error:
            return jsonify({'error': error}), 400
        
        messages = {
            'single': 'Einzelne Instanz erfolgreich gelöscht',
            'future': 'Zukünftige Instanzen erfolgreich gelöscht',
            'all': 'Gesamte Serie erfolgreich gelöscht'
        }
        
        return jsonify({'message': messages.get(option, 'Serie erfolgreich gelöscht')}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500