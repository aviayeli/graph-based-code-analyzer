# EX04 — הנדסה הפוכה ו-AI אגנטי יעיל בטוקנים
## ניתוח קוד המקור של Claude Code באמצעות גרפי ידע

<div dir="rtl">

> **קורס:** בינה מלאכותית גנרטיבית ו-LLMים  
> **מטלה:** EX04 — Reverse Engineering & Token-Efficient Agentic AI  
> **תאריך הגשה:** יוני 2026  
> **כלים:** Python 3.11 · Graphify · Obsidian · NetworkX · TypeScript AST

---

## תוכן עניינים

1. [תיאור המאגר ובחירת הפרויקט](#1-תיאור-המאגר-ובחירת-הפרויקט)
2. [שאלות מחקר ובעיה](#2-שאלות-מחקר-ובעיה)
3. [סקירת ארכיטקטורה](#3-סקירת-ארכיטקטורה)
4. [מתודולוגיה — Graphify ו-Obsidian](#4-מתודולוגיה--graphify-ו-obsidian)
5. [ממצאים — God Nodes ובקבוקי צוואר](#5-ממצאים--god-nodes-ובקבוקי-צוואר)
6. [יעילות טוקנים FinOps](#6-יעילות-טוקנים-finops)
7. [זרימת עבודה אגנטית — CrewAI / LangGraph](#7-זרימת-עבודה-אגנטית--crewai--langgraph)
8. [אלמנטים ויזואליים](#8-אלמנטים-ויזואליים)
9. [הוראות התקנה והפעלה](#9-הוראות-התקנה-והפעלה)
10. [מסקנות](#10-מסקנות)

---

## 1. תיאור המאגר ובחירת הפרויקט

### מה הוא Claude Code?

**Claude Code** הוא ממשק שורת הפקודה (CLI) הרשמי של חברת Anthropic לסוכן AI אוטונומי. הוא מאפשר למפתחים לנהל שיחה עם מודל Claude ישירות מהטרמינל — הסוכן קורא ומשנה קבצים, מריץ פקודות Bash, מנהל Git ומייצר Pull Requests ללא התערבות אנושית.

### מדוע בחרנו בפרויקט זה?

בחרנו להנדיס לאחור את קוד המקור של Claude Code מתוך שלוש סיבות עיקריות:

1. **מורכבות אגנטית אמיתית** — Claude Code הוא אחד מהיישומים האגנטיים המורכבים ביותר שנחשפו בפומבי. הוא לא demo — הוא מערכת ייצור עם 1,900 קבצי TypeScript ומעל 2 מיליון מילים.

2. **ארכיטקטורה רב-שכבתית** — הפרויקט כולל מנגנוני אבטחה ספקולטיביים, ניהול זיכרון אוטונומי, תזמון ברקע, ו-Persona mode נסתרת — רכיבים שנדיר למצוא יחד בקוד פתוח.

3. **אתגר ה-FinOps** — 2 מיליון מילים הם גבול בלתי-עביר לכל LLM בגישה ישירה. הפרויקט הזה הוא הוכחת-מושג אמיתית לצורך בניווט גרפי.

### היקף הפרויקט

| מדד | ערך |
|-----|-----|
| שפת תכנות | TypeScript (`ts` / `tsx`) |
| מספר קבצים | **1,900** |
| היקף קוד | **~2,002,597 מילים** (~2.5M טוקנים) |
| צמתי גרף | **15,906** (פונקציות, טיפוסים, קבצים, מחלקות) |
| קשתות גרף | **57,097** (imports, calls, contains) |
| קהילות שזוהו | **311** (20 מהן נקראו בשם) |
| God Nodes | **10** (degree ≥ 196) |
| תת-מערכות נסתרות | **5** (KAIROS · autoDream · undercover · buddy · bashSecurity) |
| טוקנים שנצרכו בחילוץ | **0** (AST דטרמיניסטי בלבד) |

### תוצרי הפרויקט

| קובץ | תיאור |
|------|-------|
| `claude-code/src/graphify-out/graph.json` | גרף ידע גולמי (15,906 צמתים, 57,097 קשתות) |
| `claude-code/src/graphify-out/index.md` | מפת ניווט מאקרו — 20 קהילות, wikilinks |
| `claude-code/src/graphify-out/hot.md` | מפת חום — 10 God Nodes + 5 תת-מערכות נסתרות |
| `claude-code/src/graphify-out/GRAPH_REPORT.md` | ניתוח ארכיטקטורי מקיף |
| `claude-code/src/graphify-out/graph.html` | ויזואליזציה אינטראקטיבית (תצוגת קהילות) |

---

## 2. שאלות מחקר ובעיה

### הבעיה המרכזית: "Lost in the Middle"

מחקר של Stanford מ-2023 הראה שמודלי שפה מאבדים מידע מהחלקים **האמצעיים** של פרומפטים ארוכים — תופעה המכונה **"Lost in the Middle"**. בפרויקט כמו Claude Code, הבעיה חמורה בצורה קיצונית:

```
גישה נאיבית:
  1,900 קבצים × ~1,050 טוקנים ≈ 2,000,000 טוקנים
  → 6–10 קריאות API נפרדות
  → עלות: ~$6.00 לניתוח אחד
  → Lost in the Middle: המודל מחמיץ קשרים בין קהילות
  → תשובות שגויות על ארכיטקטורה

גישת גרף:
  index.md + hot.md + שאילתה ממוקדת ≈ 12,000 טוקנים
  → עלות: ~$0.04 לניתוח
  → חיסכון: 99.4%
  → ניווט מדויק ממאקרו למיקרו
```

### שאלות המחקר

**ש1 — God Nodes:** כיצד מזהים פונקציות שעצם שינוי שמן ישבור 1,177 מודולים בו-זמנית — מבלי לקרוא שורת קוד אחת?

**ש2 — תת-מערכות נסתרות:** אילו תכונות קיימות בקוד הייצור אך אינן מוזכרות בתיעוד הרשמי? (KAIROS, autoDream, undercover, buddy, bashSecurity)

**ש3 — FinOps:** כיצד מפחיתים צריכת טוקנים ב-99%+ תוך שמירה על עומק ניתוח מלא לפרויקט בהיקף 2M מילים?

**ש4 — Cross-Community Coupling:** אילו זוגות מודולים שנראים לא-קשורים מגלים תלות נסתרת כשמנתחים את גרף ה-AST? (דוגמה: `runHeadlessStreaming()` → `createIdleTimeoutManager()`)

---

## 3. סקירת ארכיטקטורה

גרף הידע חשף ארכיטקטורה **תלת-שכבתית** עם singleton גלובלי כנקודת ייחוס מרכזית:

```
╔══════════════════════════════════════════════════════════════════╗
║  שכבת ממשק משתמש — Presentation Tier                           ║
║  components/ · screens/ · hooks/ · context/                      ║
║  ממשק טרמינל Ink/React · מערכת התראות · keybindings             ║
╚═══════════════════════════╦══════════════════════════════════════╝
                            ║ imports ↓
╔═══════════════════════════╩══════════════════════════════════════╗
║  שכבת הדומיין — Domain Tier                                     ║
║  tools/        commands/     tasks/       skills/    services/   ║
║  BashTool      slash cmds    agents       SkillTool  MCP/compact ║
║  AgentTool     git/commit    swarm        brief      autoDream   ║
║  FileEdit      config        InProcess    security   PromptSugg. ║
╚═══════════════════════════╦══════════════════════════════════════╝
                            ║ imports ↓
╔═══════════════════════════╩══════════════════════════════════════╗
║  שכבת תשתית — Infrastructure Tier                               ║
║  bootstrap/state.ts  ← Singleton גלובלי (~1,600 שורות, ~50 API) ║
║  utils/              ← debug · log · config · fs · git · env    ║
║  services/analytics/ ← GrowthBook · logEvent · OTel telemetry   ║
║  utils/permissions/  ← filesystem · yoloClassifier · sandbox    ║
╚══════════════════════════════════════════════════════════════════╝
```

### `bootstrap/state.ts` — הקובץ הכי חשוב בפרויקט

קובץ יחיד בן ~1,600 שורות שמייצא ~50 state accessors. **כל מודול אחר** בפרויקט מייבא ממנו. הוא גם מכיל את נקודת הכניסה לתכונת KAIROS (שורה 1085) — תת-מערכת לתזמון אוטונומי שלא מוזכרת בתיעוד הרשמי.

### זרימת בקשת משתמש — End to End

```
PromptInput.tsx  →  handlePromptSubmit.ts  →  QueryEngine.ts
                                                     ↓
                                              query.ts  →  services/api/claude.ts
                                                                    ↓
                                              ┌─────────────────────┤
                                              ↓                     ↓
                                   promptCacheBreakDetection    api/errors.ts
                                              ↓
                                       toolExecution.ts
                                    ┌────────┼────────┐
                                    ↓        ↓        ↓
                               BashTool  AgentTool  FileEditTool
                                    ↓        ↓
                           bashPermissions  runAgent.ts → spawnMultiAgent.ts
                                    ↓
                           yoloClassifier (ספקולטיבי)
                                              ↓
                                    Messages.tsx / REPL.tsx
```

### ה-20 קהילות המרכזיות

| # | קהילה | צמתים | לכידות | קבצים מרכזיים |
|---|-------|-------|--------|--------------|
| 0 | Agent UI Editor | 263 | 0.017 | `AgentDetail.tsx`, `AgentEditor.tsx` |
| 1 | Core State & Session | 259 | 0.021 | `bootstrap/state.ts`, `sessionStorage.ts` |
| 2 | UI Components & Bridge | 249 | 0.018 | `AgentsMenu.tsx`, `bridge/` |
| 3 | Agent Tool Core | 242 | 0.021 | `AgentTool.tsx`, `runAgent.ts` |
| 4 | Agent Dispatch & Prompts | 203 | 0.023 | `prompt.ts`, `builtinAgents.ts` |
| 5 | Bash Command Parsing | 195 | 0.022 | `bash/commands.ts`, `bash/ast.ts` |
| 6 | Analytics & Admin API | 181 | 0.028 | `api/adminRequests.ts` |
| 7 | Claude API & Bootstrap | 171 | 0.020 | `api/claude.ts`, `REPL.tsx` |
| 8 | Tool Execution & Diff | 168 | 0.026 | `FileEditTool.ts`, `FileWriteTool.ts` |
| 9 | API Error Handling | 163 | 0.023 | `api/errors.ts`, `utils/messages.ts` |
| 10 | Feature Flags & Billing | 162 | 0.029 | `analytics/growthbook.ts` |
| 11 | Settings & Config | 160 | 0.030 | `utils/settings/settings.ts` |
| 12 | First-Party Analytics | 158 | 0.031 | `analytics/firstPartyEventLoggingExporter.ts` |
| 13 | Plan Mode & Hooks | 155 | 0.022 | `hooks/asyncHookRegistry.ts` |
| 14 | Bridge Status UI | 154 | 0.025 | `bridge/bridgeStatusUtil.ts` |
| 15 | Bash Permissions & Safety | 153 | 0.028 | `tools/BashTool/bashPermissions.ts` |
| 16 | Stats & Icon Components | 151 | 0.024 | `components/FastIcon.tsx` |
| 17 | Prompt Cache Detection | 149 | 0.032 | `api/promptCacheBreakDetection.ts` |
| 18 | Task List Hooks | 141 | 0.028 | `hooks/useTaskListWatcher.ts` |
| 19 | Agent Loading & Feature Flags | 141 | 0.031 | `tools/AgentTool/loadAgentsDir.ts` |

---

## 4. מתודולוגיה — Graphify ו-Obsidian

### שלב א׳ — חילוץ AST דטרמיניסטי (0 טוקנים)

הצעד הראשון היה הפעלת **Graphify** על 1,900 קבצי TypeScript. ניתוח AST הוא תהליך דטרמיניסטי לחלוטין — ללא LLM, ללא עלות טוקנים:

```bash
# הרצת graphify על src/ של Claude Code
/graphify ./claude-code/src

# תוצאה:
# ✓ AST: 15,912 nodes, 67,128 edges  (0 tokens)
# ✓ Merged: 15,906 nodes, 57,097 edges
# ✓ 311 communities detected (Louvain)
# ✓ 10 God Nodes identified
```

**מה Graphify חילץ מכל קובץ TypeScript:**
- **צמתים:** פונקציות, מחלקות, ממשקים, טיפוסים, קבצים
- **קשתות:** `imports`, `calls`, `contains`, `imports_from`
- **98% EXTRACTED** (מ-AST ישיר) + **2% INFERRED** (הסקה סמנטית עם confidence 0.8)

### שלב ב׳ — גילוי קהילות (Community Detection)

```python
# תהליך גילוי הקהילות (פנימי ב-Graphify)
G = build_from_json(extraction, root='./claude-code/src', directed=False)
communities = cluster(G)          # אלגוריתם Louvain
cohesion    = score_all(G, communities)  # מדידת לכידות תוך-קהילתית
gods        = god_nodes(G)        # degree ≥ 196 → God Node
surprises   = surprising_connections(G, communities)  # קשתות בין-קהילתיות
```

**אלגוריתם Louvain** ממטב את ה-modularity של הגרף — הוא מוצא חלוקה לקהילות כך שהקשתות בתוך קהילה צפופות יותר מהקשתות בין קהילות. לכידות (cohesion) נמוכה מ-0.022 מציינת קהילת-אינטגרציה (hub); מעל 0.030 — מודול עצמאי שניתן לחלץ לחבילה נפרדת.

### שלב ג׳ — ניווט מאקרו→מזו→מיקרו ב-Obsidian

הקבצים שנוצרו נטענו כ-**Obsidian Vault** ומאפשרים ניווט גרפי מלא:

```
index.md                ← נקודת כניסה מאקרו (סטטיסטיקות, 20 קהילות, 5 נסתרות)
       ↓ wikilink
[[Core State & Session]] ← רמת קהילה (259 צמתים, קבצים מרכזיים, תיאור)
       ↓ wikilink
[[hot#KAIROS]]           ← רמת מיקרו (פונקציה, 24 חיבורים, קוד מקורי)
       ↓ graphify explain
getKairosActive()        ← עומק מלא + נתיב ל-autoDream (1 hop)
```

> **[הוספת צילום מסך Obsidian Graph View כאן]**  
> *פתחו את `claude-code/src/graphify-out/` כ-Vault, עברו ל-Graph View (Ctrl+G), ותראו את הרשת עם `index.md` ו-`hot.md` כ-hub nodes מרכזיים.*

### שלב ד׳ — שאילתות גרף ממוקדות

```bash
# שאילתת BFS (הקשר רחב)
graphify query "KAIROS autoDream undercover buddy bashSecurity"
# → 706 צמתים, 0 טוקנים

# נתיב קצר ביותר בין שני מושגים
graphify path "autoDream" "KAIROS"
# → autoDream.ts --imports--> getKairosActive()  (1 hop בלבד!)

# הסבר מעמיק של צומת
graphify explain "autoDream"
# → 56 חיבורים, קהילה 129, כל תלויות הייבוא

# שאילתת DFS (עיקוב נתיב ספציפי)
graphify query "speculative classifier yolo bash approval" --dfs
```

---

## 5. ממצאים — God Nodes ובקבוקי צוואר

### 5.1 טבלת God Nodes

"God Node" הוא כל צומת שה-degree שלו עולה על 196 — כלומר, 196+ מודולים שונים מייבאים אותו ישירות. 10 ה-God Nodes ביחד מהווים **~8% מכלל 57,097 הקשתות**.

| # | פונקציה | Degree | Betweenness | קובץ מקורי | קהילות מחוברות |
|---|---------|--------|-------------|------------|----------------|
| 1 | `logForDebugging()` | **1,177** | **0.179** | `utils/debug.ts:L203` | 155+ |
| 2 | `logError()` | 574 | 0.058 | `utils/log.ts:L158` | 120+ |
| 3 | `jsonStringify()` | 381 | — | `utils/slowOperations.ts:L180` | — |
| 4 | `logEvent()` | 370 | — | `services/analytics/index.ts:L133` | — |
| 5 | `isEnvTruthy()` | 343 | — | `utils/envUtils.ts:L32` | — |
| 6 | `errorMessage()` | 318 | — | `utils/errors.ts:L119` | — |
| 7 | `getFsImplementation()` | 263 | — | `utils/fsOperations.ts:L621` | — |
| 8 | `getGlobalConfig()` | 259 | — | `utils/config.ts:L1044` | — |
| 9 | `getCwd()` | 214 | — | `utils/cwd.ts:L26` | — |
| 10 | `getFeatureValue_CACHED_MAY_BE_STALE()` | 196 | — | `services/analytics/growthbook.ts:L734` | — |

> **[הוספת דיאגרמת רשת של 10 God Nodes כאן]**  
> *כלי מוצע: `graphify export html` ← פתחו את `graph.html` וסננו לפי degree ≥ 196*

### 5.2 ניתוח מקרה: `logForDebugging()` — הצומת הכי מסוכן

```
degree: 1,177  |  betweenness centrality: 0.179
```

- **17.9% מכלל הנתיבים הקצרים בגרף** עוברים דרכו
- פונקציית ניפוי שגיאות שמיובאת **ישירות לקוד ייצור** במקום דרך wrapper
- **24 קשתות INFERRED** ל-`initializeAgentMcpServers()` ו-`addCacheBreakpoints()` — תלות נסתרת

> **סיכון:** שינוי שם, חתימה, או מיקום הפונקציה ידרוש עדכון ידני ב-1,177 מקומות בו-זמנית.

### 5.3 ניתוח מקרה: `getFeatureValue_CACHED_MAY_BE_STALE()` — פשרת latency/עדכניות

שם הפונקציה עצמו הוא **תיעוד in-band** — הסיומת `_CACHED_MAY_BE_STALE` מזהירה כי הערך עלול להיות ישן. **196 אתרי קריאה** משתמשים בה לשליטה על feature flags — כולל ב-`bashPermissions` (אבטחה) ו-`api/overageCreditGrant` (חיוב כספי). ערך ישן בהקשרים אלה עלול לאשר פקודה מסוכנת שהייתה אמורה להיחסם.

### 5.4 חיבורים מפתיעים בין קהילות

| מקור | יעד | קבצי גישור | מדוע מפתיע |
|------|-----|-----------|------------|
| `logOTelEvent()` | `getEventLogger()` | `utils/telemetry/events.ts` ↔ `bootstrap/state.ts` | OTel מחווט ישירות ל-bootstrap state |
| `handleInitializeRequest()` | `setInitJsonSchema()` | `cli/print.ts` ↔ `bootstrap/state.ts` | שכבת CLI מגיעה לאתחול schema |
| `runHeadless()` | `takeInitialUserMessage()` | `cli/print.ts` ↔ `utils/sessionStart.ts` | headless שולט על תחילת session |
| `runHeadlessStreaming()` | `createIdleTimeoutManager()` | `cli/print.ts` ↔ `utils/idleTimeout.ts` | streaming runner מייצר lifecycle timeout עצמאי |
| `runHeadlessStreaming()` | `setPermissionModeChangedListener()` | `cli/print.ts` ↔ `utils/sessionState.ts` | שכבת streaming רושמת האזנה להרשאות ישירות |

### 5.5 חמש התת-מערכות הנסתרות

#### KAIROS — מצב תזמון אוטונומי

```
bootstrap/state.ts · שורה 1085
getKairosActive() · setKairosActive() · isKairosCronEnabled()
קהילה 4 · degree: 24
```

שם מיוונית: "הרגע הנכון". שער גלובלי שמעביר את המערכת ממצב CLI אינטראקטיבי לסוכן-רקע אוטונומי. BashTool, PowerShellTool, autoDream, fastMode ו-BriefTool — כולם בודקים אותו ומשנים את התנהגותם. נתיב קצר ביותר ל-autoDream: **1 hop** בלבד.

#### autoDream — מיצוי זיכרון אוטומטי ברקע

```
services/autoDream/autoDream.ts · קהילה 129 · degree: 56
```

כשהסשן סרלאי (ו-KAIROS פעיל), autoDream מפעיל **סוכן-בן (forked agent)** שקורא את הסשן, מחלץ ממנו זיכרונות ערך, וכותב אותם ל-`~/.claude/memories/`. בסשן הבא, `loadMemoryPrompt()` טוען אותם אוטומטית — זוהי מערכת הזיכרון הפעילה, לא רק הפקודה הידנית `/remember`.

```
autoDream.ts → getKairosActive() → isAutoMemoryEnabled()
             → extractMemories.ts → forkedAgent.ts → paths.ts [memdir/]
             ← stopHooks.ts  (כיבוי דרך stop hooks)
```

#### undercover — מצב Stealth / Whitelabel

```
utils/undercover.ts · קהילה 132 · degree: 15
isUndercover() · getUndercoverInstructions() · shouldShowUndercoverAutoNotice()
```

מסתיר את זהות Claude Code מכותרות commit, מפרומפטים, ומגוף PR. מיועד לפריסות ארגוניות שבהן הלקוח מוציא את הכלי תחת שם המותג שלו, או לכלים פנימיים שבהם ייחוס ל-Claude לא רצוי.

#### buddy — חיית מחמד ASCII אינטראקטיבית

```
buddy/ · קהילות 97, 120
CompanionSprite.tsx · companion.ts · sprites.ts · types.ts
```

Sprite ASCII מונפש שחי בטרמינל — עם מין, נדירות ונתוני RPG שנוצרים **דטרמיניסטית** לפי User ID. מינים: goose, duck, snail, dragon, axolotl, cactus, mushroom. מנגנון: `hashString(userId)` → `mulberry32()` PRNG → `rollRarity()` → `rollStats()`.

#### bashSecurity — מסווג אבטחה ספקולטיבי

```
tools/BashTool/bashPermissions.ts · קהילה 15
utils/permissions/yoloClassifier.ts · קהילה 114
```

לפני שהמשתמש מאשר פקודת Bash, המערכת מפעילה בדיקת אבטחה **אסינכרונית** ברקע. כשהמשתמש מאשר — התוצאה כבר מוכנה (latency אפסי):

```
BashTool מקבל פקודה
  ↓  executeAsyncClassifierCheck()  ← async, מיידי, ללא await
  ↓  [המשתמש מחליט בזמן הבדיקה רצה]
  ↓  awaitClassifierAutoapproval()  ← תוצאה מוכנה, חסימה אפסית
```

השם "yolo" הוא אירוני — זהו דווקא הבודק ה**שמרני** שמחליט אם פקודה עלולה להזיק.

---

## 6. יעילות טוקנים FinOps

### השוואת גישות

| גישה | טוקנים | עלות (Sonnet) | דיוק |
|------|--------|--------------|------|
| קריאת כל הקוד | ~2,000,000 | ~$6.00 | נמוך (Lost in the Middle) |
| קריאת קובץ בודד ממוקד | ~50,000 | ~$0.15 | בינוני (חסר הקשר) |
| **ניווט גרפי (index + hot + שאילתה)** | **~12,000** | **~$0.04** | **גבוה** |

> **חיסכון: 99.4% בטוקנים · 150× זול יותר לשאלה ארכיטקטונית**

### שלוש רמות הניווט

```
רמה 1 — מאקרו     index.md        ~2,500 טוקנים
                       ↓
רמה 2 — מזו       GRAPH_REPORT.md  ~4,000 טוקנים
                       ↓
רמה 3 — מיקרו     hot.md           ~5,500 טוקנים
                                    ───────────────
         סך הכל:                    ~12,000 טוקנים
         כיסוי:    95%+ מהידע הארכיטקטוני
```

### כיצד גרף פותר את "Lost in the Middle"

**1. שאלה נשאלת** → Graphify מריץ BFS/DFS על `graph.json`  
**2. תת-גרף רלוונטי** (~500–2,000 טוקנים) → נשלח ל-LLM בלבד  
**3. LLM מקבל רק מה שצריך** → אין "אמצע" שאבד  
**4. תשובה מדויקת** בעלות נמינלית  

> **[הוספת גרף השוואת עלויות טוקנים כאן]**  
> *Bar chart: גישה ישירה (2,000,000) לעומת ניווט גרף (12,000)*

### כלל R1 — Hard Token Budgets

בהתאם לכלל R1 המוגדר ב-`CLAUDE.md` של הפרויקט, **כל קריאת LLM חייבת להצהיר על תקציב טוקנים מוערך** לפני הביצוע. תקרת ברירת מחדל: **8,000 טוקנים לקריאה**. ניווט גרפי שומר על כל הקריאות מתחת לתקרה זו.

### בנצ'מרק — שלוש שאילתות ארכיטקטוניות

| שאלה | טוקנים גולמיים | טוקני גרף | חיסכון |
|------|--------------|-----------|-------|
| "מהם ה-God Nodes ומה הסיכון שלהם?" | ~800,000 | 5,500 | **99.3%** |
| "מה עושה autoDream ואיך הוא מחובר ל-KAIROS?" | ~200,000 | 2,000 | **99.0%** |
| "כיצד bashPermissions מאמת פקודה ספציפית?" | ~150,000 | 1,500 | **99.0%** |
| **ממוצע** | **~383,000** | **3,000** | **99.2%** |

---

## 7. זרימת עבודה אגנטית — CrewAI / LangGraph

> **[Placeholder — יממש בגרסה הבאה של הפרויקט]**

### תרשים הסוכנים המתוכנן

> **[הוספת דיאגרמת CrewAI / LangGraph Agent Workflow כאן]**  
> *הדיאגרמה תציג 4 סוכנים בזרימת עבודה: GraphNavigator → BottleneckAnalyzer → RefactorPlanner → TokenBudgetGuard*

### תיאור הסוכנים

```
┌─────────────────────────────────────────────────────────────┐
│  סוכן 1: GraphNavigatorAgent                                │
│  כלים: graphify query · graphify path · graphify explain    │
│  תפקיד: קולט שאלה → מריץ שאילתת גרף → מחזיר תת-גרף ממוקד │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌──────────────────────────▼──────────────────────────────────┐
│  סוכן 2: BottleneckAnalyzerAgent                            │
│  כלים: networkx metrics · degree analysis · betweenness     │
│  תפקיד: מזהה God Nodes ו-coupling בעייתי → רשימת תיקונים   │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌──────────────────────────▼──────────────────────────────────┐
│  סוכן 3: RefactorPlannerAgent                               │
│  כלים: GraphDiffer · AST diff generator                     │
│  תפקיד: מייצר diff מוצע לכל God Node + מעריך עלות טוקנים  │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌──────────────────────────▼──────────────────────────────────┐
│  סוכן 4: TokenBudgetGuardAgent                              │
│  כלים: token counter · budget enforcer (כלל R1)             │
│  תפקיד: מוודא ≤ 8,000 טוקנים לכל קריאה · חוסם קריאות יקרות│
└─────────────────────────────────────────────────────────────┘
```

### תיקוני בקבוקי הצוואר המזוהים

| עדיפות | בעיה | פתרון מוצע | צמצום degree משוער |
|--------|------|-----------|-------------------|
| קריטי | `logForDebugging()` degree 1,177 | Re-export alias לפני rename | מניעת שבירה מלאה |
| גבוה | `bootstrap/state.ts` >1,600 שורות | חילוץ KAIROS → `kairosState.ts` | degree −24 |
| גבוה | `getFeatureValue_CACHED_MAY_BE_STALE()` בנתיבי אבטחה | הוספת `getFeatureValue_FRESH()` | סיכון ≡ 0 |
| בינוני | autoDream: עלות forked agent לא נרשמת | חיבור ל-session cost tracker | observability |
| נמוך | `consumeSpeculativeClassifierCheck()` destructive | Null-safe wrapper | יציבות |

---

## 8. אלמנטים ויזואליים

### א. Obsidian Graph View

> **[הוספת צילום מסך Obsidian Graph View — כל 311 הקהילות — כאן]**  
> *הוראות: פתחו `claude-code/src/graphify-out/` כ-Vault → Ctrl+G → Graph View*

---

### ב. דיאגרמת God Nodes

> **[הוספת דיאגרמת רשת — 10 God Nodes עם degree ו-betweenness — כאן]**  
> *כלי: `graphify export html` → פתחו `graph.html` → סננו degree ≥ 196*

---

### ג. ארכיטקטורת OOP — שלוש השכבות

> **[הוספת דיאגרמת UML: Infrastructure / Domain / Presentation + bootstrap/state.ts — כאן]**  
> *כלי מוצע: Mermaid classDiagram*

---

### ד. מפת זרימת נתונים End-to-End

> **[הוספת flowchart: PromptInput.tsx → REPL.tsx דרך כל שכבות המערכת — כאן]**  
> *כלי מוצע: Mermaid sequenceDiagram*

---

### ה. גרף השוואת טוקנים

> **[הוספת bar chart: גישה ישירה (2,000,000) לעומת ניווט גרף (12,000) — כאן]**  
> *כלי מוצע: matplotlib / Chart.js*

---

### ו. תרשים רצף KAIROS → autoDream → זיכרון

> **[הוספת sequence diagram: KAIROS active → autoDream → forkedAgent → ~/.claude/memories/ — כאן]**  
> *כלי מוצע: Mermaid sequenceDiagram*

---

## 9. הוראות התקנה והפעלה

### דרישות מקדימות

```bash
# Python 3.11+
python3 --version

# uv — מנהל חבילות מהיר
curl -LsSf https://astral.sh/uv/install.sh | sh

# Graphify
uv tool install graphifyy

# אימות התקנה
graphify --version
```

### שכפול המאגר

```bash
git clone <repository-url>
cd graph-based-code-analyzer

# התקנת תלויות Python של הפרויקט
uv sync
```

### הרצת הניתוח מאפס

```bash
# שלב 1: הרצת graphify על src/ של Claude Code (0 טוקנים, AST בלבד)
/graphify ./claude-code/src

# שלב 2: וידוא שהגרף נוצר
ls -lh claude-code/src/graphify-out/
# graph.json   (~8MB, 15,906 nodes, 57,097 edges)
# graph.html   (ויזואליזציה אינטראקטיבית — קהילות מצטברות)
# GRAPH_REPORT.md
# index.md
# hot.md
```

### שאילתות גרף

```bash
# שאילתה כללית (BFS depth=2)
graphify query "KAIROS autoDream undercover buddy bashSecurity"

# נתיב קצר ביותר בין שני מושגים
graphify path "autoDream" "KAIROS"
# ← autoDream.ts --imports--> getKairosActive()  (1 hop)

# הסבר מעמיק של צומת
graphify explain "autoDream"
graphify explain "yoloClassifier"
graphify explain "CompanionSprite"

# שאילתה עם DFS (עיקוב נתיב ספציפי)
graphify query "speculative classifier bash approval" --dfs

# הגבלת תקציב טוקנים (כלל R1: ≤8,000)
graphify query "KAIROS state machine lifecycle" --budget 1500
```

### פתיחה ב-Obsidian

```
1. פתחו Obsidian
2. "Open Folder as Vault" ← בחרו: claude-code/src/graphify-out/
3. Ctrl+G ← Graph View
4. התחילו מ-index.md ועקבו אחר wikilinks לקהילות
```

### הרצת בדיקות Python

```bash
# בדיקות יחידה
uv run pytest tests/ -v

# בדיקת כיסוי (≥80% נדרש)
uv run pytest tests/ --cov=src --cov-report=term-missing

# בדיקת מגבלת 150 שורות לקובץ (כלל R7)
find src/ -name "*.py" | xargs wc -l | awk '$1>150{print "FAIL:",$0;f=1}END{exit f}'
```

### עדכון הגרף לאחר שינויים בקוד

```bash
# עדכון מצטבר — רק קבצים שהשתנו (מהיר, 0 טוקנים)
/graphify ./claude-code/src --update

# בנייה מחדש מלאה
/graphify ./claude-code/src
```

### מבנה הפרויקט

```
graph-based-code-analyzer/
├── src/                          # Python pipeline
│   ├── config.py                 # Pydantic settings + env
│   ├── fetcher.py                # RepoFetcher
│   ├── parser.py                 # ASTParser (Python AST)
│   ├── graph.py                  # GraphBuilder (NetworkX)
│   ├── exporter.py               # GraphExporter (Obsidian MD)
│   ├── finops.py                 # FinOpsAnalyzer
│   ├── differ.py                 # GraphDiffer (before/after)
│   └── mixins/
│       ├── logging_mixin.py      # Cached-property logger
│       ├── token_budget_mixin.py # Hard 8K ceiling + tracking
│       └── checkpoint_mixin.py   # Atomic JSON checkpoints
├── claude-code/src/              # קוד המקור של Claude Code (read-only)
│   └── graphify-out/             # פלטי גרף הידע
│       ├── graph.json            # גרף גולמי (15,906 צמתים)
│       ├── graph.html            # ויזואליזציה אינטראקטיבית
│       ├── index.md              # מפת ניווט מאקרו
│       ├── hot.md                # God Nodes + נסתרות
│       └── GRAPH_REPORT.md       # ניתוח ארכיטקטורי מקיף
├── tests/                        # בדיקות יחידה (≥80% כיסוי)
├── docs/
│   ├── refactor_report.md        # סימולציית refactoring + Mermaid
│   └── finops_report.md          # בנצ'מרק FinOps מפורט
├── CLAUDE.md                     # כללי R1–R8 לסוכן AI
└── pyproject.toml                # תלויות Python עם גרסאות נעוצות
```

---

## 10. מסקנות

ניתוח קוד המקור של Claude Code באמצעות גרפי ידע הניב שלושה ממצאים מרכזיים:

### ממצא א׳ — God Nodes כמדד כמותי לחוב טכני

`logForDebugging()` עם degree 1,177 ו-betweenness centrality 0.179 הוא **מספר** — לא שיפוט סובייקטיבי. ניתן לזהות God Nodes לפני שגורמים נזק, לתעדף refactoring לפי השפעה מדידה, ולעקוב אחר שיפור אורכי בין גרסאות.

### ממצא ב׳ — Code Archaeology — תת-מערכות נסתרות

KAIROS, autoDream, undercover, buddy ו-bashSecurity אינן מוזכרות בתיעוד הרשמי, אך מחוברות בחוזקה לשאר הקוד. ניתוח AST גרפי מגלה אותן תוך דקות — במקום שעות של chasing imports ידני. **הגרף מספר את האמת, לא התיעוד.**

### ממצא ג׳ — 99.2% חיסכון בטוקנים

מעבר מ-2,000,000 טוקנים (קריאה גולמית) ל-12,000 טוקנים (ניווט מאקרו→מיקרו) מאפשר ניתוח מעמיק בתוך **תקציב API סביר** — ומונע את "Lost in the Middle" שמייצר תשובות שגויות על ארכיטקטורה. זהו ה-Karpathy Wiki pattern ביישום FinOps אמיתי.

---

## קישורים

- [Graphify (graphifyy)](https://github.com/safishamsi/graphifyy)
- [Obsidian](https://obsidian.md)
- [Claude Code — Anthropic](https://claude.ai/code)
- [Lost in the Middle — Stanford NLP 2023](https://arxiv.org/abs/2307.03172)
- [Louvain Community Detection](https://arxiv.org/abs/0803.0476)
- [NetworkX](https://networkx.org)

---

*EX04 — Reverse Engineering & Token-Efficient Agentic AI · אוניברסיטת בר-אילן · יוני 2026*  
*נבנה על פי 4 כללי Karpathy: חשוב לפני שכותב · פשטות תחילה · שינויים כירורגיים · ביצוע מונחה-מטרות*

</div>
