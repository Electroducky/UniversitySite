from university_system.models import department_info_manager, department_manager


def get_title_list(level=None):
    departments = department_manager.search('level') if level is None else department_manager.search('level',
                                                                                                     level)
    titles_and_ids = []
    if departments is not None:
        for department in departments:
            department_info = department_info_manager.get(department.info_id)
            titles_and_ids.append((department_info.department_id, department_info.title))
        return titles_and_ids
    else:
        return []
