import pandas as pd
import os, sys, time
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper
import rai_guide
import streamlit as st
from menu import menu

def stakeholder_section(st, sys_info, us_description, is_direct):
    sh_type = "direct" if is_direct else "indirect"
    sh_enum = helper.Task.DIRECT_SH.value if is_direct else helper.Task.INDIRECT_SH.value

    if us_description != '' and f'{sh_enum}_task_status' not in st.session_state:
        helper.send_req(st, sys_info, sh_enum)

    st.subheader(f"{sh_type.capitalize()} Stakeholders") 
    if is_direct:
        st.write(rai_guide.direct_stakeholder_def)
    else:
        st.write(rai_guide.indirect_stakeholder_def)
    st.write(f"_Click the button below to brainstorm {sh_type} stakeholders_")

    stakeholder_button = st.button(f"Help me brainstorm potential {sh_type} stakeholders",use_container_width=True)

    if f'{sh_enum}_clicked' in st.session_state and f'{sh_enum}_result' in st.session_state:
        with st.container(border=True):
            st.write(st.session_state[f'{sh_enum}_result'])

    if stakeholder_button:
        if us_description != '':
            st.session_state[f'{sh_enum}_clicked'] = True
            if f'{sh_enum}_task_status' in st.session_state:
                if st.session_state[f'{sh_enum}_task_status'] == 'Running':
                    with st.spinner('Generating Stakeholders...'):
                        while True:
                            result = helper.poll_task_status(st, st.session_state[f'{sh_enum}_task_id'], sh_enum)
                            if result:
                                result = result.replace("Direct Obvious Stakeholders", "Direct Stakeholders")\
                                      .replace("Direct Surprising Stakeholders", "Other Direct Stakeholders")\
                                      .replace("Indirect Obvious Stakeholders", "Indirect Stakeholders")\
                                      .replace("Indirect Surprising Stakeholders", "Other Indirect Stakeholders")
                                with st.container(border=True):
                                    st.write(result)
                                st.session_state[f"{sh_enum}_result"] = result
                                break
                            else:
                                time.sleep(5)
        else:
            st.write("Please fill in an user story first")

    def update_df():
        updates = st.session_state[f'{sh_type}_stakeholders_changes']
        df = st.session_state[f'{sh_type}_stakeholders']

        # Handle edited rows
        for idx, changes in updates['edited_rows'].items():
            for col, val in changes.items():
                df.at[idx, col] = val
                
        # Handle added rows
        for _ in updates['added_rows']:
            df = pd.concat([df, pd.DataFrame([{f'{sh_type.capitalize()} Stakeholders':''}])], ignore_index=True)
            
        # Handle deleted rows
        df = df.drop(updates['deleted_rows']).reset_index(drop=True)

        st.session_state[f'{sh_type}_stakeholders'] = df

    if f'{sh_type}_stakeholders' not in st.session_state:
        st.session_state[f'{sh_type}_stakeholders'] = pd.DataFrame(
            [
                {f"{sh_type.capitalize()} Stakeholders": ""},
                {f"{sh_type.capitalize()} Stakeholders": ""},
                {f"{sh_type.capitalize()} Stakeholders": ""},
                {f"{sh_type.capitalize()} Stakeholders": ""},
                {f"{sh_type.capitalize()} Stakeholders": ""},
            ]
        )

    st.data_editor(st.session_state[f'{sh_type}_stakeholders'],  num_rows="dynamic", hide_index=True, use_container_width=True, key=f'{sh_type}_stakeholders_changes', on_change=update_df)

st.header(f"Section 2: Stakeholders Identification")

us_description = st.session_state.get(f'us1_des', "").strip()
sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {us_description}"

st.write(f"User Story #1 : **{us_description if us_description != '' else '[Please enter an user story in section 1]'}**")

st.write("_First, identify the system's stakeholders for your primary user story. Think broadly about the people impacted directly and indirectly. Then, for each stakeholder, document the goals and potential concerns._")

stakeholder_section(st, sys_info, us_description, True)
stakeholder_section(st, sys_info, us_description, False)
        
all_stakeholders = helper.get_stakeholders(st)
st.session_state['can_display_fairness_sections'] = len(all_stakeholders) > 0

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        if len(all_stakeholders) > 0:
            st.switch_page("pages/section4.py")
        else:
            st.toast("Please fill in the stakeholders")

menu(st)