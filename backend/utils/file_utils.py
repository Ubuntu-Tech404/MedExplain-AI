import os
import shutil
from typing import Optional, Tuple, List, Dict
import magic
from pathlib import Path
import hashlib
import mimetypes
from datetime import datetime

from config import settings

class FileUtils:
    """Utility functions for file operations"""
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension in lowercase"""
        return Path(filename).suffix.lower()
    
    @staticmethod
    def get_filename_without_extension(filename: str) -> str:
        """Get filename without extension"""
        return Path(filename).stem
    
    @staticmethod
    def is_allowed_file(filename: str, allowed_extensions: Optional[List[str]] = None) -> bool:
        """Check if file extension is allowed"""
        if allowed_extensions is None:
            allowed_extensions = settings.allowed_extensions
        
        extension = FileUtils.get_file_extension(filename)
        return extension in allowed_extensions
    
    @staticmethod
    def get_file_size_mb(filepath: str) -> float:
        """Get file size in megabytes"""
        return os.path.getsize(filepath) / (1024 * 1024)
    
    @staticmethod
    def get_file_size_kb(filepath: str) -> float:
        """Get file size in kilobytes"""
        return os.path.getsize(filepath) / 1024
    
    @staticmethod
    def get_mime_type(filepath: str) -> Optional[str]:
        """Get MIME type of file"""
        try:
            # Try python-magic first
            mime = magic.Magic(mime=True)
            return mime.from_file(filepath)
        except:
            try:
                # Fallback to mimetypes
                mime_type, _ = mimetypes.guess_type(filepath)
                return mime_type
            except:
                return None
    
    @staticmethod
    def is_file_type(filepath: str, mime_type: str) -> bool:
        """Check if file matches specific MIME type"""
        file_mime = FileUtils.get_mime_type(filepath)
        return file_mime == mime_type if file_mime else False
    
    @staticmethod
    def create_directory(path: str) -> bool:
        """Create directory if it doesn't exist"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            return False
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """Convert filename to safe version"""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        safe_name = filename
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Replace spaces with underscores
        safe_name = safe_name.replace(' ', '_')
        
        # Limit length
        max_length = 255  # Filesystem limit
        if len(safe_name) > max_length:
            name, ext = os.path.splitext(safe_name)
            safe_name = name[:max_length - len(ext)] + ext
        
        return safe_name
    
    @staticmethod
    def get_unique_filename(directory: str, filename: str) -> str:
        """Get unique filename in directory"""
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
        
        return new_filename
    
    @staticmethod
    def get_file_info(filepath: str) -> Optional[Dict]:
        """Get comprehensive file information"""
        try:
            stat = os.stat(filepath)
            
            return {
                "path": filepath,
                "filename": os.path.basename(filepath),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "size_kb": round(stat.st_size / 1024, 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "extension": FileUtils.get_file_extension(filepath),
                "mime_type": FileUtils.get_mime_type(filepath),
                "is_file": os.path.isfile(filepath),
                "is_dir": os.path.isdir(filepath),
                "exists": os.path.exists(filepath)
            }
        except Exception as e:
            print(f"Error getting file info for {filepath}: {e}")
            return None
    
    @staticmethod
    def validate_upload_file(filepath: str, max_size_mb: Optional[float] = None) -> Tuple[bool, str]:
        """Validate uploaded file"""
        try:
            if max_size_mb is None:
                max_size_mb = settings.max_upload_size_mb
            
            # Check if file exists
            if not os.path.exists(filepath):
                return False, "File does not exist"
            
            # Check file size
            file_size_mb = FileUtils.get_file_size_mb(filepath)
            if file_size_mb > max_size_mb:
                return False, f"File size ({file_size_mb:.2f} MB) exceeds maximum ({max_size_mb} MB)"
            
            # Check if file is readable
            with open(filepath, 'rb') as f:
                f.read(1)
            
            # Check MIME type if possible
            mime_type = FileUtils.get_mime_type(filepath)
            if mime_type:
                # Basic security check - reject executable files
                executable_mimes = [
                    'application/x-executable',
                    'application/x-sharedlib',
                    'application/x-shellscript'
                ]
                if any(mime in mime_type for mime in executable_mimes):
                    return False, "Executable files are not allowed"
            
            return True, "File is valid"
            
        except PermissionError:
            return False, "Permission denied"
        except Exception as e:
            return False, f"File validation error: {str(e)}"
    
    @staticmethod
    def calculate_file_hash(filepath: str, algorithm: str = "sha256") -> Optional[str]:
        """Calculate file hash for integrity checking"""
        try:
            hash_func = hashlib.new(algorithm)
            
            with open(filepath, 'rb') as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {filepath}: {e}")
            return None
    
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying file from {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """Move file from source to destination"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Error moving file from {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Delete file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
            return False
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """List files in directory matching pattern"""
        try:
            return [str(f) for f in Path(directory).glob(pattern) if f.is_file()]
        except Exception as e:
            print(f"Error listing files in {directory}: {e}")
            return []
    
    @staticmethod
    def ensure_upload_directory() -> str:
        """Ensure upload directory exists and return its path"""
        upload_dir = settings.upload_dir
        FileUtils.create_directory(upload_dir)
        return upload_dir
    
    @staticmethod
    def generate_upload_path(filename: str, patient_id: str = "unknown") -> str:
        """Generate upload path for a file"""
        upload_dir = FileUtils.ensure_upload_directory()
        
        # Create patient-specific subdirectory
        patient_dir = os.path.join(upload_dir, patient_id)
        FileUtils.create_directory(patient_dir)
        
        # Generate unique filename
        safe_name = FileUtils.safe_filename(filename)
        unique_name = FileUtils.get_unique_filename(patient_dir, safe_name)
        
        return os.path.join(patient_dir, unique_name)