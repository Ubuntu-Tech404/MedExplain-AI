from typing import Optional
import os
from supabase import create_client, Client
import logging

from config import settings

logger = logging.getLogger(__name__)

class Database:
    """Database connection manager"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.connected = False
        
    def connect(self) -> bool:
        """Connect to Supabase database"""
        try:
            if settings.supabase_url and settings.supabase_anon_key:
                self.supabase = create_client(
                    settings.supabase_url,
                    settings.supabase_anon_key
                )
                self.connected = True
                logger.info("Connected to Supabase database")
                return True
            else:
                logger.warning("Supabase credentials not configured, using local storage")
                self.connected = False
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        self.supabase = None
        self.connected = False
        logger.info("Disconnected from database")
    
    def get_connection(self) -> Optional[Client]:
        """Get database connection"""
        if not self.connected:
            self.connect()
        return self.supabase
    
    def health_check(self) -> dict:
        """Check database health"""
        if not self.connected:
            return {"status": "disconnected", "type": "local"}
        
        try:
            # Simple query to check connection
            response = self.supabase.table("health_check").select("count").limit(1).execute()
            return {"status": "connected", "type": "supabase", "response": response.data}
        except Exception as e:
            return {"status": "error", "type": "supabase", "error": str(e)}

# Global database instance
db = Database()