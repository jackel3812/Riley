"""
Notes Service - Handles note-taking functionality.
"""

import os
import logging
import json
from datetime import datetime
from pathlib import Path

class NotesService:
    """Handles note taking and retrieval."""
    
    def __init__(self):
        """Initialize the Notes Service."""
        self.logger = logging.getLogger(__name__)
        
        # Directory for storing notes
        self.notes_dir = Path.home() / '.jarvis' / 'notes'
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        # File for storing notes
        self.notes_file = self.notes_dir / 'notes.json'
        
        # Load existing notes
        self.notes = self._load_notes()
        
        self.logger.info("Notes Service initialized")
    
    def _load_notes(self):
        """Load notes from the file.
        
        Returns:
            List of note dictionaries
        """
        if not self.notes_file.exists():
            return []
        
        try:
            with open(self.notes_file, 'r') as f:
                notes = json.load(f)
            
            self.logger.debug(f"Loaded {len(notes)} notes")
            return notes
        except Exception as e:
            self.logger.error(f"Error loading notes: {e}")
            return []
    
    def _save_notes(self):
        """Save notes to the file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.notes_file, 'w') as f:
                json.dump(self.notes, f, indent=2)
            
            self.logger.debug(f"Saved {len(self.notes)} notes")
            return True
        except Exception as e:
            self.logger.error(f"Error saving notes: {e}")
            return False
    
    def add_note(self, content, title=None, tags=None):
        """Add a new note.
        
        Args:
            content: Content of the note
            title: Optional title for the note
            tags: Optional list of tags
            
        Returns:
            ID of the new note if successful, None otherwise
        """
        if not content:
            self.logger.warning("Attempted to add note with empty content")
            return None
        
        # Generate a unique ID
        note_id = str(len(self.notes) + 1)
        
        # Create note object
        note = {
            'id': note_id,
            'title': title or f"Note {note_id}",
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add to notes list
        self.notes.append(note)
        
        # Save notes
        if self._save_notes():
            self.logger.info(f"Added note {note_id}")
            return note_id
        else:
            # Remove the note if saving failed
            self.notes.pop()
            self.logger.error(f"Failed to add note")
            return None
    
    def get_note(self, note_id):
        """Get a note by ID.
        
        Args:
            note_id: ID of the note to get
            
        Returns:
            Note dictionary or None if not found
        """
        for note in self.notes:
            if note['id'] == note_id:
                return note
        
        self.logger.warning(f"Note {note_id} not found")
        return None
    
    def update_note(self, note_id, content=None, title=None, tags=None):
        """Update an existing note.
        
        Args:
            note_id: ID of the note to update
            content: New content for the note (or None to keep existing)
            title: New title for the note (or None to keep existing)
            tags: New tags for the note (or None to keep existing)
            
        Returns:
            True if successful, False otherwise
        """
        note = self.get_note(note_id)
        if not note:
            return False
        
        # Update fields if provided
        if content is not None:
            note['content'] = content
        if title is not None:
            note['title'] = title
        if tags is not None:
            note['tags'] = tags
        
        note['updated_at'] = datetime.now().isoformat()
        
        # Save notes
        if self._save_notes():
            self.logger.info(f"Updated note {note_id}")
            return True
        else:
            self.logger.error(f"Failed to update note {note_id}")
            return False
    
    def delete_note(self, note_id):
        """Delete a note by ID.
        
        Args:
            note_id: ID of the note to delete
            
        Returns:
            True if successful, False otherwise
        """
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                self.notes.pop(i)
                
                # Save notes
                if self._save_notes():
                    self.logger.info(f"Deleted note {note_id}")
                    return True
                else:
                    self.logger.error(f"Failed to delete note {note_id}")
                    return False
        
        self.logger.warning(f"Note {note_id} not found for deletion")
        return False
    
    def search_notes(self, query):
        """Search for notes by keyword.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching note dictionaries
        """
        if not query:
            return []
        
        query = query.lower()
        results = []
        
        for note in self.notes:
            # Search in title and content
            if (query in note['title'].lower() or
                query in note['content'].lower() or
                any(query in tag.lower() for tag in note['tags'])):
                results.append(note)
        
        self.logger.debug(f"Found {len(results)} notes matching '{query}'")
        return results
    
    def get_all_notes(self):
        """Get all notes.
        
        Returns:
            List of all note dictionaries
        """
        return self.notes
    
    def get_recent_notes(self, limit=5):
        """Get recent notes.
        
        Args:
            limit: Maximum number of notes to return
            
        Returns:
            List of recent note dictionaries
        """
        # Sort notes by creation time (newest first)
        sorted_notes = sorted(self.notes, 
                             key=lambda note: note['created_at'], 
                             reverse=True)
        
        return sorted_notes[:limit]
    
    def get_notes_by_tag(self, tag):
        """Get notes with a specific tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of matching note dictionaries
        """
        return [note for note in self.notes if tag in note['tags']]
    
    def get_formatted_note(self, note_id):
        """Get a formatted string for a note.
        
        Args:
            note_id: ID of the note to format
            
        Returns:
            Formatted string with note details
        """
        note = self.get_note(note_id)
        if not note:
            return f"Note {note_id} not found."
        
        # Format creation time
        created_at = "Unknown time"
        try:
            created_at = datetime.fromisoformat(note['created_at']).strftime('%B %d, %Y at %I:%M %p')
        except:
            pass
        
        result = f"Note: {note['title']}\n"
        result += f"Created: {created_at}\n"
        
        if note['tags']:
            result += f"Tags: {', '.join(note['tags'])}\n"
        
        result += f"\n{note['content']}\n"
        
        return result
    
    def get_formatted_notes(self, notes=None, limit=5):
        """Get a formatted string with notes.
        
        Args:
            notes: List of notes to format (or None for recent notes)
            limit: Maximum number of notes to include
            
        Returns:
            Formatted string with notes
        """
        if notes is None:
            notes = self.get_recent_notes(limit)
        else:
            notes = notes[:limit]
        
        if not notes:
            return "No notes found."
        
        result = f"Notes ({len(notes)}):\n\n"
        
        for note in notes:
            # Format creation time
            created_at = "Unknown time"
            try:
                created_at = datetime.fromisoformat(note['created_at']).strftime('%B %d, %Y')
            except:
                pass
            
            result += f"{note['id']}: {note['title']} ({created_at})\n"
            
            # Show a preview of the content
            content = note['content']
            if len(content) > 50:
                content = content[:50] + "..."
            result += f"  {content}\n\n"
        
        return result
