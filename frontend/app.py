import streamlit as st
import sys
import os
import pandas as pd
import json

backend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "backend")
)

sys.path.append(backend_path)

from auto_patch_engine import AutoPatchEngine
from ai_fix_generator import generate_fix
from commit_analyzer import analyze_repository
from sprint_summary import generate_summary
from release_notes import generate_release_notes
from risk_analyzer import get_risk_level
from jira_formatter import generate_jira_tasks
from github_commit_service import push_ai_fix_file
from github_pr_service import create_pull_request


# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="AI Engineering Productivity Platform",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Engineering Productivity Platform")
st.write("Analyze GitHub repositories using AI")


# ---------------- INPUTS ----------------
owner = st.text_input("GitHub Owner", "microsoft")
repo = st.text_input("Repository Name", "vscode")

repo_url = f"https://github.com/{owner}/{repo}"


# ---------------- SESSION STATE ----------------
if "results" not in st.session_state:
    st.session_state.results = []

if "pr_url" not in st.session_state:
    st.session_state.pr_url = None


# ---------------- ENGINE INIT (SAFE) ----------------
engine = None
if owner and repo:
    engine = AutoPatchEngine(repo_url)


# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Repository"):

    with st.spinner("Analyzing repository..."):

        st.session_state.results = analyze_repository(owner, repo)

        st.success(f"Found {len(st.session_state.results)} commits")


results = st.session_state.results


# ---------------- VARIABLES ----------------
commit_messages = []
analysis_data = []

high = 0
medium = 0
low = 0


# ---------------- ANALYSIS ----------------
if results:

    st.header("📊 Commit Analysis")

    for item in results:

        message = item.get("message", "")
        analysis = item.get("analysis", {})

        commit_messages.append(message)

        if isinstance(analysis, str):
            try:
                analysis = json.loads(analysis)
            except:
                analysis = {
                    "category": "Unknown",
                    "priority": "Low",
                    "risk_score": 0,
                    "summary": analysis
                }

        analysis_data.append(analysis)

        risk_score = analysis.get("risk_score", 0)
        risk = get_risk_level(risk_score)

        if risk == "High":
            high += 1
        elif risk == "Medium":
            medium += 1
        else:
            low += 1

        with st.expander(f"Commit: {message[:70]}..."):

            st.code(message)
            st.json(analysis)
            st.write("Risk:", risk)

            try:
                fix = generate_fix(message, analysis.get("summary", ""))
                st.subheader("🤖 AI Suggested Fix")
                st.json(fix)
            except Exception as e:
                st.warning(f"Fix generation failed: {e}")


# ---------------- DASHBOARD ----------------
if results:

    st.header("📈 Risk Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("🔴 High Risk", high)
    col2.metric("🟡 Medium Risk", medium)
    col3.metric("🟢 Low Risk", low)

    df = pd.DataFrame({
        "Risk Level": ["High", "Medium", "Low"],
        "Count": [high, medium, low]
    })

    st.bar_chart(df.set_index("Risk Level"))

    total = high + medium + low

    if total > 0:
        health = (low * 100 + medium * 60 + high * 20) / total
        st.metric("Health Score", f"{health:.1f}/100")


# ---------------- SPRINT SUMMARY ----------------
if results:

    st.header("📝 Sprint Summary")

    try:
        st.write(generate_summary(commit_messages))
    except:
        st.write(generate_summary(analysis_data))


# ---------------- RELEASE NOTES ----------------
if results:

    st.header("📋 Release Notes")

    try:
        st.write(generate_release_notes(commit_messages))
    except:
        st.write(generate_release_notes(analysis_data))


# ---------------- JIRA TASKS ----------------
if results:

    st.header("🧩 Jira Tasks")

    try:
        tasks = generate_jira_tasks(analysis_data)
        for t in tasks:
            st.json(t)
    except Exception as e:
        st.warning(f"Jira error: {e}")


# ---------------- AUTO FIX + PR ----------------
if results:

    st.header("🤖 Auto PR Bot")

    if st.button("Run AI Auto Fix + Create PR"):

        with st.spinner("Applying fixes + creating PR..."):

            try:
                fixes_applied = 0

                if engine is None:
                    st.error("Engine not initialized")
                    st.stop()

                for item in results:

                    message = item.get("message", "")
                    analysis = item.get("analysis", {})

                    fix = generate_fix(message, analysis.get("summary", ""))

                    # IMPORTANT: run_fix expects structured fix
                    if isinstance(fix, dict):
                        success = engine.run_fix(
                            fix,
                            message
                        )
                        if success:
                            fixes_applied += 1

                push_ai_fix_file("AI auto fixes applied")

                url = create_pull_request()

                st.session_state.pr_url = url

                st.success("PR Created Successfully!")
                st.write(url)

                st.info(f"Fixes applied: {fixes_applied}")

            except Exception as e:
                st.error(f"Auto fix failed: {e}")


# ---------------- SHOW PR ----------------
if st.session_state.pr_url:
    st.success("Latest PR:")
    st.write(st.session_state.pr_url)