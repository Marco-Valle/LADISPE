from __future__ import annotations
from backend.settings import MEDIA_ROOT, MEDIA_URL, FILEBROWSER_DIRECTORY, MAX_DEPTH_IN_MATERIAL_SEARCH
from common.utils import safe_path
from pathlib import Path
from datetime import datetime
from os import sep
from re import sub
from urllib.parse import quote
from typing import List, Dict, Union, Optional, Callable

from ladicourses.models import LADICourse
from ladiusers.models import LADIUser


# If a course is not marked as public, just the professor and his assistants can request it.
restricted_course : Callable[[LADICourse, LADIUser], bool] = \
    lambda course, user: not(user.is_superuser or course.public or user in {course.professor, course.first_assistant, course.second_assistant})


class materialFile:
    """File of a LADICourse's material."""
    
    name            :   str
    url             :   str
    path            :   Path
    size            :   float
    date            :   datetime
    
    
    def __init__(self, path : Union[str, Path]) -> None:
        """Initializer of the materialFile class."""
        self.path = Path(path)
        self.name = self.path.name
        self.size = self.path.stat().st_size * 9.54e-7
        self.date = datetime.fromtimestamp(self.path.stat().st_mtime).date()
        url = sub(rf'^.*?{FILEBROWSER_DIRECTORY}', '', str(path).replace(sep, '/'))
        self.url = str(quote("{}{}{}".format(MEDIA_URL, FILEBROWSER_DIRECTORY, url))).replace('%2F', '/', 1)
        
        
    @property
    def valid(self) -> bool:
        "Check if it is a valid file."
        return self.path.is_file()
    
    
    def export(self) -> Optional[Dict[str, str]]:
        """Export the file into a dictionary."""
        return {
            'name'  :   self.name,
            'url'   :   self.url,
            'size'  :   f'{self.size:.3f}',
            'date'  :   self.date.strftime('%d-%m-%Y')
        } if self.valid else None
    

class materialDirectory:
    """Material directory class of a LADICourse."""
    
    title           :   str
    path            :   Path
    breadcrumbs     :   List[str]
    files           :   List[materialFile]
    dirs            :   List[materialDirectory]
    
    
    def __init__(self, path : Union[str, Path]) -> None:
        """Initializer of the materialDirectory class."""
        self.path = Path(path)
        self.title = self.path.name
        breadcrumb_path = sub(rf'^.*?{FILEBROWSER_DIRECTORY}', '', str(path).replace(sep, '/'))
        self.breadcrumbs = [folder for folder in breadcrumb_path.split(sep)][3:]
        self.files = []
        self.dirs = []
        max_depth_reached = len(self.breadcrumbs) >= MAX_DEPTH_IN_MATERIAL_SEARCH
        for child in self.path.iterdir():
            if child.is_file():
                self.files.append(materialFile(child))
            elif child.is_dir() and not max_depth_reached:
                self.dirs.append(materialDirectory(child))
        
        
    @property
    def valid(self) -> bool:
        """Check if it is a valid directory."""
        return self.path.is_dir()
    


class courseDirectory(materialDirectory):
    """Root folder for a a LADICourse."""
    
    professor_id        :   int
    course_title        :   str
    _iter_queue         :   List[materialDirectory]
    
    
    def __init__(self, course_title, professor_id) -> None:
        """Initializer of the courseDirectory class."""
        self.professor_id = professor_id
        self.course_title = course_title
        self._iter_queue = []
        path = safe_path(trusted_part=(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users'),
                         untrusted_part=(str(professor_id), course_title))
        materialDirectory.__init__(self, path=path)
        self._iter_queue.append(self)
    
    
    def __iter__(self) -> courseDirectory:
        """Iterate between all the directories of the course."""
        if not self.valid:
            raise OSError(f"{self.path} is not a valid directory.")
        return self
        
        
    def __next__(self) -> materialDirectory:
        """Get the next directory of the course."""
        if not self._iter_queue:
            raise StopIteration
        next_dir = self._iter_queue.pop(0)
        for dir in next_dir.dirs:
            self._iter_queue.append(dir)
        return next_dir
        
    
    def export_material(self) -> List[Dict[str, Union[str, List[str], Dict[str, str]]]]:
        """Export into a list of dictionaries all the directory of the course."""
        result = []
        for dir in self:
            files = [file.export() for file in dir.files]
            result.append({
                'title'         :   dir.title,
                'breadcrumbs'   :   dir.breadcrumbs,
                'files'         :   files
            })
        result.sort(key=(lambda material: len(material['breadcrumbs'])), reverse=False)
        return result
    