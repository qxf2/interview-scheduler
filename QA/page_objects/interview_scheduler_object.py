from .Base_Page import Base_Page
import conf.locators_conf as locators
from selenium import webdriver
from utils.Wrapit import Wrapit
import conf.name_conf 


class Interview_Scheduler_Object:

    COL_NAME = 1

    def remove_interviewer(self):
        
        interviewers_name = self.get_elements(locators.find_rows)
        result_flag = False
        name = conf.name_conf.name
    
        for index,value in enumerate(interviewers_name):
            if name == value.text.lower():
                index = index + 1
                result_flag = self.click_element(locators.delete_button%index)
                result_flag = self.get_element(locators.confirmation_Pop_up).click()
                result_flag = self.get_element(locators.close_pop_up).click()
        print(result_flag)
        return result_flag

    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def get_all_text(self):
        "Get the text within the table"
        table_text = []
        row_doms = self.get_elements(locators.tab_rows)
        for index,row_dom in enumerate(row_doms):
            row_text = []
            cell_doms = self.get_elements(locators.relative_xpath%(index+1))
            for cell_dom in cell_doms:
                row_text.append(self.get_dom_text(cell_dom).decode('utf-8'))
            table_text.append(row_text)
                        
        return table_text

    @Wrapit._exceptionHandler
    def get_column_names(self):
        "Return a list with the column names"
        column_names = []
        col_doms = self.get_elements(locators.column_header)
        for col_dom in col_doms:
            column_names.append(self.get_dom_text(col_dom).decode('utf-8'))
    
        return column_names

    def get_column_text(self,column_name):
        "Get the text within a column"
        column_text = []
        col_index = -1
        if column_name.lower()=='interviewer name':
            col_index = self.COL_NAME
       

        if col_index > -1:
            table_text = self.get_all_text()
            #Transpose the matrix since you want the column
            column_text = list(zip(*table_text))[col_index]

        return column_text

    @Wrapit._exceptionHandler
    def check_cell_text_present(self,text,column_name='all'):
        "Check if the text you want is present in a cell"
        result_flag = False
        if column_name == 'all':
            table_text = self.get_all_text()
        else:
            table_text = [self.get_column_text(column_name)]
        
        for row in table_text:
            for col in row:
                if col.lower() == text.lower():
                    result_flag = True
                    break
            if result_flag is True:
                break

        return result_flag

    @Wrapit._exceptionHandler
    def check_name_present(self,name):
        "Check if the supplied name is present anywhere in the table"
        return self.check_cell_text_present(name,column_name='interviewer name')


    @Wrapit._exceptionHandler
    def print_table_text(self):
        "Print out the table text neatly"
        result_flag = False
        column_names = self.get_column_names()
        table_text = self.get_all_text()
        self.write('||'.join(column_names))
        if table_text is not None:
            for row in table_text:
                self.write('|'.join(row))
            result_flag = True
                
        return result_flag

    

    


    

    


   
        

   