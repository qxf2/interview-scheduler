
from page_objects.main_page import main_page
from .interview_scheduler_page import Interview_Scheduler_Page
import conf.base_url_conf

class PageFactory():
    "PageFactory uses the factory design pattern."
    def get_page_object(page_name,base_url=conf.base_url_conf.base_url,trailing_slash_flag=True):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["main page", "main", "landing", "landing page"]:
            test_obj = main_page(base_url=base_url,trailing_slash_flag=trailing_slash_flag)
        elif page_name == "list of interviewer details":
            test_obj = Interview_Scheduler_Page(base_url=base_url)
        
        return test_obj

    get_page_object = staticmethod(get_page_object)