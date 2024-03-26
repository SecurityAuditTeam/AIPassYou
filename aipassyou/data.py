from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

class Profile(BaseModel):
    """
    Profile information from social network 
    """
    id: int = Field(description = "Numerical identifier")
    username: str = Field(description = "Username from social network")
    full_name: str = Field(default = None, description = "Full name provided for this user")
    age: int = Field(default = None, description = "Approximation of the user's age")
    biography: str = Field(default = None, description = "Profile description")
    location: str = Field(default = None, description = "Location, country or city")
    education: str = Field(default = None, description = "Education information provided")
    work: str = Field(default = None, description = "Work experience")
    # family: str = None or list[User] =

class Answer(BaseModel):
    """
    Answers or replies to publications
    """
    id: int = Field(description = "Numerical identifier")
    date: datetime = Field(description = "Publishing date")
    content: str = Field(description = "Raw content of the reply")
    user: Profile = Field(description = "Author profile information")

class Post(BaseModel):
    """
    Information from user puublications 
    """
    id: int = Field(description = "Numerical identifier")
    date: datetime = Field(description = "Publishing date")
    content: str = Field(description = "Raw content of the message")
    title: str = Field(default = None, description = "Post title")
    answers: list[Answer] = Field(default = [], description = "List of answers from other profiles")

'''
class Job(BaseModel):
    """
    Job information
    """
    start_date: str = Field(description = "Position start date")
    end_date: datetime = Field(description = "Position end date")
    title: str = Field(description = "Job title")
    company: str = Field(description = "Employer company name")
    location: str = Field(default = None, description = "job country or city")
'''

class User(BaseModel):
    """
    User information extracted from a social network
    """
    network: str = Field(description = "Social network")
    profile: Profile = Field(default = None, description = "User profile inforation")

    posts: list[Post] = Field(default = [], description = "List of user posts or publications")
    following: list[Profile] = Field(default = [], description = "List of profiles followed by the user")
    #jobs: list[Job] = Field(default = [], description = "List of answers from other profiles")
    
    locations: list[str] = Field(default = [], description = "List of locations extracted from user data")
    hashtags: list[str] = Field(default = [], description = "List of hashtags extracted from user data")
    hobbies: list[str] = Field(default = [], description = "List of hobbies extracted from user data")
    dates: list[str] = Field(default = [], description = "List of dates extracted from user data")

class Scan(BaseModel):
    """
    Run information
    """
    args: list[str] = Field(description = "Command line arguments")
    start_date: datetime = Field(default_factory=datetime.now, description = "Start date")
    end_date: datetime = Field(default = None, description = "End date")

    results: list[User] = Field(default = [], description = "List of information from social networks")
