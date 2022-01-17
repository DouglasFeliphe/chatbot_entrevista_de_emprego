
def create_questions_file():
    f = open("questions.txt", "x")

def save_question_in_file(question):
    with open('./questions.txt', 'a') as f:
        f.write(f'\n\n{question}')
    print('Question Saved')
    
def save_answer_in_file(answer):
    with open('./questions.txt', 'a') as f:
        f.write(f'\n{answer}')
    print('Answer Saved')       

    
            