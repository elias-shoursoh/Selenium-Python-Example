import allure
from selenium.webdriver.common.by import By

from pages.top_bars.top_navigate_bar import TopNavigateBar
from selenium.webdriver.support import expected_conditions


class ProjectsPage(TopNavigateBar):
    """ Projects page - Where projects are added and edited"""

    _START_BUTTON = (By.CSS_SELECTOR, "#app .px-4 a")
    _CREATE_NEW_WORKSPACE_BUTTON = (By.CSS_SELECTOR, ".font-medium button")
    _WORKSPACE_EDIT_BUTTON = (By.CSS_SELECTOR, "[data-icon='chevron-down']")
    _RENAME_WORKSPACE_BUTTON = (By.CSS_SELECTOR, ".mr-3 .hover\\:bg-gray-600")
    _DELETE_WORKSPACE_BUTTON = (By.CSS_SELECTOR, ".mr-3 .text-red-600")
    _RENAME_FIELD = (By.CSS_SELECTOR, ".vue-portal-target input")
    _CONFIRMATION_BUTTON = (By.CSS_SELECTOR, "#confirm-create-button")
    _NEW_WORKSPACE_NAME_FIELD = (By.CSS_SELECTOR, "[placeholder='Workspace name']")
    _DELETE_WORKSPACE_FIELD = (By.CSS_SELECTOR, ".h-12")
    _CREATE_PROJECT_BUTTON = (By.CSS_SELECTOR, ".hidden.px-3")
    _SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-icon='search']")
    _SEARCH_FIELD = (By.CSS_SELECTOR, "[type='text']")
    _CONFIRM_DELETE_PROJECT_BUTTON = (By.CSS_SELECTOR, "#confirm-delete-button")
    _CANCEL_PROJECT_DELETION_BUTTON = (By.CSS_SELECTOR, "form [type='button'")
    _PROJECT_PAGE_TITLE = (By.CSS_SELECTOR, "#app h1.leading-tight.truncate")

    _WORKSPACE_LIST = (By.CSS_SELECTOR, ".mt-6 a")
    _PROJECT_BLOCK = (By.CSS_SELECTOR, "#app .max-w-full div .mt-4 > .mt-8 > div")

    def __init__(self):
        super().__init__()

    @allure.step("Create new workspace {workspace_name}")
    def create_workspace(self, workspace_name):
        self.click(self._CREATE_NEW_WORKSPACE_BUTTON)
        self.fill_text(self._NEW_WORKSPACE_NAME_FIELD, workspace_name)
        self.click(self._CONFIRMATION_BUTTON)

    @allure.step("Delete a workspace")
    def delete_workspace(self):
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        # in case only the main workspace exists, then create another
        if len(workspaces) < 2:
            self.create_workspace("test")
            workspaces = self._wait.until(
                expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        # click on the second created workspace
        workspaces[1].click()
        self.click(self._WORKSPACE_EDIT_BUTTON)
        self.click(self._DELETE_WORKSPACE_BUTTON)
        # get the name of the workspace to delete from the background text in delete workspace field
        name = self._driver.find_element(*self._DELETE_WORKSPACE_FIELD).get_attribute("placeholder")
        self.fill_text(self._DELETE_WORKSPACE_FIELD, name)
        self.click(self._CONFIRMATION_BUTTON)

    @allure.step("Rename workspace {old_name} to {new_name}")
    def rename_workspace(self, old_name, new_name):
        flag = False
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        # get workspaces as text
        workspaces_text_list = [workspace.text for workspace in workspaces]
        # if the old workspace name is not present in list, then add it
        for i in range(len(workspaces_text_list)):
            if old_name in workspaces_text_list[i]:
                flag = True
                break
        # case the old workspace is not present
        if not flag:
            self.create_workspace(old_name)
            workspaces = self._wait.until(
                expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        for workspace in workspaces:
            if old_name in workspace.text:
                workspace.click()
                self.click(self._WORKSPACE_EDIT_BUTTON)
                self.click(self._RENAME_WORKSPACE_BUTTON)
                self.fill_text(self._RENAME_FIELD, new_name)
                self.click(self._CONFIRMATION_BUTTON)
                break

    @allure.step("Get workspaces number")
    def get_workspaces_number(self):
        self._wait.until(
            expected_conditions.invisibility_of_element_located(self._NEW_WORKSPACE_NAME_FIELD))
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        return len(workspaces)

    @allure.step("Get number of projects display on page")
    def get_projects_number_in_page(self):
        projects = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._PROJECT_BLOCK))
        return len(projects)

    @allure.step("Get number of projects displayed next to main workspace (My Workspace) name")
    def get_projects_number_from_workspace(self):
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        number = workspaces[0].find_element_by_css_selector("span:nth-child(2)")
        return int(number.text)

    @allure.step("Verify if workspace {workspace_name} exists")
    def is_workspace_found(self, workspace_name):
        self._wait.until(expected_conditions.invisibility_of_element_located(self._RENAME_FIELD))
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        for workspace in workspaces:
            if workspace_name in workspace.text:
                return True
        return False

    @allure.step("Get projects' page title")
    def get_title(self):
        return self.get_text(self._PROJECT_PAGE_TITLE)
