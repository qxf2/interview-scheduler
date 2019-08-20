#Common locator file for all locators
#Locators are ordered alphabetically

############################################
#Selectors we can use
#ID
#NAME
#css selector
#CLASS_NAME
#LINK_TEXT
#PARTIAL_LINK_TEXT
#XPATH
###########################################

#Locators for the Main page
TEMPERATURE_FIELD = "id,temperature"
BUY_BUTTON = "xpath,//button[contains(text(),'Buy %s')]"

#Product page
PAGE_HEADING = "xpath,//h2[text()='%s']"
PRODUCTS_LIST = "xpath,//div[contains(@class,'col-4')]"
ADD_PRODUCT_BUTTON = "xpath,//div[contains(@class,'col-4') and contains(.,'%s')]/descendant::button[text()='Add']"
CART_QUANTITY_TEXT = "id,cart"
CART_BUTTON = "xpath,//button[@onclick='goToCart()']"

#Cart page
CART_TITLE = "xpath,//h2[text()='Checkout']"
CART_ROW = "xpath,//tbody/descendant::tr"
CART_ROW_COLUMN = "xpath,//tbody/descendant::tr[%d]/descendant::td"
CART_TOTAL = "id,total"

#Pay With card
PAY_WITH_CARD_BUTTON ="xpath,//span[contains(text(),'Pay with Card')]"
PAY_WITH_CARD_TITTLE ="xpath,//h1[@text()='Stripe.com']"
EMAIL ="xpath,//input[@type='email']"
CARD_NUMBER = "xpath,//input[@placeholder='Card number']"
EXPIRY_DATE = "xpath,//input[@placeholder='MM / YY']"
CVC_NUMBER = "xpath,//input[@placeholder='CVC']"
ZIPCODE = "xpath,//input[@placeholder='ZIP Code']"
CHECKBOX_TICK = "xpath,//div[contains(@class,'Checkbox-tick']"
MOBILE_NUMBER = "xpath,//input[@autocomplete='mobile tel']"
SUBMIT_BUTTON = "xpath,//button[@type='submit']"
PAYMENT_SUCESS_TITTLE = "xpath,//h2[text()='PAYMENT SUCCESS']"
IFRAME_NAME = "//iframe[@name='stripe_checkout_app']"