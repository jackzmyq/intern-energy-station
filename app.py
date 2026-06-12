import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="实习能量站",
    page_icon="HR",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = [
    "name",
    "role",
    "school",
    "major",
    "mentor",
    "stage",
    "task_completion",
    "job_skill",
    "initiative",
    "collaboration",
    "mentor_score",
    "feedback_status",
    "last_feedback_days",
    "career_goal",
    "mentor_feedback",
]

NUMERIC_COLUMNS = [
    "task_completion",
    "job_skill",
    "initiative",
    "collaboration",
    "mentor_score",
    "last_feedback_days",
]

OPTIONAL_NUMERIC_COLUMNS = ["week", "satisfaction", "weekly_change"]

PAGES = ["home", "list", "profile", "mentor", "trend", "hr"]
PAGE_LABELS = {
    "zh": {
        "home": "首页总览",
        "list": "实习生列表",
        "profile": "个人详情",
        "mentor": "导师工作台",
        "trend": "成长趋势",
        "hr": "HR 分析看板",
    },
    "en": {
        "home": "Overview",
        "list": "Intern List",
        "profile": "Profile",
        "mentor": "Mentor Workspace",
        "trend": "Growth Trends",
        "hr": "HR Analytics",
    },
}

TEXT = {
    "zh": {
        "app_title": "实习能量站",
        "subtitle": "用适岗指数、风险预警和 AI 建议，把实习培养从经验驱动变成数据驱动。",
        "sidebar_caption": "业务部实习生成长导航 AI 看板",
        "upload": "上传实习生 CSV 数据",
        "upload_help": "字段结构可参考项目里的 interns.csv。上传后看板会自动改用你的数据。",
        "download_template": "下载数据模板",
        "choose_page": "选择页面",
        "role_filter": "岗位筛选",
        "risk_filter": "风险等级筛选",
        "data_source": "当前数据源：{source}，共 {count} 名实习生。",
        "sample_data": "示例数据",
        "uploaded_data": "上传数据",
        "empty": "当前筛选条件下没有实习生数据。请在左侧至少选择一个岗位和一个风险等级。",
        "total": "实习生总数",
        "avg_fit": "平均适岗指数",
        "high_potential_count": "高潜人数",
        "risk_count": "风险人数",
        "feedback_rate": "导师反馈完成率",
        "overall_status": "整体状态",
        "role_avg_title": "各岗位平均适岗指数",
        "risk_dist_title": "风险等级分布",
        "weekly_summary": "AI 本周管理摘要",
        "watchlist": "重点关注名单",
        "intern_table": "实习生状态表",
        "select_intern_hr": "选择一位实习生生成 HR 跟进建议",
        "current_status": "{name} 当前状态：",
        "generate_hr": "生成 HR 跟进建议",
        "select_intern": "选择实习生",
        "role": "岗位",
        "stage": "当前阶段",
        "fit_score": "适岗指数",
        "risk_level": "风险等级",
        "basic_info": "个人基础信息",
        "basic_info_text": "{name}，来自 {school} {major}，导师为 {mentor}，职业目标是：{goal}。",
        "growth_path": "30/60/90 天成长路径",
        "radar": "能力雷达",
        "feedback_ai": "导师反馈与 AI 总结",
        "raw_feedback": "导师原始反馈：{feedback}",
        "mentor_todo": "导师本周待办",
        "select_mentor": "选择导师",
        "mentee_count": "带教人数",
        "todo_count": "待处理事项",
        "feedback_timely": "反馈及时率",
        "feedback_generator": "AI 反馈生成器",
        "select_feedback_intern": "选择要生成反馈的实习生",
        "weekly_note": "本周观察补充",
        "generate_feedback": "生成结构化导师反馈",
        "supplement": "可补充记录：",
        "mentor_template": "标准带教模板",
        "role_analysis": "岗位维度分析",
        "scatter_title": "任务完成率与适岗指数关系",
        "conversion_title": "转正潜力分布",
        "high_and_risk": "高潜人才与风险人才",
        "high_potential": "高潜人才",
        "risky_talent": "风险人才",
        "ai_report": "AI 周报",
        "upload_error": "请下载左侧数据模板，按相同字段填写后重新上传。",
        "trend_title": "成长趋势分析",
        "fit_trend_title": "周度平均适岗指数趋势",
        "role_trend_title": "各岗位周度适岗指数趋势",
        "satisfaction_title": "满意度与适岗指数关系",
        "risk_reason_title": "风险原因拆解",
        "risk_reason_hint": "系统会把风险拆成任务滞后、导师反馈延迟、主动性不足、协作偏低和适岗下滑，帮助 HR 判断该先介入哪里。",
        "export_report": "下载 HR 周报",
        "ai_mode": "AI 模式",
        "rule_mode": "规则引擎模式",
        "llm_mode": "大模型模式（未来扩展，不调用 API）",
        "ai_mode_note": "当前使用{mode}：版本 A 不接真实 AI API，使用规则引擎自动生成建议；正式落地可接入腾讯混元 / 元宝。",
    },
    "en": {
        "app_title": "Intern Energy Station",
        "subtitle": "A data-driven AI dashboard for intern growth, risk alerts, and HR follow-up.",
        "sidebar_caption": "AI Growth Navigation Dashboard",
        "upload": "Upload intern CSV",
        "upload_help": "Use interns.csv as the field template. Uploaded data will replace the sample dataset.",
        "download_template": "Download template",
        "choose_page": "Page",
        "role_filter": "Role filter",
        "risk_filter": "Risk filter",
        "data_source": "Data source: {source}. Total interns: {count}.",
        "sample_data": "Sample data",
        "uploaded_data": "Uploaded data",
        "empty": "No interns match the current filters. Select at least one role and one risk level on the left.",
        "total": "Total interns",
        "avg_fit": "Avg fit score",
        "high_potential_count": "High potential",
        "risk_count": "At risk",
        "feedback_rate": "Feedback completion",
        "overall_status": "Overall Status",
        "role_avg_title": "Average Fit Score by Role",
        "risk_dist_title": "Risk Level Distribution",
        "weekly_summary": "AI Weekly Summary",
        "watchlist": "Watchlist",
        "intern_table": "Intern Status Table",
        "select_intern_hr": "Select an intern for HR follow-up advice",
        "current_status": "{name} status: ",
        "generate_hr": "Generate HR Advice",
        "select_intern": "Select intern",
        "role": "Role",
        "stage": "Stage",
        "fit_score": "Fit score",
        "risk_level": "Risk level",
        "basic_info": "Basic Info",
        "basic_info_text": "{name} is from {school}, majoring in {major}. Mentor: {mentor}. Career goal: {goal}.",
        "growth_path": "30/60/90-Day Growth Path",
        "radar": "Capability Radar",
        "feedback_ai": "Mentor Feedback and AI Summary",
        "raw_feedback": "Original mentor feedback: {feedback}",
        "mentor_todo": "Mentor Weekly Tasks",
        "select_mentor": "Select mentor",
        "mentee_count": "Mentees",
        "todo_count": "Open actions",
        "feedback_timely": "Timely feedback",
        "feedback_generator": "AI Feedback Generator",
        "select_feedback_intern": "Select intern for feedback",
        "weekly_note": "Additional weekly notes",
        "generate_feedback": "Generate Structured Feedback",
        "supplement": "Additional note:",
        "mentor_template": "Standard Mentoring Template",
        "role_analysis": "Role-Level Analysis",
        "scatter_title": "Task Completion vs Fit Score",
        "conversion_title": "Conversion Potential Distribution",
        "high_and_risk": "High-Potential and Risk Talent",
        "high_potential": "High potential",
        "risky_talent": "At-risk talent",
        "ai_report": "AI Weekly Report",
        "upload_error": "Download the template on the left, keep the same fields, and upload again.",
        "trend_title": "Growth Trend Analysis",
        "fit_trend_title": "Weekly Average Fit Score Trend",
        "role_trend_title": "Weekly Fit Score Trend by Role",
        "satisfaction_title": "Satisfaction vs Fit Score",
        "risk_reason_title": "Risk Driver Breakdown",
        "risk_reason_hint": "The dashboard breaks risk into task delay, delayed mentor feedback, low initiative, weak collaboration, and declining fit score.",
        "export_report": "Download HR Report",
        "ai_mode": "AI mode",
        "rule_mode": "Rule engine mode",
        "llm_mode": "LLM mode (future extension, no API call)",
        "ai_mode_note": "Current mode: {mode}. Version A does not call a real AI API; it uses a rule engine now and can connect to Tencent Hunyuan / Yuanbao later.",
    },
}

COLUMN_LABELS = {
    "zh": {
        "name": "姓名",
        "role": "岗位",
        "school": "学校",
        "major": "专业",
        "mentor": "导师",
        "stage": "阶段",
        "task_completion": "任务完成率",
        "job_skill": "岗位技能",
        "initiative": "学习主动性",
        "collaboration": "沟通协作",
        "mentor_score": "导师评分",
        "fit_score": "适岗指数",
        "risk_level": "风险等级",
        "conversion_potential": "转正潜力",
        "feedback_status": "反馈状态",
        "last_feedback_days": "距上次反馈天数",
        "mentor_feedback": "导师反馈",
        "feedback_status": "反馈状态",
    },
    "en": {
        "name": "Name",
        "role": "Role",
        "school": "School",
        "major": "Major",
        "mentor": "Mentor",
        "stage": "Stage",
        "task_completion": "Task completion",
        "job_skill": "Job skill",
        "initiative": "Initiative",
        "collaboration": "Collaboration",
        "mentor_score": "Mentor score",
        "fit_score": "Fit score",
        "risk_level": "Risk level",
        "conversion_potential": "Conversion potential",
        "feedback_status": "Feedback status",
        "last_feedback_days": "Days since feedback",
        "mentor_feedback": "Mentor feedback",
    },
}

RISK_LEVELS = ["高潜", "健康成长", "需要关注", "高风险"]
RISK_LABELS = {
    "zh": {
        "高潜": "高潜",
        "健康成长": "健康成长",
        "需要关注": "需要关注",
        "高风险": "高风险",
    },
    "en": {
        "高潜": "High potential",
        "健康成长": "Healthy",
        "需要关注": "Needs attention",
        "高风险": "High risk",
    },
}


def tr(key: str, lang: str, **kwargs) -> str:
    value = TEXT[lang].get(key, key)
    return value.format(**kwargs) if kwargs else value


def localize_columns(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    return df.rename(columns=COLUMN_LABELS[lang])


def read_csv_safely(source) -> pd.DataFrame:
    try:
        return pd.read_csv(source, encoding="utf-8-sig")
    except UnicodeDecodeError:
        if hasattr(source, "seek"):
            source.seek(0)
        return pd.read_csv(source, encoding="gbk")


def classify_risk(score: float) -> str:
    if score >= 85:
        return "高潜"
    if score >= 70:
        return "健康成长"
    if score >= 55:
        return "需要关注"
    return "高风险"


def classify_conversion(row: pd.Series) -> str:
    if row["fit_score"] >= 88 and row["task_completion"] >= 88 and row["mentor_score"] >= 88:
        return "强推荐转正"
    if row["fit_score"] >= 75:
        return "可转正但需补强"
    if row["fit_score"] >= 60:
        return "暂缓观察"
    return "不建议转正"


def load_data(uploaded_file=None) -> pd.DataFrame:
    df = read_csv_safely(uploaded_file if uploaded_file is not None else "interns.csv")
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError("上传文件缺少这些字段：" + "、".join(missing))

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in OPTIONAL_NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[NUMERIC_COLUMNS].isna().any().any():
        bad_cols = df[NUMERIC_COLUMNS].columns[df[NUMERIC_COLUMNS].isna().any()].tolist()
        raise ValueError("这些数字字段存在空值或非数字内容：" + "、".join(bad_cols))

    if "week" not in df.columns or df["week"].isna().any():
        df["week"] = (df.index % 12) + 1
    if "satisfaction" not in df.columns or df["satisfaction"].isna().any():
        df["satisfaction"] = (
            df["mentor_score"] * 0.45 + df["initiative"] * 0.30 + df["collaboration"] * 0.25
        ).round(0)
    if "weekly_change" not in df.columns or df["weekly_change"].isna().any():
        df["weekly_change"] = 0

    df["fit_score"] = (
        df["task_completion"] * 0.30
        + df["job_skill"] * 0.25
        + df["mentor_score"] * 0.20
        + df["initiative"] * 0.15
        + df["collaboration"] * 0.10
    ).round(1)
    df["risk_level"] = df["fit_score"].apply(classify_risk)
    df["conversion_potential"] = df.apply(classify_conversion, axis=1)
    return df


def risk_color(level: str) -> str:
    return {
        "高潜": "green",
        "健康成长": "blue",
        "需要关注": "orange",
        "高风险": "red",
    }.get(level, "gray")


def ai_student_advice(row: pd.Series, lang: str) -> str:
    if lang == "en":
        reasons = []
        actions = []
        if row["task_completion"] < 60:
            reasons.append("task completion is below 60%, so the intern is behind the expected pace")
            actions.append("split next week's work into 2-3 concrete deliverables and check progress mid-week")
        if row["last_feedback_days"] >= 10:
            reasons.append("mentor feedback has not been updated for more than 10 days")
            actions.append("ask the mentor to provide feedback and schedule a 30-minute 1:1")
        if row["initiative"] < 60:
            reasons.append("initiative is low, which may indicate unclear goals or adjustment pressure")
            actions.append("ask the intern to submit a weekly issue list and confirm priorities with the mentor")
        if row["collaboration"] < 65:
            reasons.append("collaboration score is low, so cross-role communication may be insufficient")
            actions.append("run a project sync rehearsal and require a short communication outline")
        if not reasons:
            reasons.append("the current growth status is stable with no obvious risk signal")
            actions.append("increase task difficulty and assign a small real-business deliverable")
        return (
            f"AI diagnosis: {row['name']} is currently in "
            f"'{RISK_LABELS['en'][row['risk_level']]}' status. "
            f"{'; '.join(reasons)}. Recommendation: {'; '.join(actions)}."
        )

    reasons = []
    actions = []
    if row["task_completion"] < 60:
        reasons.append("任务完成率低于 60%，成长节奏已经落后于当前阶段")
        actions.append("将本周任务拆成 2-3 个可交付小目标，并在周中安排一次进度确认")
    if row["last_feedback_days"] >= 10:
        reasons.append("导师反馈超过 10 天未更新，带教节奏存在断点")
        actions.append("HR 提醒导师完成反馈，并建议安排一次 30 分钟 1v1")
    if row["initiative"] < 60:
        reasons.append("学习主动性评分偏低，可能存在目标不清或适应压力")
        actions.append("让实习生提交一份本周问题清单，导师帮助排序并确认优先级")
    if row["collaboration"] < 65:
        reasons.append("沟通协作评分偏低，跨角色同步可能不足")
        actions.append("下周安排一次需求或项目同步演练，要求提前准备沟通提纲")
    if not reasons:
        reasons.append("当前成长状态稳定，核心指标没有明显风险信号")
        actions.append("继续提高任务挑战度，安排一个更接近真实业务的小型交付")
    return (
        f"AI 诊断：{row['name']}当前处于「{row['risk_level']}」状态。"
        f"{'；'.join(reasons)}。建议：{'；'.join(actions)}。"
    )


def ai_mentor_feedback(row: pd.Series, lang: str) -> str:
    if lang == "en":
        strength = "is progressing steadily" if row["fit_score"] >= 70 else "is still adapting to the role"
        focus = []
        if row["job_skill"] < 70:
            focus.append("job skills")
        if row["initiative"] < 70:
            focus.append("initiative")
        if row["collaboration"] < 70:
            focus.append("collaboration")
        if not focus:
            focus.append("a more challenging independent deliverable")
        return (
            f"{row['name']} {strength}. The current fit score for {row['role']} is {row['fit_score']}. "
            f"Next week, focus on {', '.join(focus)}. The mentor can arrange a concrete case review "
            f"to help turn learning into deliverable output."
        )

    strength = "能够保持稳定推进" if row["fit_score"] >= 70 else "目前还在适应岗位节奏"
    focus = []
    if row["job_skill"] < 70:
        focus.append("岗位技能")
    if row["initiative"] < 70:
        focus.append("学习主动性")
    if row["collaboration"] < 70:
        focus.append("沟通协作")
    if not focus:
        focus.append("更高难度的独立交付")
    return (
        f"{row['name']}本周{strength}，在「{row['role']}」的阶段任务中适岗指数为 {row['fit_score']}。"
        f"下周建议重点关注{'、'.join(focus)}，导师可安排一次具体案例复盘，帮助其把学习成果转化为可交付产出。"
    )


def ai_weekly_report(df: pd.DataFrame, lang: str) -> str:
    risky = df[df["risk_level"].isin(["需要关注", "高风险"])].sort_values("fit_score")
    high = df[df["risk_level"] == "高潜"].sort_values("fit_score", ascending=False)
    weakest_role = df.groupby("role")["fit_score"].mean().sort_values().index[0]
    names = "、".join(risky["name"].head(3).tolist()) if len(risky) else "暂无"
    if lang == "en":
        names_en = ", ".join(risky["name"].head(3).tolist()) if len(risky) else "none"
        return (
            f"This week, {len(df)} interns have an average fit score of {df['fit_score'].mean():.1f}. "
            f"There are {len(high)} high-potential interns and {len(risky)} interns needing attention or at high risk. "
            f"HR should follow up with {names_en}. By role, {weakest_role} has the lowest average fit score, "
            f"so the task design and mentor feedback cadence should be reviewed."
        )
    return (
        f"本周 {len(df)} 名实习生平均适岗指数为 {df['fit_score'].mean():.1f}。"
        f"高潜实习生 {len(high)} 人，建议优先进入重点培养池；"
        f"需要关注或高风险实习生 {len(risky)} 人，其中 {names} 需要 HR 与导师跟进。"
        f"岗位维度看，{weakest_role}平均适岗指数相对较低，建议复盘该岗位的任务设计与导师反馈频率。"
    )


def risk_reason_flags(row: pd.Series, lang: str) -> list[str]:
    if lang == "en":
        labels = {
            "task": "Task delay",
            "feedback": "Delayed mentor feedback",
            "initiative": "Low initiative",
            "collaboration": "Weak collaboration",
            "decline": "Fit score decline",
        }
    else:
        labels = {
            "task": "任务滞后",
            "feedback": "导师反馈延迟",
            "initiative": "主动性不足",
            "collaboration": "协作偏低",
            "decline": "适岗下滑",
        }

    reasons = []
    if row["task_completion"] < 60:
        reasons.append(labels["task"])
    if row["last_feedback_days"] >= 10:
        reasons.append(labels["feedback"])
    if row["initiative"] < 60:
        reasons.append(labels["initiative"])
    if row["collaboration"] < 65:
        reasons.append(labels["collaboration"])
    if row["weekly_change"] <= -10:
        reasons.append(labels["decline"])
    if not reasons:
        reasons.append("No major risk driver" if lang == "en" else "暂无明显风险")
    return reasons


def risk_reason_table(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        if row["risk_level"] not in ["需要关注", "高风险"]:
            continue
        for reason in risk_reason_flags(row, lang):
            if reason not in ["暂无明显风险", "No major risk driver"]:
                rows.append({"reason": reason, "count": 1})
    if not rows:
        return pd.DataFrame({"reason": [], "count": []})
    return pd.DataFrame(rows).groupby("reason", as_index=False)["count"].sum().sort_values("count", ascending=False)


def build_markdown_report(df: pd.DataFrame, lang: str) -> str:
    risky = df[df["risk_level"].isin(["需要关注", "高风险"])].sort_values("fit_score")
    high = df[df["risk_level"] == "高潜"].sort_values("fit_score", ascending=False)
    role_summary = df.groupby("role")["fit_score"].mean().round(1).sort_values(ascending=False)
    risk_reasons = risk_reason_table(df, lang)

    if lang == "en":
        lines = [
            "# Intern Energy Station Weekly HR Report",
            "",
            ai_weekly_report(df, lang),
            "",
            "## KPI Snapshot",
            f"- Total interns: {len(df)}",
            f"- Average fit score: {df['fit_score'].mean():.1f}",
            f"- High-potential interns: {len(high)}",
            f"- At-risk interns: {len(risky)}",
            f"- Feedback completion rate: {(df['feedback_status'] == '已反馈').mean() * 100:.0f}%",
            "",
            "## Role Average Fit Score",
        ]
        lines += [f"- {role}: {score}" for role, score in role_summary.items()]
        lines += ["", "## Priority Follow-up"]
        lines += [f"- {row['name']} ({row['role']}): {row['fit_score']} / {RISK_LABELS['en'][row['risk_level']]}" for _, row in risky.head(5).iterrows()]
        lines += ["", "## Risk Drivers"]
        lines += [f"- {row['reason']}: {row['count']}" for _, row in risk_reasons.iterrows()] if len(risk_reasons) else ["- No major risk driver."]
        return "\n".join(lines)

    lines = [
        "# 实习能量站 HR 周报",
        "",
        ai_weekly_report(df, lang),
        "",
        "## 核心指标",
        f"- 实习生总数：{len(df)}",
        f"- 平均适岗指数：{df['fit_score'].mean():.1f}",
        f"- 高潜人数：{len(high)}",
        f"- 风险人数：{len(risky)}",
        f"- 导师反馈完成率：{(df['feedback_status'] == '已反馈').mean() * 100:.0f}%",
        "",
        "## 岗位平均适岗指数",
    ]
    lines += [f"- {role}：{score}" for role, score in role_summary.items()]
    lines += ["", "## 优先跟进名单"]
    lines += [f"- {row['name']}（{row['role']}）：{row['fit_score']} / {row['risk_level']}" for _, row in risky.head(5).iterrows()]
    lines += ["", "## 风险原因拆解"]
    lines += [f"- {row['reason']}：{row['count']}" for _, row in risk_reasons.iterrows()] if len(risk_reasons) else ["- 暂无明显风险原因。"]
    return "\n".join(lines)


def radar_chart(row: pd.Series, lang: str) -> go.Figure:
    labels = (
        ["岗位技能", "学习主动性", "沟通协作", "问题解决", "业务理解"]
        if lang == "zh"
        else ["Job skill", "Initiative", "Collaboration", "Problem solving", "Business understanding"]
    )
    values = [
        row["job_skill"],
        row["initiative"],
        row["collaboration"],
        round((row["job_skill"] * 0.55 + row["task_completion"] * 0.45), 1),
        round((row["mentor_score"] * 0.5 + row["collaboration"] * 0.5), 1),
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=row["name"],
            line_color="#2563eb",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def path_for_role(role: str, lang: str) -> pd.DataFrame:
    mapping_zh = {
        "研发岗": [
            ("30 天", "熟悉代码规范、开发环境、需求评审流程", "完成一个小缺陷修复或工具链配置"),
            ("60 天", "参与模块开发、联调测试、异常场景分析", "独立交付一个小功能并通过评审"),
            ("90 天", "承担小模块、复盘性能或稳定性问题", "输出技术复盘并支持转正评估"),
        ],
        "产品岗": [
            ("30 天", "理解业务、用户场景、竞品分析方法", "完成竞品分析和用户访谈纪要"),
            ("60 天", "输出需求文档、参与需求评审、跟进数据反馈", "独立完成一版 PRD 并复盘指标"),
            ("90 天", "承担小需求闭环、沉淀产品判断依据", "完成从需求到复盘的小项目"),
        ],
        "销售岗": [
            ("30 天", "熟悉产品卖点、客户画像、基础话术", "完成客户画像和话术演练"),
            ("60 天", "参与商机跟进、客户异议处理、行业案例整理", "完成一次模拟客户方案汇报"),
            ("90 天", "独立跟进低风险商机、沉淀复盘方法", "输出客户跟进复盘和转化建议"),
        ],
    }
    mapping_en = {
        "研发岗": [
            ("30 days", "Learn coding standards, dev environment, and review process", "Fix a small defect or complete tool setup"),
            ("60 days", "Join module development, integration testing, and exception analysis", "Deliver a small feature through review"),
            ("90 days", "Own a small module and review performance or stability issues", "Submit a technical review for conversion evaluation"),
        ],
        "产品岗": [
            ("30 days", "Understand business context, user scenarios, and competitor analysis", "Complete competitor analysis and interview notes"),
            ("60 days", "Write PRDs, join reviews, and track data feedback", "Deliver one PRD and review key metrics"),
            ("90 days", "Own a small product requirement and build judgment evidence", "Complete a small requirement-to-review project"),
        ],
        "销售岗": [
            ("30 days", "Learn product value, customer profiles, and basic pitch scripts", "Complete customer profiles and pitch practice"),
            ("60 days", "Join opportunity follow-up, objection handling, and case collection", "Complete one simulated customer proposal"),
            ("90 days", "Independently follow up low-risk opportunities and summarize learnings", "Submit a customer follow-up review and conversion suggestions"),
        ],
    }
    columns = ["阶段", "能力目标", "交付成果"] if lang == "zh" else ["Stage", "Capability Goal", "Deliverable"]
    return pd.DataFrame((mapping_zh if lang == "zh" else mapping_en)[role], columns=columns)


header_left, header_right = st.columns([0.74, 0.26])
with header_right:
    lang_label = st.selectbox(
        "Language",
        ["中文", "English"],
        index=0,
        label_visibility="collapsed",
    )
lang = "zh" if lang_label == "中文" else "en"
with header_right:
    ai_mode = st.selectbox(
        tr("ai_mode", lang),
        [tr("rule_mode", lang), tr("llm_mode", lang)],
        label_visibility="collapsed",
    )

with header_left:
    st.title(tr("app_title", lang))
    st.caption(tr("subtitle", lang))
    st.caption(tr("ai_mode_note", lang, mode=ai_mode))

st.sidebar.title(tr("app_title", lang))
st.sidebar.caption(tr("sidebar_caption", lang))

uploaded_file = st.sidebar.file_uploader(
    tr("upload", lang),
    type=["csv"],
    help=tr("upload_help", lang),
)

template_csv = pd.read_csv("interns.csv", encoding="utf-8-sig").to_csv(index=False, encoding="utf-8-sig")
template_bytes = template_csv.encode("utf-8-sig")
st.sidebar.download_button(
    tr("download_template", lang),
    template_bytes,
    file_name="interns_template.csv",
    mime="text/csv; charset=utf-8-sig",
)

try:
    df = load_data(uploaded_file)
except Exception as exc:
    st.error(str(exc))
    st.info(tr("upload_error", lang))
    st.stop()

data_source = tr("uploaded_data", lang) if uploaded_file is not None else tr("sample_data", lang)

page = st.sidebar.radio(
    tr("choose_page", lang),
    PAGES,
    format_func=lambda key: PAGE_LABELS[lang][key],
)

role_filter = st.sidebar.multiselect(
    tr("role_filter", lang),
    options=sorted(df["role"].unique()),
    default=sorted(df["role"].unique()),
)
risk_filter = st.sidebar.multiselect(
    tr("risk_filter", lang),
    options=RISK_LEVELS,
    default=RISK_LEVELS,
    format_func=lambda key: RISK_LABELS[lang][key],
)
filtered = df[df["role"].isin(role_filter) & df["risk_level"].isin(risk_filter)]

st.caption(tr("data_source", lang, source=data_source, count=len(df)))

if filtered.empty:
    st.warning(tr("empty", lang))
    st.stop()

if page == "home":
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(tr("total", lang), f"{len(filtered)}")
    with col2:
        st.metric(tr("avg_fit", lang), f"{filtered['fit_score'].mean():.1f}")
    with col3:
        st.metric(tr("high_potential_count", lang), f"{(filtered['risk_level'] == '高潜').sum()}")
    with col4:
        st.metric(tr("risk_count", lang), f"{filtered['risk_level'].isin(['需要关注', '高风险']).sum()}")
    with col5:
        feedback_rate = (filtered["feedback_status"] == "已反馈").mean() * 100
        st.metric(tr("feedback_rate", lang), f"{feedback_rate:.0f}%")

    st.subheader(tr("overall_status", lang))
    left, right = st.columns([1.2, 1])
    with left:
        role_avg = filtered.groupby("role", as_index=False)["fit_score"].mean()
        fig = px.bar(
            role_avg,
            x="role",
            y="fit_score",
            color="role",
            text=role_avg["fit_score"].round(1),
            title=tr("role_avg_title", lang),
            color_discrete_sequence=["#2563eb", "#0f766e", "#b45309"],
        )
        fig.update_layout(showlegend=False, yaxis_range=[0, 100], height=380)
        st.plotly_chart(fig, width="stretch")
    with right:
        risk_counts = filtered["risk_level"].value_counts().reindex(RISK_LEVELS, fill_value=0)
        fig = px.pie(
            names=[RISK_LABELS[lang][key] for key in risk_counts.index],
            values=risk_counts.values,
            title=tr("risk_dist_title", lang),
            color=risk_counts.index,
            color_discrete_map={
                "高潜": "#147a4d",
                "健康成长": "#2563eb",
                "需要关注": "#b45309",
                "高风险": "#b91c1c",
            },
        )
        fig.update_layout(height=380)
        st.plotly_chart(fig, width="stretch")

    st.subheader(tr("weekly_summary", lang))
    st.info(ai_weekly_report(filtered, lang))
    st.download_button(
        tr("export_report", lang),
        build_markdown_report(filtered, lang).encode("utf-8-sig"),
        file_name="intern_energy_hr_report.md",
        mime="text/markdown",
    )

    st.subheader(tr("watchlist", lang))
    watch = filtered[filtered["risk_level"].isin(["需要关注", "高风险"])].sort_values("fit_score")
    st.dataframe(
        localize_columns(
            watch[["name", "role", "stage", "task_completion", "fit_score", "risk_level", "last_feedback_days"]],
            lang,
        ),
        width="stretch",
        hide_index=True,
    )

elif page == "list":
    st.subheader(tr("intern_table", lang))
    display = filtered.sort_values("fit_score", ascending=False)[
        [
            "name",
            "role",
            "school",
            "major",
            "stage",
            "task_completion",
            "job_skill",
            "initiative",
            "collaboration",
            "mentor_score",
            "fit_score",
            "risk_level",
            "conversion_potential",
            "feedback_status",
        ]
    ]
    st.dataframe(localize_columns(display, lang), width="stretch", hide_index=True)

    selected_name = st.selectbox(tr("select_intern_hr", lang), filtered["name"].tolist())
    row = filtered[filtered["name"] == selected_name].iloc[0]
    status_label = RISK_LABELS[lang][row["risk_level"]]
    st.markdown(
        f"**{tr('current_status', lang, name=selected_name)}** "
        f":{risk_color(row['risk_level'])}[{status_label}]"
    )
    if st.button(tr("generate_hr", lang), type="primary"):
        st.success(ai_student_advice(row, lang))

elif page == "profile":
    selected_name = st.selectbox(tr("select_intern", lang), filtered["name"].tolist())
    row = filtered[filtered["name"] == selected_name].iloc[0]

    top1, top2, top3, top4 = st.columns(4)
    with top1:
        st.metric(tr("role", lang), row["role"])
    with top2:
        st.metric(tr("stage", lang), row["stage"])
    with top3:
        st.metric(tr("fit_score", lang), f"{row['fit_score']}")
    with top4:
        st.metric(tr("risk_level", lang), RISK_LABELS[lang][row["risk_level"]])

    st.subheader(tr("basic_info", lang))
    st.write(
        tr(
            "basic_info_text",
            lang,
            name=row["name"],
            school=row["school"],
            major=row["major"],
            mentor=row["mentor"],
            goal=row["career_goal"],
        )
    )

    left, right = st.columns([1, 1])
    with left:
        st.subheader(tr("growth_path", lang))
        st.dataframe(path_for_role(row["role"], lang), width="stretch", hide_index=True)
    with right:
        st.subheader(tr("radar", lang))
        st.plotly_chart(radar_chart(row, lang), width="stretch")

    st.subheader(tr("feedback_ai", lang))
    st.write(tr("raw_feedback", lang, feedback=row["mentor_feedback"]))
    st.info(ai_student_advice(row, lang))

elif page == "mentor":
    st.subheader(tr("mentor_todo", lang))
    mentor = st.selectbox(tr("select_mentor", lang), sorted(filtered["mentor"].unique()))
    mentor_df = filtered[filtered["mentor"] == mentor].copy()
    need_action = mentor_df[
        (mentor_df["feedback_status"] != "已反馈")
        | (mentor_df["risk_level"].isin(["需要关注", "高风险"]))
        | (mentor_df["last_feedback_days"] >= 10)
    ].sort_values("fit_score")

    a, b, c, d = st.columns(4)
    with a:
        st.metric(tr("mentee_count", lang), len(mentor_df))
    with b:
        st.metric(tr("todo_count", lang), len(need_action))
    with c:
        st.metric(tr("avg_fit", lang), f"{mentor_df['fit_score'].mean():.1f}")
    with d:
        st.metric(tr("feedback_timely", lang), f"{(mentor_df['last_feedback_days'] <= 7).mean() * 100:.0f}%")

    st.dataframe(
        localize_columns(
            need_action[["name", "role", "stage", "fit_score", "risk_level", "feedback_status", "last_feedback_days"]],
            lang,
        ),
        width="stretch",
        hide_index=True,
    )

    st.subheader(tr("feedback_generator", lang))
    selected = st.selectbox(tr("select_feedback_intern", lang), mentor_df["name"].tolist())
    row = mentor_df[mentor_df["name"] == selected].iloc[0]
    task_note = st.text_area(tr("weekly_note", lang), value=row["mentor_feedback"], height=100)
    if st.button(tr("generate_feedback", lang), type="primary"):
        st.success(ai_mentor_feedback(row, lang))
        st.write(tr("supplement", lang), task_note)

    st.subheader(tr("mentor_template", lang))
    if lang == "zh":
        template = pd.DataFrame(
            [
                ("第 1 周", "建立关系、确认目标、熟悉业务和工具", "完成入职任务清单"),
                ("第 2-4 周", "拆解基础任务，建立反馈节奏", "每周至少一次具体反馈"),
                ("第 5-8 周", "尝试独立交付，暴露并解决关键短板", "完成一个岗位相关小项目"),
                ("第 9-12 周", "复盘成长表现，形成转正判断依据", "输出转正评估材料"),
            ],
            columns=["阶段", "导师动作", "衡量标准"],
        )
    else:
        template = pd.DataFrame(
            [
                ("Week 1", "Build trust, confirm goals, learn business and tools", "Complete onboarding checklist"),
                ("Weeks 2-4", "Break down basic tasks and set a feedback rhythm", "At least one concrete feedback session per week"),
                ("Weeks 5-8", "Try independent delivery and expose key gaps", "Complete one role-related mini project"),
                ("Weeks 9-12", "Review growth and form conversion evidence", "Submit conversion evaluation materials"),
            ],
            columns=["Stage", "Mentor Action", "Measure"],
        )
    st.dataframe(template, width="stretch", hide_index=True)

elif page == "trend":
    st.subheader(tr("trend_title", lang))
    weekly = (
        filtered.groupby("week", as_index=False)
        .agg(
            fit_score=("fit_score", "mean"),
            task_completion=("task_completion", "mean"),
            satisfaction=("satisfaction", "mean"),
        )
        .sort_values("week")
    )
    weekly["fit_score"] = weekly["fit_score"].round(1)
    weekly["task_completion"] = weekly["task_completion"].round(1)
    weekly["satisfaction"] = weekly["satisfaction"].round(1)

    fig = px.line(
        weekly,
        x="week",
        y=["fit_score", "task_completion", "satisfaction"],
        markers=True,
        title=tr("fit_trend_title", lang),
    )
    fig.update_layout(height=420, yaxis_range=[0, 100])
    st.plotly_chart(fig, width="stretch")

    role_weekly = (
        filtered.groupby(["week", "role"], as_index=False)["fit_score"]
        .mean()
        .sort_values(["role", "week"])
    )
    role_weekly["fit_score"] = role_weekly["fit_score"].round(1)
    fig = px.line(
        role_weekly,
        x="week",
        y="fit_score",
        color="role",
        markers=True,
        title=tr("role_trend_title", lang),
    )
    fig.update_layout(height=420, yaxis_range=[0, 100])
    st.plotly_chart(fig, width="stretch")

    left, right = st.columns([1.1, 1])
    with left:
        fig = px.scatter(
            filtered,
            x="satisfaction",
            y="fit_score",
            color="risk_level",
            size="task_completion",
            hover_name="name",
            hover_data=["role", "week", "mentor_score"],
            title=tr("satisfaction_title", lang),
            color_discrete_map={
                "高潜": "#147a4d",
                "健康成长": "#2563eb",
                "需要关注": "#b45309",
                "高风险": "#b91c1c",
            },
        )
        fig.update_layout(height=420, xaxis_range=[0, 100], yaxis_range=[0, 100])
        st.plotly_chart(fig, width="stretch")
    with right:
        st.subheader(tr("risk_reason_title", lang))
        st.caption(tr("risk_reason_hint", lang))
        reasons = risk_reason_table(filtered, lang)
        if len(reasons):
            fig = px.bar(reasons, x="count", y="reason", orientation="h", title=tr("risk_reason_title", lang))
            fig.update_layout(height=360, yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, width="stretch")
            st.dataframe(reasons, width="stretch", hide_index=True)
        else:
            st.info("No major risk drivers." if lang == "en" else "当前筛选范围内暂无明显风险原因。")

elif page == "hr":
    st.subheader(tr("role_analysis", lang))
    role_summary = (
        filtered.groupby("role")
        .agg(
            avg_fit_score=("fit_score", "mean"),
            avg_task_completion=("task_completion", "mean"),
            avg_mentor_score=("mentor_score", "mean"),
            risk_count=("risk_level", lambda x: x.isin(["需要关注", "高风险"]).sum()),
            count=("name", "count"),
        )
        .reset_index()
    )
    role_summary["risk_ratio"] = (role_summary["risk_count"] / role_summary["count"] * 100).round(1)
    role_summary_labels = {
        "zh": {
            "role": "岗位",
            "avg_fit_score": "平均适岗指数",
            "avg_task_completion": "平均任务完成率",
            "avg_mentor_score": "平均导师评分",
            "risk_count": "风险人数",
            "count": "人数",
            "risk_ratio": "风险占比",
        },
        "en": {
            "role": "Role",
            "avg_fit_score": "Avg fit score",
            "avg_task_completion": "Avg task completion",
            "avg_mentor_score": "Avg mentor score",
            "risk_count": "Risk count",
            "count": "Count",
            "risk_ratio": "Risk ratio",
        },
    }
    st.dataframe(role_summary.round(1).rename(columns=role_summary_labels[lang]), width="stretch", hide_index=True)

    left, right = st.columns(2)
    with left:
        fig = px.scatter(
            filtered,
            x="task_completion",
            y="fit_score",
            color="risk_level",
            size="mentor_score",
            hover_name="name",
            hover_data=["role", "initiative", "collaboration"],
            title=tr("scatter_title", lang),
            color_discrete_map={
                "高潜": "#147a4d",
                "健康成长": "#2563eb",
                "需要关注": "#b45309",
                "高风险": "#b91c1c",
            },
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, width="stretch")
    with right:
        conversion = filtered["conversion_potential"].value_counts().reset_index()
        conversion.columns = ["conversion_potential", "count"]
        fig = px.bar(
            conversion,
            x="conversion_potential",
            y="count",
            color="conversion_potential",
            title=tr("conversion_title", lang),
            color_discrete_sequence=["#147a4d", "#2563eb", "#b45309", "#b91c1c"],
        )
        fig.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig, width="stretch")

    st.subheader(tr("high_and_risk", lang))
    col1, col2 = st.columns(2)
    with col1:
        st.write(tr("high_potential", lang))
        st.dataframe(
            localize_columns(
                filtered[filtered["risk_level"] == "高潜"].sort_values("fit_score", ascending=False)[
                    ["name", "role", "fit_score", "conversion_potential", "mentor_feedback"]
                ],
                lang,
            ),
            width="stretch",
            hide_index=True,
        )
    with col2:
        st.write(tr("risky_talent", lang))
        st.dataframe(
            localize_columns(
                filtered[filtered["risk_level"].isin(["需要关注", "高风险"])].sort_values("fit_score")[
                    ["name", "role", "fit_score", "risk_level", "feedback_status", "last_feedback_days"]
                ],
                lang,
            ),
            width="stretch",
            hide_index=True,
        )

    st.subheader(tr("risk_reason_title", lang))
    st.caption(tr("risk_reason_hint", lang))
    reasons = risk_reason_table(filtered, lang)
    if len(reasons):
        fig = px.bar(reasons, x="count", y="reason", orientation="h", title=tr("risk_reason_title", lang))
        fig.update_layout(height=360, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No major risk drivers." if lang == "en" else "当前筛选范围内暂无明显风险原因。")

    st.subheader(tr("ai_report", lang))
    st.info(ai_weekly_report(filtered, lang))
    st.download_button(
        tr("export_report", lang),
        build_markdown_report(filtered, lang).encode("utf-8-sig"),
        file_name="intern_energy_hr_report.md",
        mime="text/markdown",
    )
