"""Service for loading and rendering help center documentation."""

import os
import re
import markdown
from flask import current_app


class HelpService:
    """Service for loading and rendering help documentation from markdown files."""

    def __init__(self):
        self.help_dir = os.path.join(current_app.root_path, '..', 'docs', 'help')
        self.md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])

    def _transform_links(self, html, current_path):
        """Transform relative .md links to proper help center URLs.

        Args:
            html: The rendered HTML content
            current_path: The current article path (for resolving relative links)

        Returns:
            HTML with transformed links
        """
        def replace_link(match):
            href = match.group(1)
            # Only transform relative .md links (not external URLs)
            if href.endswith('.md') and not href.startswith(('http://', 'https://', '/')):
                # Handle relative paths like ../buchungen/platz-buchen.md
                if current_path:
                    # Get the directory of the current article
                    current_dir = os.path.dirname(current_path)
                    # Resolve the relative path
                    resolved = os.path.normpath(os.path.join(current_dir, href))
                else:
                    resolved = href
                # Remove .md extension
                resolved = resolved[:-3] if resolved.endswith('.md') else resolved
                # Build URL path directly
                return f'href="/members/help/{resolved}"'
            return match.group(0)

        return re.sub(r'href="([^"]+)"', replace_link, html)

    def get_article(self, path):
        """Load and render a markdown article.

        Args:
            path: The article path relative to help_dir (without .md extension)

        Returns:
            HTML string of rendered markdown, or None if not found
        """
        file_path = os.path.join(self.help_dir, f"{path}.md")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.md.reset()
            html = self.md.convert(content)
            # Transform relative .md links to proper URLs
            return self._transform_links(html, path)
        return None

    def get_article_title(self, path):
        """Extract the title from a markdown article (first H1).

        Args:
            path: The article path relative to help_dir (without .md extension)

        Returns:
            The title string, or a formatted version of the path
        """
        file_path = os.path.join(self.help_dir, f"{path}.md")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('# '):
                        return line[2:].strip()
        # Fallback: format path as title
        return path.split('/')[-1].replace('-', ' ').title()

    def get_navigation(self):
        """Return the navigation structure for the help center.

        Returns:
            Dictionary with 'main' items and 'sections' with nested items
        """
        return {
            'main': [
                {'title': 'Schnellstart', 'path': 'quick_start_guide', 'icon': 'rocket_launch'},
                {'title': 'FAQ', 'path': 'faq', 'icon': 'quiz'},
                {'title': 'Glossar', 'path': 'glossar', 'icon': 'menu_book'},
            ],
            'sections': [
                {
                    'title': 'Buchungen',
                    'icon': 'event',
                    'links': [
                        {'title': 'Platz buchen', 'path': 'buchungen/platz-buchen'},
                        {'title': 'Buchungslimits', 'path': 'buchungen/buchungslimits'},
                        {'title': 'Kurzfristige Buchungen', 'path': 'buchungen/kurzfristige-buchungen'},
                        {'title': 'Stornierung', 'path': 'buchungen/stornierung'},
                        {'title': 'Für andere buchen', 'path': 'buchungen/buchung-fuer-andere'},
                        {'title': 'Meine Buchungen', 'path': 'buchungen/meine-buchungen'},
                    ]
                },
                {
                    'title': 'Profil',
                    'icon': 'person',
                    'links': [
                        {'title': 'Profil bearbeiten', 'path': 'profil/profil-bearbeiten'},
                        {'title': 'Profilbild', 'path': 'profil/profilbild'},
                        {'title': 'E-Mail-Bestätigung', 'path': 'profil/email-bestaetigung'},
                        {'title': 'Benachrichtigungen', 'path': 'profil/benachrichtigungen'},
                    ]
                },
                {
                    'title': 'Favoriten',
                    'icon': 'star',
                    'links': [
                        {'title': 'Favoriten verwalten', 'path': 'favoriten/favoriten-verwalten'},
                    ]
                },
                {
                    'title': 'Mitgliedschaft',
                    'icon': 'card_membership',
                    'links': [
                        {'title': 'Mitgliedsbeitrag', 'path': 'mitgliedschaft/beitrag'},
                        {'title': 'Zahlung bestätigen', 'path': 'mitgliedschaft/zahlung-bestaetigen'},
                    ]
                },
                {
                    'title': 'Statistiken',
                    'icon': 'bar_chart',
                    'links': [
                        {'title': 'Meine Statistiken', 'path': 'statistiken/meine-statistiken'},
                    ]
                },
                {
                    'title': 'Fehlerbehebung',
                    'icon': 'build',
                    'links': [
                        {'title': 'Buchung nicht möglich', 'path': 'fehlerbehebung/buchung-nicht-moeglich'},
                        {'title': 'Zugangsprobleme', 'path': 'fehlerbehebung/zugangsprobleme'},
                    ]
                },
            ]
        }
