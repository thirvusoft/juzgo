import frappe
def validate(doc,action):
    total_act_point = 0
    total_sco_point = 0
    for i in doc.interview_results:
        total_act_point = (i.actual_points or 0) + total_act_point
        total_sco_point = (i.score_points or 0) + total_sco_point
    doc.total_actual_points = total_act_point
    doc.total_score_points = total_sco_point
@frappe.whitelist()
def get_interview_questions(interview_round = None, interview = None):
    if (not interview or not interview_round):
        return []
    questions = frappe.get_all("Interview Questions", filters={"parent": interview_round}, fields=["*"])
    answers = frappe.get_all("Interview Response", filters={"interview": interview}, limit=1, order_by="creation desc")
    if answers:
        answer = frappe.get_doc("Interview Response", answers[0])
        for row in answer.interview_response_question_tab:
            if row.interview_question or row.question:
                for ques in questions:
                    if row.interview_question:
                        if row.interview_question == ques.interview_question:
                            ques.applicants_answer = row.answer
                            break
                    else:
                        if row.question == ques.question:
                            ques.applicants_answer = row.answer
                            break
    
    return questions
