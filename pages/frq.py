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
prompt="Grade the student's response to " + question + "and score it out of 9 points (award one point for each term that is correctly applied)"
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