
import re
from typing import Optional, Any, Callable
from typing import Protocol, ClassVar



class SerializerInterface(Protocol):
    name: ClassVar[str]
    regex: ClassVar[str]
    regex_group: ClassVar[Optional[int]]
    required: ClassVar[bool]
    addit_parser: ClassVar[Optional[Callable]]

    data: Any
    validated_data: Any


class BaseSerializer(SerializerInterface):

    def __init__(self, data: str, *args, **kwargs) -> None:
        if data:
            self.data = data
            self.validated_data = self.validate(data)
        super().__init__(*args, **kwargs)
    
    def validate(self, data):
        match = re.search(self.regex, data)
        if match:
            val = match.group(getattr(self,"regex_group", 1))
        else:
            raise Exception
        if self.addit_parser:
            val = self.addit_parser(val)
        return val

    
class SummarySerializer(BaseSerializer):
    """all the data"""

    name = "summary_data"
    regex = '(.*)'
    regex_group = 1
    required = True
    addit_parser = None


class TitleSerializer(BaseSerializer):

    name = "title"
    regex = 'title="(.+?)<'
    regex_group = 1
    required = True
    addit_parser = None


class CompanySerializer(BaseSerializer):

    name = "company"
    regex = 'companyName">(.+?)<'
    regex_group = 1
    required = True
    
    @staticmethod
    def addit_parser(val: str):
        """Additional parser for company
        
        long company strings often occur when there's a link to the company's page. parse further
        """
        if len(val) > 50:
            val = val.split('>')[-1]
        return val


class SalarySerializer(BaseSerializer):

    name = "salary"
    regex = 'salary-snippet"><span>(.+?)<'
    regex_group = 1
    required = False
    addit_parser = None


class LocationSerializer(BaseSerializer):

    name = "location"
    regex = 'companyLocation">(.+?)<'
    regex_group = 1
    required = False
    addit_parser = None

