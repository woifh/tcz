"""Member service for business logic."""
from sqlalchemy import or_, func
from app import db
from app.models import Member, favourites


class MemberService:
    """Service for managing members."""
    
    @staticmethod
    def search_members(query, current_member_id):
        """
        Search for members by name or email, excluding current member and existing favourites.
        
        Args:
            query: Search string (case-insensitive)
            current_member_id: ID of the member performing the search
            
        Returns:
            list: List of Member objects matching the search criteria
        """
        if not query or not query.strip():
            return []
        
        # Get IDs of current member's favourites
        favourite_ids_subquery = db.session.query(favourites.c.favourite_id).filter(
            favourites.c.member_id == current_member_id
        ).subquery()
        
        # Build the search query
        search_pattern = f"%{query.strip()}%"
        
        results = db.session.query(Member).filter(
            # Search in name or email (case-insensitive)
            or_(
                func.lower(Member.name).like(func.lower(search_pattern)),
                func.lower(Member.email).like(func.lower(search_pattern))
            ),
            # Exclude current member
            Member.id != current_member_id,
            # Exclude existing favourites
            ~Member.id.in_(favourite_ids_subquery)
        ).order_by(
            # Order alphabetically by name
            Member.name
        ).limit(50).all()  # Limit to 50 members
        
        return results