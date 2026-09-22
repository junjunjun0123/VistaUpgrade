import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import io

# Page config
st.set_page_config(
    page_title="VISTA Upgrade Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .success {
        background-color: #d4edda;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .warning {
        background-color: #fff3cd;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
    .error {
        background-color: #f8d7da;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        'modules': {
            'Vista Head Office': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started',
                'owner': '',
                'start_date': '',
                'end_date': ''
            },
            'Vista Connect': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started',
                'owner': '',
                'start_date': '',
                'end_date': ''
            },
            'Vista Loyalty': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started',
                'owner': '',
                'start_date': '',
                'end_date': ''
            },
            'Vista Voucher': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started',
                'owner': '',
                'start_date': '',
                'end_date': ''
            },
            'Vista Cinema': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started',
                'owner': '',
                'start_date': '',
                'end_date': ''
            },
            'Vista Programming': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started',
                'owner': '',
                'start_date': '',
                'end_date': ''
            }
        },
        'created_date': datetime.now().isoformat(),
        'target_version': '5.0.18',
        'current_version': '5.0.13',
        'test_cases': [],
        'issues': [],
        'notes': []
    }

# ==================== UTILITY FUNCTIONS ====================
def get_module_stats(module_data):
    """Calculate stats for a module"""
    all_tasks = []
    for stage_tasks in module_data['stages'].values():
        all_tasks.extend(stage_tasks)
    
    total = len(all_tasks)
    completed = sum(1 for task in all_tasks if task.get('completed', False))
    
    return {
        'total': total,
        'completed': completed,
        'progress': (completed / total * 100) if total > 0 else 0
    }

def get_project_stats():
    """Calculate overall project stats"""
    total_modules = len(st.session_state.project_data['modules'])
    total_tasks = 0
    completed_tasks = 0
    
    for module_data in st.session_state.project_data['modules'].values():
        stats = get_module_stats(module_data)
        total_tasks += stats['total']
        completed_tasks += stats['completed']
    
    return {
        'total_modules': total_modules,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }

def create_progress_chart():
    """Create overall progress visualization"""
    stats = get_project_stats()
    
    fig = go.Figure(data=[
        go.Bar(
            x=['Completed', 'Remaining'],
            y=[stats['completed_tasks'], stats['total_tasks'] - stats['completed_tasks']],
            marker=dict(color=['#667eea', '#e0e0e0']),
            text=[stats['completed_tasks'], stats['total_tasks'] - stats['completed_tasks']],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Task Progress Overview',
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def create_module_breakdown():
    """Create module completion breakdown"""
    modules = st.session_state.project_data['modules']
    module_names = []
    module_progress = []
    
    for name, data in modules.items():
        stats = get_module_stats(data)
        module_names.append(name.replace('Vista ', ''))
        module_progress.append(stats['progress'])
    
    fig = px.bar(
        x=module_names,
        y=module_progress,
        title='Module Completion Status',
        color=module_progress,
        color_continuous_scale='Viridis',
        height=300,
        labels={'y': 'Progress (%)', 'x': 'Module'}
    )
    
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def export_to_json():
    """Export project data as JSON"""
    return json.dumps(st.session_state.project_data, indent=2, default=str)

def export_to_csv():
    """Export project data as CSV"""
    export_data = []
    for module_name, module_info in st.session_state.project_data['modules'].items():
        for stage in ['Planning', 'Testing', 'Development']:
            for task in module_info['stages'][stage]:
                export_data.append({
                    'Module': module_name,
                    'Stage': stage,
                    'Task': task['name'],
                    'Completed': 'Yes' if task.get('completed', False) else 'No'
                })
    
    df_export = pd.DataFrame(export_data)
    return df_export.to_csv(index=False)

# ==================== SIDEBAR NAVIGATION ====================
st.sidebar.title("🚀 VISTA Upgrade Portal")
st.sidebar.markdown(f"**v{st.session_state.project_data['current_version']} → v{st.session_state.project_data['target_version']}**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📋 Project Planning",
        "🧪 Test Cases",
        "🐛 Issues Tracker",
        "📝 Notes & Docs",
        "📤 Import/Export",
        "📈 Analytics & Reports"
    ]
)

st.sidebar.markdown("---")

# Quick Stats in Sidebar
stats = get_project_stats()
st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Modules", stats['total_modules'])
st.sidebar.metric("Tasks", stats['total_tasks'])
st.sidebar.metric("Completed", stats['completed_tasks'])
st.sidebar.metric("Progress", f"{stats['progress']:.1f}%")

# ==================== PAGE: DASHBOARD ====================
if page == "📊 Dashboard":
    st.title("📊 Project Dashboard")
    
    # Header metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Modules", stats['total_modules'])
    with col2:
        st.metric("Total Tasks", stats['total_tasks'])
    with col3:
        st.metric("Completed Tasks", stats['completed_tasks'])
    with col4:
        st.metric("Overall Progress", f"{stats['progress']:.1f}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_progress_chart(), use_container_width=True)
    with col2:
        st.plotly_chart(create_module_breakdown(), use_container_width=True)
    
    st.markdown("---")
    
    # Module Status Table
    st.subheader("📋 Module Status Overview")
    
    module_data = []
    for module_name, module_info in st.session_state.project_data['modules'].items():
        stats_mod = get_module_stats(module_info)
        module_data.append({
            'Module': module_name,
            'Status': module_info['status'],
            'Owner': module_info.get('owner', '-'),
            'Tasks': f"{stats_mod['completed']}/{stats_mod['total']}",
            'Progress': f"{stats_mod['progress']:.0f}%"
        })
    
    df = pd.DataFrame(module_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== PAGE: PROJECT PLANNING ====================
elif page == "📋 Project Planning":
    st.title("📋 Project Planning & Execution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_module = st.selectbox(
            "Select Module to Edit",
            list(st.session_state.project_data['modules'].keys())
        )
    
    with col2:
        if st.button("➕ Add New Module"):
            st.session_state.show_add_module = True
    
    if 'show_add_module' in st.session_state and st.session_state.show_add_module:
        new_module_name = st.text_input("Enter new module name")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Add"):
                if new_module_name and new_module_name not in st.session_state.project_data['modules']:
                    st.session_state.project_data['modules'][new_module_name] = {
                        'stages': {'Planning': [], 'Testing': [], 'Development': []},
                        'new_features': '',
                        'bug_fixes': '',
                        'status': 'Not Started',
                        'owner': '',
                        'start_date': '',
                        'end_date': ''
                    }
                    st.session_state.show_add_module = False
                    st.rerun()
        with col2:
            if st.button("✗ Cancel"):
                st.session_state.show_add_module = False
    
    st.markdown("---")
    
    module_info = st.session_state.project_data['modules'][selected_module]
    stats_mod = get_module_stats(module_info)
    
    # Module Configuration
    st.subheader(f"⚙️ {selected_module} Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        module_info['status'] = st.selectbox(
            "Module Status",
            ["Not Started", "Planning", "In Progress", "Testing", "Completed"],
            index=["Not Started", "Planning", "In Progress", "Testing", "Completed"].index(module_info.get('status', 'Not Started')),
            key=f"status_{selected_module}"
        )
    
    with col2:
        module_info['owner'] = st.text_input(
            "Owner",
            value=module_info.get('owner', ''),
            key=f"owner_{selected_module}"
        )
    
    with col3:
        st.metric("Progress", f"{stats_mod['progress']:.1f}%")
    
    st.progress(stats_mod['progress'] / 100)
    
    col1, col2 = st.columns(2)
    with col1:
        module_info['start_date'] = st.date_input(
            "Start Date",
            key=f"start_{selected_module}"
        )
    with col2:
        module_info['end_date'] = st.date_input(
            "End Date",
            key=f"end_{selected_module}"
        )
    
    st.markdown("---")
    
    # Planning Stages
    st.subheader("📍 Planning Stages")
    
    tabs = st.tabs(['Planning', 'Testing', 'Development'])
    
    for tab_idx, stage in enumerate(['Planning', 'Testing', 'Development']):
        with tabs[tab_idx]:
            tasks = module_info['stages'][stage]
            
            if tasks:
                for idx, task in enumerate(tasks):
                    col1, col2, col3, col4 = st.columns([0.08, 0.7, 0.1, 0.12])
                    
                    with col1:
                        task_completed = st.checkbox(
                            "✓",
                            value=task.get('completed', False),
                            key=f"task_{selected_module}_{stage}_{idx}"
                        )
                        task['completed'] = task_completed
                    
                    with col2:
                        st.write(f"{'~~' if task_completed else ''}{task['name']}{'~~' if task_completed else ''}")
                    
                    with col3:
                        if st.button("Edit", key=f"edit_{selected_module}_{stage}_{idx}", use_container_width=True):
                            task['name'] = st.text_input("Edit task", value=task['name'], key=f"edit_input_{idx}")
                    
                    with col4:
                        if st.button("🗑️", key=f"delete_{selected_module}_{stage}_{idx}", use_container_width=True):
                            module_info['stages'][stage].pop(idx)
                            st.rerun()
                    
                    st.divider()
            else:
                st.info(f"No tasks in {stage} yet")
            
            # Add new task
            new_task = st.text_input(
                f"Add new {stage} task",
                key=f"new_task_{selected_module}_{stage}",
                placeholder=f"Enter a new {stage} task..."
            )
            
            if st.button(f"Add {stage} Task", key=f"add_task_{selected_module}_{stage}", use_container_width=True):
                if new_task.strip():
                    module_info['stages'][stage].append({
                        'name': new_task.strip(),
                        'completed': False
                    })
                    st.rerun()
    
    st.markdown("---")
    
    # New Features and Bug Fixes
    st.subheader("📝 Additional Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**✨ New Features**")
        module_info['new_features'] = st.text_area(
            "New Features for this module",
            value=module_info.get('new_features', ''),
            key=f"features_{selected_module}",
            height=150
        )
    
    with col2:
        st.write("**🐛 Bug Fixes**")
        module_info['bug_fixes'] = st.text_area(
            "Bug Fixes for this module",
            value=module_info.get('bug_fixes', ''),
            key=f"bugs_{selected_module}",
            height=150
        )

# ==================== PAGE: TEST CASES ====================
elif page == "🧪 Test Cases":
    st.title("🧪 Test Cases Management")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Manage and track test cases for the upgrade")
    with col2:
        if st.button("➕ Add Test Case"):
            st.session_state.show_add_test = True
    
    st.markdown("---")
    
    # Add Test Case
    if 'show_add_test' in st.session_state and st.session_state.show_add_test:
        with st.form("add_test_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                test_module = st.selectbox("Module", list(st.session_state.project_data['modules'].keys()))
            with col2:
                test_name = st.text_input("Test Case Name")
            
            col1, col2 = st.columns(2)
            with col1:
                test_status = st.selectbox("Status", ["Pending", "In Progress", "Passed", "Failed", "Blocked"])
            with col2:
                test_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            
            test_description = st.text_area("Test Description")
            test_expected = st.text_area("Expected Result")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✓ Add Test Case", use_container_width=True):
                    st.session_state.project_data['test_cases'].append({
                        'id': len(st.session_state.project_data['test_cases']) + 1,
                        'module': test_module,
                        'name': test_name,
                        'status': test_status,
                        'priority': test_priority,
                        'description': test_description,
                        'expected': test_expected,
                        'created_date': datetime.now().isoformat()
                    })
                    st.session_state.show_add_test = False
                    st.success("Test case added!")
            with col2:
                if st.form_submit_button("✗ Cancel", use_container_width=True):
                    st.session_state.show_add_test = False
    
    st.markdown("---")
    
    # Test Cases List
    if st.session_state.project_data['test_cases']:
        st.subheader("Test Cases Summary")
        
        test_data = []
        for test in st.session_state.project_data['test_cases']:
            test_data.append({
                'ID': test['id'],
                'Module': test['module'],
                'Test Name': test['name'],
                'Status': test['status'],
                'Priority': test['priority']
            })
        
        df_tests = pd.DataFrame(test_data)
        st.dataframe(df_tests, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Test Status Summary
        st.subheader("Test Status Summary")
        
        status_counts = {}
        for test in st.session_state.project_data['test_cases']:
            status = test['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        col1, col2, col3, col4, col5 = st.columns(5)
        colors = {'Pending': '🟡', 'In Progress': '🔵', 'Passed': '🟢', 'Failed': '🔴', 'Blocked': '⚫'}
        
        for col, (status, count) in zip([col1, col2, col3, col4, col5], status_counts.items()):
            with col:
                st.metric(f"{colors.get(status, '')} {status}", count)
        
        st.markdown("---")
        
        # Detailed View
        st.subheader("Test Cases Details")
        
        for test in st.session_state.project_data['test_cases']:
            with st.expander(f"🔹 {test['name']} - {test['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Module:** {test['module']}")
                    st.write(f"**Priority:** {test['priority']}")
                with col2:
                    st.write(f"**Status:** {test['status']}")
                    st.write(f"**Created:** {test['created_date'][:10]}")
                
                st.write(f"**Description:** {test['description']}")
                st.write(f"**Expected Result:** {test['expected']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_test_{test['id']}"):
                        st.info("Edit functionality coming soon")
                with col2:
                    if st.button("Delete", key=f"delete_test_{test['id']}"):
                        st.session_state.project_data['test_cases'] = [t for t in st.session_state.project_data['test_cases'] if t['id'] != test['id']]
                        st.rerun()
    else:
        st.info("No test cases added yet. Click 'Add Test Case' to get started!")

# ==================== PAGE: ISSUES TRACKER ====================
elif page == "🐛 Issues Tracker":
    st.title("🐛 Issues & Bug Tracker")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Track issues and bugs found during the upgrade")
    with col2:
        if st.button("➕ Report Issue"):
            st.session_state.show_add_issue = True
    
    st.markdown("---")
    
    # Add Issue
    if 'show_add_issue' in st.session_state and st.session_state.show_add_issue:
        with st.form("add_issue_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                issue_module = st.selectbox("Module", list(st.session_state.project_data['modules'].keys()), key="issue_module")
            with col2:
                issue_title = st.text_input("Issue Title")
            
            col1, col2 = st.columns(2)
            with col1:
                issue_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            with col2:
                issue_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed", "On Hold"])
            
            issue_description = st.text_area("Issue Description")
            issue_steps = st.text_area("Steps to Reproduce")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✓ Report Issue", use_container_width=True):
                    st.session_state.project_data['issues'].append({
                        'id': len(st.session_state.project_data['issues']) + 1,
                        'module': issue_module,
                        'title': issue_title,
                        'severity': issue_severity,
                        'status': issue_status,
                        'description': issue_description,
                        'steps': issue_steps,
                        'created_date': datetime.now().isoformat()
                    })
                    st.session_state.show_add_issue = False
                    st.success("Issue reported!")
            with col2:
                if st.form_submit_button("✗ Cancel", use_container_width=True):
                    st.session_state.show_add_issue = False
    
    st.markdown("---")
    
    # Issues List
    if st.session_state.project_data['issues']:
        st.subheader("Issues Summary")
        
        issues_data = []
        for issue in st.session_state.project_data['issues']:
            issues_data.append({
                'ID': issue['id'],
                'Module': issue['module'],
                'Title': issue['title'],
                'Severity': issue['severity'],
                'Status': issue['status']
            })
        
        df_issues = pd.DataFrame(issues_data)
        st.dataframe(df_issues, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Severity Summary
        st.subheader("Issue Severity Summary")
        
        severity_counts = {}
        for issue in st.session_state.project_data['issues']:
            severity = issue['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        col1, col2, col3, col4 = st.columns(4)
        colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴', 'Critical': '⚫'}
        
        for col, (severity, count) in zip([col1, col2, col3, col4], severity_counts.items()):
            with col:
                st.metric(f"{colors.get(severity, '')} {severity}", count)
        
        st.markdown("---")
        
        # Detailed View
        st.subheader("Issue Details")
        
        for issue in st.session_state.project_data['issues']:
            severity_color = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴', 'Critical': '⚫'}
            with st.expander(f"{severity_color.get(issue['severity'], '')} {issue['title']} - {issue['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Module:** {issue['module']}")
                    st.write(f"**Severity:** {issue['severity']}")
                with col2:
                    st.write(f"**Status:** {issue['status']}")
                    st.write(f"**Reported:** {issue['created_date'][:10]}")
                
                st.write(f"**Description:** {issue['description']}")
                st.write(f"**Steps to Reproduce:** {issue['steps']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_issue_{issue['id']}"):
                        st.info("Edit functionality coming soon")
                with col2:
                    if st.button("Delete", key=f"delete_issue_{issue['id']}"):
                        st.session_state.project_data['issues'] = [i for i in st.session_state.project_data['issues'] if i['id'] != issue['id']]
                        st.rerun()
    else:
        st.info("No issues reported yet. Click 'Report Issue' to get started!")

# ==================== PAGE: NOTES & DOCS ====================
elif page == "📝 Notes & Docs":
    st.title("📝 Notes & Documentation")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Add notes and documentation for the upgrade project")
    with col2:
        if st.button("➕ Add Note"):
            st.session_state.show_add_note = True
    
    st.markdown("---")
    
    # Add Note
    if 'show_add_note' in st.session_state and st.session_state.show_add_note:
        with st.form("add_note_form", clear_on_submit=True):
            note_title = st.text_input("Note Title")
            note_category = st.selectbox("Category", ["General", "Technical", "Process", "Risk", "Decision"])
            note_content = st.text_area("Note Content", height=150)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✓ Add Note", use_container_width=True):
                    st.session_state.project_data['notes'].append({
                        'id': len(st.session_state.project_data['notes']) + 1,
                        'title': note_title,
                        'category': note_category,
                        'content': note_content,
                        'created_date': datetime.now().isoformat()
                    })
                    st.session_state.show_add_note = False
                    st.success("Note added!")
            with col2:
                if st.form_submit_button("✗ Cancel", use_container_width=True):
                    st.session_state.show_add_note = False
    
    st.markdown("---")
    
    # Notes List
    if st.session_state.project_data['notes']:
        st.subheader("Notes")
        
        # Filter by category
        categories = list(set([note['category'] for note in st.session_state.project_data['notes']]))
        selected_category = st.multiselect("Filter by Category", categories, default=categories)
        
        filtered_notes = [note for note in st.session_state.project_data['notes'] if note['category'] in selected_category]
        
        for note in filtered_notes:
            category_emoji = {'General': '📌', 'Technical': '⚙️', 'Process': '📋', 'Risk': '⚠️', 'Decision': '✅'}
            with st.expander(f"{category_emoji.get(note['category'], '')} {note['title']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Category:** {note['category']}")
                with col2:
                    st.write(f"**Created:** {note['created_date'][:10]}")
                
                st.write(note['content'])
                
                if st.button("Delete", key=f"delete_note_{note['id']}"):
                    st.session_state.project_data['notes'] = [n for n in st.session_state.project_data['notes'] if n['id'] != note['id']]
                    st.rerun()
    else:
        st.info("No notes added yet. Click 'Add Note' to get started!")

# ==================== PAGE: IMPORT/EXPORT ====================
elif page == "📤 Import/Export":
    st.title("📤 Import / Export Project Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Export Project")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            json_data = export_to_json()
            st.download_button(
                label="📥 Export as JSON",
                data=json_data,
                file_name=f"vista_upgrade_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col_b:
            csv_data = export_to_csv()
            st.download_button(
                label="📥 Export as CSV",
                data=csv_data,
                file_name=f"vista_upgrade_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Export Summary Report
        st.subheader("📋 Export Summary Report")
        
        report = f"""
VISTA APP UPGRADE PROJECT REPORT
Version: {st.session_state.project_data['current_version']} → {st.session_state.project_data['target_version']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROJECT STATISTICS
==================
Total Modules: {stats['total_modules']}
Total Tasks: {stats['total_tasks']}
Completed Tasks: {stats['completed_tasks']}
Overall Progress: {stats['progress']:.1f}%

MODULE BREAKDOWN
================
"""
        for module_name, module_info in st.session_state.project_data['modules'].items():
            mod_stats = get_module_stats(module_info)
            report += f"\n{module_name}\n"
            report += f"  Status: {module_info['status']}\n"
            report += f"  Owner: {module_info.get('owner', 'N/A')}\n"
            report += f"  Progress: {mod_stats['progress']:.1f}% ({mod_stats['completed']}/{mod_stats['total']} tasks)\n"
        
        st.text_area("Summary Report", value=report, height=300)
        
        report_bytes = report.encode()
        st.download_button(
            label="📥 Export Summary Report",
            data=report_bytes,
            file_name=f"vista_upgrade_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📤 Import Project")
        
        uploaded_file = st.file_uploader("Choose a JSON file to import", type=['json'])
        
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                st.success("✓ File loaded successfully!")
                
                st.write("Preview of imported data:")
                st.json(imported_data)
                
                if st.button("✓ Import and Overwrite Current Project", use_container_width=True):
                    st.session_state.project_data = imported_data
                    st.success("Project imported successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
        
        st.markdown("---")
        st.subheader("📊 Data Summary")
        
        summary_data = {
            'Modules': len(st.session_state.project_data['modules']),
            'Total Tasks': stats['total_tasks'],
            'Test Cases': len(st.session_state.project_data['test_cases']),
            'Issues': len(st.session_state.project_data['issues']),
            'Notes': len(st.session_state.project_data['notes'])
        }
        
        for key, value in summary_data.items():
            st.metric(key, value)

# ==================== PAGE: ANALYTICS & REPORTS ====================
elif page == "📈 Analytics & Reports":
    st.title("📈 Analytics & Reports")
    
    # Timeline view
    st.subheader("📊 Module Timeline & Status")
    
    timeline_data = []
    for module_name, module_info in st.session_state.project_data['modules'].items():
        mod_stats = get_module_stats(module_info)
        timeline_data.append({
            'Module': module_name,
            'Status': module_info['status'],
            'Progress': mod_stats['progress']
        })
    
    df_timeline = pd.DataFrame(timeline_data)
    
    fig_timeline = px.bar(
        df_timeline,
        x='Module',
        y='Progress',
        color='Status',
        title='Module Progress by Status',
        height=400,
        labels={'Progress': 'Progress (%)'}
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown("---")
    
    # Test Coverage
    st.subheader("🧪 Test Coverage Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Test Cases", len(st.session_state.project_data['test_cases']))
    with col2:
        passed = sum(1 for t in st.session_state.project_data['test_cases'] if t['status'] == 'Passed')
        st.metric("Passed Tests", passed)
    with col3:
        failed = sum(1 for t in st.session_state.project_data['test_cases'] if t['status'] == 'Failed')
        st.metric("Failed Tests", failed)
    
    if st.session_state.project_data['test_cases']:
        test_by_status = {}
        for test in st.session_state.project_data['test_cases']:
            status = test['status']
            test_by_status[status] = test_by_status.get(status, 0) + 1
        
        fig_tests = px.pie(
            values=list(test_by_status.values()),
            names=list(test_by_status.keys()),
            title='Test Status Distribution',
            height=300
        )
        st.plotly_chart(fig_tests, use_container_width=True)
    
    st.markdown("---")
    
    # Issues Analysis
    st.subheader("🐛 Issues Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Issues", len(st.session_state.project_data['issues']))
    with col2:
        critical = sum(1 for i in st.session_state.project_data['issues'] if i['severity'] == 'Critical')
        st.metric("Critical", critical)
    with col3:
        high = sum(1 for i in st.session_state.project_data['issues'] if i['severity'] == 'High')
        st.metric("High", high)
    with col4:
        open_issues = sum(1 for i in st.session_state.project_data['issues'] if i['status'] == 'Open')
        st.metric("Open", open_issues)
    
    if st.session_state.project_data['issues']:
        issues_by_severity = {}
        for issue in st.session_state.project_data['issues']:
            severity = issue['severity']
            issues_by_severity[severity] = issues_by_severity.get(severity, 0) + 1
        
        fig_issues = px.pie(
            values=list(issues_by_severity.values()),
            names=list(issues_by_severity.keys()),
            title='Issues by Severity',
            height=300
        )
        st.plotly_chart(fig_issues, use_container_width=True)
    
    st.markdown("---")
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completed_modules = sum(1 for m in st.session_state.project_data['modules'].values() if m['status'] == 'Completed')
        st.metric("Completed Modules", f"{completed_modules}/{stats['total_modules']}")
    
    with col2:
        avg_progress = sum(get_module_stats(m)['progress'] for m in st.session_state.project_data['modules'].values()) / stats['total_modules']
        st.metric("Average Module Progress", f"{avg_progress:.1f}%")
    
    with col3:
        remaining_tasks = stats['total_tasks'] - stats['completed_tasks']
        st.metric("Remaining Tasks", remaining_tasks)

# ==================== FOOTER ====================
st.markdown("---")
st.caption(f"🚀 VISTA App Upgrade Portal | v{st.session_state.project_data['current_version']} → v{st.session_state.project_data['target_version']} | Created: {st.session_state.project_data['created_date'][:10]}")
