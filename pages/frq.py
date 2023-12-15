import openai
import streamlit as st

openai.api_key = st.secrets['api_secret']


st.subheader("free-response question demo")
topic = st.sidebar.selectbox(
    "course",
    ('AP Psychology', 'AP Human Geography'),
)
frq_specificities=['it should describe a scenario and ask students to explain how nine different psychology terms apply to that scenario.', 'it should describe a scenario and give students seven different questions, asking human geography terms apply to that scenario.']
if topic=='AP Psychology':
    idx=0
else:
     idx=1
question_retrieve=openai.completions.create(model='gpt-3.5-turbo-instruct',
                                            prompt=f"write a free response question about {topic}"+frq_specificities[idx],
                                            max_tokens=1200, 
                                            temperature = 0.5,
                                            stream = False)
question=question_retrieve.choices[0].text
st.markdown(question)

user_input = st.text_area("Your answer: ",placeholder = "Write your response", key="input")
prompt=['\''+user_input+'\''+" is the student's full answer. Do not complete the response or add any additional information. Grade the student's response to "+'\''+question+'\''+"and score it out of 9 points, awarding points if the term is EXPLICITLY mentioned AND contains an ACCURATE application to the scenario. Grade very harshly and do not award pity points. Explain how every single point was earned and report the final score on a new line.",
        '\''+user_input+'\''+" is the student's full answer. Do not complete the response or add any additional information. Grade the student's response to "+'\''+question+'\''+"and score it out of 7 points, awarding points if the term is EXPLICITLY mentioned AND contains an ACCURATE answer to the question. Grade very harshly and do not award pity points. Explain how every single point was earned and report the final score on a new line."]
full_str=prompt[idx]+question+user_input

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
