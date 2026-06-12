# 《实习能量站》方案说明

版本 A：规则 AI 提交版  
提交口径：当前 Demo 使用规则引擎模拟 AI 决策逻辑，不接真实 AI API；正式落地可接入腾讯混元 / 元宝。

## 中文版方案说明

### 一、问题诊断

某业务部门近期入职 20 名校招实习生，分布在研发、产品、销售等岗位。当前培养方式主要依赖导师经验：实习生不清楚每阶段该学什么、做到什么程度才算合格；导师反馈节奏和评价标准不统一；HR 只能通过私聊和表格零散了解情况，难以及时发现适岗风险和高潜人才。因此，本方案希望把实习培养从“经验带教”升级为“数据看板 + 规则 AI 辅助决策”。

### 二、方案设计

Demo 名为“实习能量站：业务部实习生成长导航 AI 看板”，服务实习生、导师、HR 和业务负责人四类角色。产品包含首页总览、实习生列表、个人详情、导师工作台、成长趋势、HR 分析看板六个页面。核心流程为：入职生成岗位成长路径，每周记录任务进度和导师反馈，系统计算适岗指数与风险等级，自动生成 HR 跟进建议、导师反馈和周报，帮助 HR 推动导师或实习生完成干预。

### 三、AI 工具选型

版本 A 不接入真实 AI API，不需要 API Key。Demo 阶段采用规则引擎模拟 AI 决策逻辑，基于任务完成率、岗位技能、导师反馈、学习主动性、协作评分等结构化数据，自动生成 HR 建议、导师反馈和管理周报。这样可以保证公网部署稳定、免费、无需登录，也避免因模型额度、网络或密钥配置导致演示失败。

正式落地时，可接入腾讯混元大模型或腾讯元宝，将结构化数据、导师反馈文本和风险原因作为 Prompt 输入，生成更自然、更个性化的成长建议。规则引擎负责稳定判断风险，大模型负责语言生成与个性化表达，二者结合可降低幻觉风险并提升可解释性。

### 四、指标体系

- 适岗指数 = 30% 任务完成率 + 25% 岗位技能评分 + 20% 导师反馈评分 + 15% 学习主动性 + 10% 沟通协作评分。
- 风险等级：85-100 为高潜，70-84 为健康成长，55-69 为需要关注，55 以下为高风险。
- 风险原因拆解：任务滞后、导师反馈延迟、主动性不足、协作偏低、适岗下滑。

### 五、效果评估

对实习生而言，系统降低“我该学什么”的迷茫感；对导师而言，反馈模板减少撰写成本并统一带教标准；对 HR 而言，看板将被动追问变为主动预警；对业务负责人而言，系统能更早识别高潜人才和培养风险，为转正决策提供依据。

---

## English Proposal

### 1. Problem Diagnosis

A business unit recently onboarded 20 campus interns across engineering, product, and sales roles. Current mentoring relies heavily on individual mentor experience. Interns are unsure what to learn at each stage; mentors use inconsistent feedback standards; and HR lacks a real-time view of intern growth, role-fit risk, and high-potential talent. This project upgrades intern development from experience-based coaching to a data dashboard plus rule-based AI decision support.

### 2. Solution Design

Intern Energy Station serves four user groups: interns, mentors, HR, and business leaders. It includes six pages: overview, intern list, profile, mentor workspace, growth trends, and HR analytics. The workflow is: generate a role-specific growth path, record weekly progress and mentor feedback, calculate fit scores and risk levels, automatically generate HR follow-up advice, mentor feedback, and weekly reports, then help HR drive timely interventions.

### 3. AI Approach

Version A does not connect to a real AI API and does not require an API key. The demo uses a rule engine to simulate AI decision logic. Based on structured data such as task completion, job skills, mentor feedback, initiative, and collaboration, it automatically generates HR advice, mentor feedback, and management reports. This keeps public deployment stable, free, and login-free.

In production, the product can connect to Tencent Hunyuan or Yuanbao. Structured data, mentor feedback, and risk drivers can be used as prompt inputs to generate more natural and personalized growth recommendations. The rule engine handles stable risk judgment, while the large model improves language generation and personalization.

### 4. Metric System

- Fit Score = 30% task completion + 25% job skill + 20% mentor score + 15% initiative + 10% collaboration.
- Risk levels: 85-100 high potential, 70-84 healthy, 55-69 needs attention, below 55 high risk.
- Risk drivers include task delay, delayed mentor feedback, low initiative, weak collaboration, and declining fit score.

### 5. Expected Impact

For interns, the product reduces uncertainty about what to learn next. For mentors, it reduces feedback-writing effort and standardizes coaching. For HR, it changes management from passive follow-up to proactive alerts. For business leaders, it provides earlier visibility into high-potential talent and development risks.
