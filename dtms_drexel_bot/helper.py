from dtms_client.DMTSClient import DrexelTMSClass


def tms_course_to_row(dtms_course: DrexelTMSClass):
    c = dtms_course
    return f"{c.course_number} {c.days_time} {c.section} {c.crn} {c.instruction_method} {c.instruction_type} {c.instructors}"
