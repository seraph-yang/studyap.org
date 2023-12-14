import openai
import streamlit as st

openai.api_key = st.secrets['api_secret']


st.subheader("free-response question demo")


question_retrieve=openai.completions.create(model='gpt-3.5-turbo-instruct',
                                            prompt="write a free response question about psychology. it should describe a scenario and ask students to explain how nine different psychology terms apply to that scenario.",
                                            max_tokens=120, 
                                            temperature = 0.5,
                                            stream = False)
question=question_retrieve.choices[0].text
st.markdown(question)

user_input = st.text_area("Your answer: ",placeholder = "Write your response", key="input")
prompt=user_input + " is the student's full answer. Do not complete the response or add any additional information. Grade the student's response to " + question + "and score it out of 9 points (award one point for each term that is correctly applied). Be very harsh when grading. Do not award pity points. Award points only if the term is explicitly mentioned and contains a meaningful and accurate explanation. Justify your score as well. Your response should begin with the score and the score and explanation should be on separate lines."
full_str=prompt+question+user_input

if st.button("Submit", type="primary"):
    st.markdown("----")
    res_box = st.empty()
    report=[]
    for resp in openai.completions.create(model='gpt-3.5-turbo-instruct',
                                            prompt=full_str,
                                            max_tokens=120, 
                                            temperature = 0.5,
                                            stream = True):
            report.append(resp.choices[0].text)
            result = "".join(report).strip()
            result = result.replace("\n", "")        
            res_box.markdown(f'*{result}*') 
    res_box.write(result)
st.markdown("----")
