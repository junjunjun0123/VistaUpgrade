import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="VISTA App Upgrade Portal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .progress-container {
        margin: 20px 0;
    }
    .module-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .stage-container {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'project_data' not in st.session_state:
    st.session_state.project_data = {
        'modules': {
            'Vista Head Office': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started'
            },
            'Vista Connect': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started'
            },
            'Vista Loyalty': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started'
            },
            'Vista Voucher': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started'
            },
            'Vista Cinema': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started'
            },
            'Vista Programming': {
                'stages': {'Planning': [], 'Testing': [], 'Development': []},
                'new_features': '',
                'bug_fixes': '',
                'status': 'Not Started'
            }
        },
        'created_date': datetime.now().isoformat(),
        'target_version': '5.0.18',
        'current_version': '5.0.13'
    }

def save_project_data():
    """Save project data to session state"""
    pass

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

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 VISTA App Upgrade Portal")
with col2:
    st.metric("", f"v{st.session_state.project_data['current_version']} → v{st.session_state.project_data['target_version']}")

st.markdown("---")

# Navigation
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Planning", "🔧 Module Details", "📈 Reports"])

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.header("Project Overview")
    
    # Summary Metrics
    stats = get_project_stats()
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
    st.subheader("Module Status Overview")
    
    module_data = []
    for module_name, module_info in st.session_state.project_data['modules'].items():
        stats = get_module_stats(module_info)
        module_data.append({
            'Module': module_name,
            'Status': module_info['status'],
            'Tasks': f"{stats['completed']}/{stats['total']}",
            'Progress': f"{stats['progress']:.0f}%"
        })
    
    df = pd.DataFrame(module_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== TAB 2: PLANNING ====================
with tab2:
    st.header("Project Planning & Execution")
    
    # Module selector
    selected_module = st.selectbox(
        "Select Module",
        list(st.session_state.project_data['modules'].keys())
    )
    
    module_data = st.session_state.project_data['modules'][selected_module]
    
    # Module status
    col1, col2, col3 = st.columns(3)
    stats = get_module_stats(module_data)
    
    with col1:
        new_status = st.selectbox(
            "Module Status",
            ["Not Started", "Planning", "In Progress", "Testing", "Completed"],
            index=["Not Started", "Planning", "In Progress", "Testing", "Completed"].index(module_data.get('status', 'Not Started')),
            key=f"status_{selected_module}"
        )
        module_data['status'] = new_status
    
    with col2:
        st.metric("Total Tasks", stats['total'])
    
    with col3:
        st.metric("Progress", f"{stats['progress']:.1f}%")
    
    st.progress(stats['progress'] / 100)
    
    st.markdown("---")
    
    # Planning stages
    st.subheader("Planning Stages")
    
    for stage in ['Planning', 'Testing', 'Development']:
        st.write(f"### {stage}")
        
        # Display existing tasks
        tasks = module_data['stages'][stage]
        for idx, task in enumerate(tasks):
            col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
            
            with col1:
                task_completed = st.checkbox(
                    "Done",
                    value=task.get('completed', False),
                    key=f"task_{selected_module}_{stage}_{idx}"
                )
                task['completed'] = task_completed
            
            with col2:
                st.write(f"**{task['name']}**")
            
            with col3:
                if st.button("🗑️", key=f"delete_{selected_module}_{stage}_{idx}"):
                    module_data['stages'][stage].pop(idx)
                    st.rerun()
        
        # Add new task
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            new_task = st.text_input(
                f"Add new {stage} task",
                key=f"new_task_{selected_module}_{stage}",
                placeholder=f"Enter a new {stage} task..."
            )
        with col2:
            if st.button("Add", key=f"add_task_{selected_module}_{stage}"):
                if new_task.strip():
                    module_data['stages'][stage].append({
                        'name': new_task.strip(),
                        'completed': False
                    })
                    st.rerun()
        
        st.markdown("---")
    
    # New Features and Bug Fixes
    st.subheader("Additional Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**✨ New Features**")
        module_data['new_features'] = st.text_area(
            "New Features for this module",
            value=module_data.get('new_features', ''),
            key=f"features_{selected_module}",
            height=150
        )
    
    with col2:
        st.write("**🐛 Bug Fixes**")
        module_data['bug_fixes'] = st.text_area(
            "Bug Fixes for this module",
            value=module_data.get('bug_fixes', ''),
            key=f"bugs_{selected_module}",
            height=150
        )

# ==================== TAB 3: MODULE DETAILS ====================
with tab3:
    st.header("Detailed Module Information")
    
    # Create a grid of modules
    col1, col2 = st.columns(2)
    
    modules = list(st.session_state.project_data['modules'].items())
    
    for idx, (module_name, module_info) in enumerate(modules):
        column = col1 if idx % 2 == 0 else col2
        
        with column:
            with st.container(border=True):
                st.subheader(module_name)
                
                stats = get_module_stats(module_info)
                
                # Status badge
                status_colors = {
                    'Not Started': '🔴',
                    'Planning': '🟡',
                    'In Progress': '🔵',
                    'Testing': '🟣',
                    'Completed': '🟢'
                }
                st.write(f"**Status:** {status_colors.get(module_info['status'], '⚪')} {module_info['status']}")
                
                # Progress
                st.write(f"**Progress:** {stats['completed']}/{stats['total']} tasks ({stats['progress']:.0f}%)")
                st.progress(stats['progress'] / 100)
                
                # Stages summary
                st.write("**Stages:**")
                for stage in ['Planning', 'Testing', 'Development']:
                    stage_tasks = module_info['stages'][stage]
                    completed = sum(1 for t in stage_tasks if t.get('completed', False))
                    st.caption(f"  {stage}: {completed}/{len(stage_tasks)} ✓")
                
                # New Features
                if module_info.get('new_features'):
                    st.write("**✨ New Features:**")
                    st.caption(module_info['new_features'][:100] + "..." if len(module_info['new_features']) > 100 else module_info['new_features'])
                
                # Bug Fixes
                if module_info.get('bug_fixes'):
                    st.write("**🐛 Bug Fixes:**")
                    st.caption(module_info['bug_fixes'][:100] + "..." if len(module_info['bug_fixes']) > 100 else module_info['bug_fixes'])

# ==================== TAB 4: REPORTS ====================
with tab4:
    st.header("Project Reports & Analytics")
    
    # Timeline view
    st.subheader("Module Timeline")
    
    timeline_data = []
    for module_name, module_info in st.session_state.project_data['modules'].items():
        stats = get_module_stats(module_info)
        timeline_data.append({
            'Module': module_name,
            'Status': module_info['status'],
            'Progress': stats['progress']
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
    
    # Summary statistics
    st.subheader("Summary Statistics")
    
    stats = get_project_stats()
    
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
    
    st.markdown("---")
    
    # Export data
    st.subheader("Export Project Data")
    
    # Export as JSON
    json_data = json.dumps(st.session_state.project_data, indent=2, default=str)
    st.download_button(
        label="📥 Download as JSON",
        data=json_data,
        file_name=f"vista_upgrade_plan_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
    
    # Export as CSV
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
    csv = df_export.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"vista_upgrade_tasks_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.caption(f"VISTA App Upgrade Portal | Version {st.session_state.project_data['current_version']} → {st.session_state.project_data['target_version']}")
