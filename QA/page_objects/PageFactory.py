"""
PageFactory uses the factory design pattern. 
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
"""

from page_objects.main_page import main_page
class PageFactory():
    "PageFactory uses the factory design pattern."
    def get_page_object(page_name,base_url='http://3.219.215.68/',trailing_slash_flag=True):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["main page", "main", "landing", "landing page"]:
            test_obj = main_page(base_url=base_url,trailing_slash_flag=trailing_slash_flag)
        
        return test_obj

    get_page_object = staticmethod(get_page_object)