"""
PageFactory uses the factory design pattern. 
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
"""

from page_objects.main_page import main_page
#from page_objects.Sunscreens_Page import Sunscreens_Page
#from page_objects.Moisturizers_Page import Moisturizers_Page
#from page_objects.Cart_Page import Cart_Page
class PageFactory():
    "PageFactory uses the factory design pattern."
    def get_page_object(page_name,base_url=' http://127.0.0.1:6464/',trailing_slash_flag=True):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["main page", "main", "landing", "landing page"]:
            test_obj = main_page(base_url=base_url,trailing_slash_flag=trailing_slash_flag)
        
        return test_obj

    get_page_object = staticmethod(get_page_object)