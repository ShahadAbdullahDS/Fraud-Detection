from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

METRICS_PATH = DATA_DIR / "model_metrics.json"
FRAUD_STATS_PATH = DATA_DIR / "fraud_stats.json"
EDA_SUMMARY_PATH = DATA_DIR / "eda_summary.json"
HOURLY_FRAUD_PATH = DATA_DIR / "hourly_fraud.csv"
AMT_DIST_PATH = DATA_DIR / "amt_distribution.csv"
PRODUCTCD_PATH = DATA_DIR / "productcd_fraud.csv"
CONFUSION_MATRIX_PATH = DATA_DIR / "confusion_matrix.csv"
FEATURE_IMPORTANCE_PATH = DATA_DIR / "feature_importance.csv"
SAMPLE_TRANSACTIONS_PATH = DATA_DIR / "sample_transactions.csv"
MODEL_INPUT_PATH = DATA_DIR / "model_input_samples.parquet"
FEATURE_SCHEMA_PATH = ARTIFACTS_DIR / "feature_schema.json"
MODEL_PATH = ARTIFACTS_DIR / "final_model_xgb.ubj"

COLORS = {
    "bg": "#F8FAFC",
    "primary": "#2E1A47",
    "secondary": "#1E1035",
    "muted": "#64748B",
    "card": "#FFFFFF",
    "border": "#E2E8F0",
    "danger": "#DC2626",
    "success": "#15803D",
    "warning": "#B45309",
}

RISK_THRESHOLDS = {
    "low_max": 0.30,
    "medium_max": 0.60,
}

DISPLAY_COLUMNS = [
    "TransactionAmt", "ProductCD", "card4", "card6",
    "hour", "P_emaildomain", "R_emaildomain",
    "DeviceType", "DeviceInfo",
]

HIDDEN_PREFIXES = ["V", "id_", "C", "D", "M"]

LANGUAGES = {"ar": "العربية", "en": "English"}
DEFAULT_LANG = "ar"

TRANSLATIONS = {
    "app_title": {
        "ar": "Fraud Signal Desk",
        "en": "Fraud Signal Desk",
    },
    "app_subtitle": {
        "ar": "مراجعة وتحليل المعاملات المشبوهة",
        "en": "Review and analyze suspicious transactions",
    },
    "page_overview": {
        "ar": "نظرة عامة",
        "en": "Overview",
    },
    "page_model": {
        "ar": "مراجعة المعاملات",
        "en": "Transaction Review",
    },
    "overview_title": {
        "ar": "أنماط الاحتيال في لمحة",
        "en": "Fraud patterns at a glance",
    },
    "overview_subtitle": {
        "ar": "تحليل أكثر من نصف مليون معاملة مالية من مجموعة بيانات IEEE-CIS",
        "en": "Analysis of over half a million financial transactions from the IEEE-CIS dataset",
    },
    "review_title": {
        "ar": "مراجعة معاملة",
        "en": "Review a transaction",
    },
    "review_subtitle": {
        "ar": "اختر عينة لفحص تقدير المخاطر من النموذج",
        "en": "Select a sample case to inspect the model's risk estimate",
    },
    "total_transactions": {
        "ar": "إجمالي المعاملات",
        "en": "Total Transactions",
    },
    "fraud_rate": {
        "ar": "نسبة الاحتيال",
        "en": "Fraud Rate",
    },
    "avg_fraud_amount": {
        "ar": "متوسط مبلغ الاحتيال",
        "en": "Avg Fraud Amount",
    },
    "what_we_found": {
        "ar": "ماذا اكتشفنا؟",
        "en": "What did we find?",
    },
    "hourly_chart_title": {
        "ar": "معدل الاحتيال حسب الساعة",
        "en": "Fraud rate by hour",
    },
    "hourly_chart_caption": {
        "ar": "كل عمود يمثل نسبة الاحتيال من إجمالي المعاملات في تلك الساعة",
        "en": "Each bar shows fraud cases as a share of all transactions in that hour",
    },
    "amount_chart_title": {
        "ar": "معدل الاحتيال حسب نطاق المبلغ",
        "en": "Fraud rate by amount band",
    },
    "amount_chart_caption": {
        "ar": "النسبة تعكس حصة الاحتيال من إجمالي المعاملات في كل نطاق",
        "en": "Rate reflects the share of fraud among all transactions in each band",
    },
    "data_context_title": {
        "ar": "عن البيانات",
        "en": "About the data",
    },
    "data_context_body": {
        "ar": "يعتمد النموذج على حقول مالية وتقنية إضافية مشفّرة لتحسين الدقة. الحقول مثل V1-V339 مخفية من الواجهة لأنها غير مقروءة للمستخدمين، بينما تبقى متاحة للنموذج.",
        "en": "The model relies on additional encoded financial and technical fields. Fields like V1-V339 are hidden from the interface because they are not readable to users, while they remain available to the model.",
    },
    "model_performance": {
        "ar": "أداء النموذج",
        "en": "Model Performance",
    },
    "precision_desc": {
        "ar": "من المعاملات المصنّفة كاحتيال، كم كانت فعلاً احتيالية؟",
        "en": "Of transactions flagged as fraud, how many were actually fraudulent?",
    },
    "recall_desc": {
        "ar": "من إجمالي حالات الاحتيال الفعلية، كم تم اكتشافها؟",
        "en": "Of all actual fraud cases, how many did the model catch?",
    },
    "f1_desc": {
        "ar": "التوازن بين الدقة والاسترجاع",
        "en": "The balance between Precision and Recall",
    },
    "auc_desc": {
        "ar": "قدرة النموذج على التمييز بين المعاملات الشرعية والاحتيالية",
        "en": "The model's ability to distinguish between legitimate and fraudulent transactions",
    },
    "fp_desc": {
        "ar": "معاملات شرعية صُنّفت خطأً كاحتيال",
        "en": "Legitimate transactions wrongly flagged as fraud",
    },
    "fn_desc": {
        "ar": "معاملات احتيالية لم يكتشفها النموذج",
        "en": "Fraudulent transactions the model missed",
    },
    "confusion_matrix": {
        "ar": "مصفوفة الارتباك",
        "en": "Confusion Matrix",
    },
    "cm_explanation": {
        "ar": "الإنذارات الكاذبة (FP) تزعج العملاء، والحالات المفقودة (FN) تعني خسائر مالية",
        "en": "False Positives (FP) inconvenience customers, while False Negatives (FN) mean financial losses",
    },
    "feature_importance": {
        "ar": "أهمية المتغيرات",
        "en": "Feature Importance",
    },
    "fi_caption": {
        "ar": "أهمية عامة للمتغيرات وليست تفسيراً لكل تنبؤ فردي",
        "en": "Overall feature importance, not a case-specific explanation",
    },
    "select_transaction": {
        "ar": "اختر معاملة",
        "en": "Select a transaction",
    },
    "analyze_btn": {
        "ar": "تحليل المعاملة",
        "en": "Analyze transaction",
    },
    "readable_note": {
        "ar": "الحقول المقروءة فقط معروضة هنا؛ النموذج يستخدم حقولاً إضافية في الخلفية",
        "en": "Only readable fields are shown; the model uses additional features in the background",
    },
    "risk_result_title": {
        "ar": "تقدير المخاطر",
        "en": "Risk Assessment",
    },
    "estimated_fraud_risk": {
        "ar": "احتمالية الاحتيال المقدرة",
        "en": "Estimated fraud risk",
    },
    "model_recommendation_note": {
        "ar": "هذا التقدير يدعم المراجعة وليس قراراً نهائياً",
        "en": "This score supports review and is not a final decision",
    },
    "risk_low": {
        "ar": "مخاطر منخفضة",
        "en": "Low risk",
    },
    "risk_medium": {
        "ar": "يحتاج مراجعة",
        "en": "Needs review",
    },
    "risk_high": {
        "ar": "مشبوه، يتطلب مراجعة",
        "en": "Suspicious, requires review",
    },
    "signals_title": {
        "ar": "إشارات في هذه المعاملة",
        "en": "Signals in this case",
    },
    "signals_tooltip": {
        "ar": "هذه إشارات مبنية على الحقول المقروءة للمعاملة المحددة",
        "en": "These signals are based on the readable fields of the selected transaction",
    },
    "no_signals": {
        "ar": "لا توجد إشارات مقروءة لهذه المعاملة",
        "en": "No readable signals available for this transaction",
    },
    "factors_title": {
        "ar": "إشارات في هذه المعاملة",
        "en": "Signals in this case",
    },
    "actual_label": {
        "ar": "التصنيف الفعلي",
        "en": "Actual Label",
    },
    "is_fraud": {
        "ar": "احتيالية",
        "en": "Fraudulent",
    },
    "is_legit": {
        "ar": "شرعية",
        "en": "Legitimate",
    },
    "predicted": {
        "ar": "المتوقع",
        "en": "Predicted",
    },
    "actual": {
        "ar": "الفعلي",
        "en": "Actual",
    },
    "truth_reveal_title": {
        "ar": "هل أصاب النموذج؟",
        "en": "Did the model get it right?",
    },
    "amount": {
        "ar": "المبلغ",
        "en": "Amount",
    },
    "hour_label": {
        "ar": "الوقت",
        "en": "Time",
    },
    "device": {
        "ar": "الجهاز",
        "en": "Device",
    },
    "email_domain": {
        "ar": "نطاق البريد",
        "en": "Email domain",
    },
    "card_type": {
        "ar": "نوع البطاقة",
        "en": "Card type",
    },
    "card_network": {
        "ar": "شبكة البطاقة",
        "en": "Card network",
    },
    "product": {
        "ar": "سياق الدفع",
        "en": "Payment context",
    },
    "not_available": {
        "ar": "غير متوفر",
        "en": "Not available",
    },
    "language_label": {
        "ar": "اللغة",
        "en": "Language",
    },
    "normal": {
        "ar": "طبيعي",
        "en": "Normal",
    },
    "needs_review": {
        "ar": "يحتاج مراجعة",
        "en": "Needs review",
    },
    "high_risk": {
        "ar": "مخاطر عالية",
        "en": "High risk",
    },
    "fraud_count": {
        "ar": "عدد حالات الاحتيال",
        "en": "Fraud Count",
    },
    "legit_count": {
        "ar": "المعاملات الشرعية",
        "en": "Legitimate Transactions",
    },
    "fraud_label": {
        "ar": "احتيال",
        "en": "Fraud",
    },
    "legit_label": {
        "ar": "شرعي",
        "en": "Legitimate",
    },
    "risk_gauge_title": {
        "ar": "احتمالية الاحتيال",
        "en": "Fraud Probability",
    },
    "sample_id_label": {
        "ar": "عينة",
        "en": "Sample",
    },
    "browse_samples": {
        "ar": "تصفح العينات العشرين",
        "en": "Browse the 20 demo cases",
    },
    "diagnostics_title": {
        "ar": "تشخيصات النموذج",
        "en": "Model Diagnostics",
    },
    "performance_snapshot": {
        "ar": "ملخص الأداء",
        "en": "Performance Snapshot",
    },
    "tab_confusion": {
        "ar": "مصفوفة الارتباك",
        "en": "Confusion Matrix",
    },
    "tab_importance": {
        "ar": "أهمية المتغيرات",
        "en": "Feature Importance",
    },
    "methodology": {
        "ar": "المنهجية",
        "en": "Methodology",
    },
    "limitations": {
        "ar": "القيود",
        "en": "Limitations",
    },
    "methodology_body": {
        "ar": "تم تدريب نموذج XGBoost باستخدام التحقق الزمني (5 طيات). تم اختيار أفضل عتبة بناءً على F1-Score. لا يُستخدم PCA ولا يتم حذف المتغيرات المرتبطة.",
        "en": "XGBoost model trained with time-based validation (5 folds). Best threshold selected based on F1-Score. No PCA used and no correlated features deleted.",
    },
    "limitations_body": {
        "ar": "العينات المعروضة محدودة (20 معاملة). التفسيرات المحلية غير متاحة، الإشارات المعروضة مبنية على الحقول المقروءة فقط وليست تفسيراً كاملاً لقرار النموذج.",
        "en": "Displayed samples are limited (20 transactions). Local explanations are not available; shown signals are based on readable fields only, not a full explanation of the model's decision.",
    },
    "hour_hover": {
        "ar": "الساعة",
        "en": "Hour",
    },
    "fraud_rate_hover": {
        "ar": "معدل الاحتيال",
        "en": "Fraud rate",
    },
    "fraud_cases_hover": {
        "ar": "حالات الاحتيال",
        "en": "Fraud cases",
    },
    "all_transactions_hover": {
        "ar": "إجمالي المعاملات",
        "en": "All transactions",
    },
    "amount_band_hover": {
        "ar": "نطاق المبلغ",
        "en": "Amount band",
    },
    "model_quality_title": {
        "ar": "ما مدى موثوقية النموذج؟",
        "en": "How reliable is the model?",
    },
    "model_quality_help": {
        "ar": "هذه المقاييس توضح مدى جودة النموذج في اكتشاف الاحتيال على مجموعة البيانات المتاحة",
        "en": "These metrics show how well the model detects fraud on the available dataset",
    },
    "advanced_evidence": {
        "ar": "تفاصيل تقنية متقدمة",
        "en": "Advanced model evidence",
    },
    "fi_limitation": {
        "ar": "أسماء المتغيرات المشفّرة (مثل V258) ليست وصفاً مقروءاً. هذا ترتيب تقني عام وليس تفسيراً لكل حالة.",
        "en": "Encoded feature names (like V258) are not human-readable descriptions. This is an overall technical ranking, not a case-specific explanation.",
    },
    "hourly_story_title": {
        "ar": "متى تكون المعاملات أكثر عرضة للخطر؟",
        "en": "When are transactions most at risk?",
    },
    "hourly_story_subtitle": {
        "ar": "أعلى معدل احتيال مُلاحظ: {rate}% عند الساعة {hour}:00",
        "en": "Highest observed fraud rate: {rate}% at {hour}:00",
    },
    "volume_label": {
        "ar": "حجم المعاملات",
        "en": "Transaction volume",
    },
    "rate_label": {
        "ar": "معدل الاحتيال",
        "en": "Fraud rate",
    },
    "chart_key_note": {
        "ar": "ساعة مزدحمة لا تعني تلقائياً ساعة عالية الخطورة",
        "en": "A busy hour is not automatically a high-risk hour",
    },
    "correct_classification": {
        "ar": "تصنيف صحيح",
        "en": "Correct classification",
    },
    "misclassified_case": {
        "ar": "حالة مصنّفة خطأً",
        "en": "Misclassified case",
    },
    "actual_outcome": {
        "ar": "النتيجة الفعلية",
        "en": "Actual outcome",
    },
    "model_prediction_label": {
        "ar": "تنبؤ النموذج",
        "en": "Model prediction",
    },
    "correct_match_note": {
        "ar": "تنبؤ النموذج يطابق التصنيف الفعلي لهذه العينة",
        "en": "The model's predicted class matches this demo sample's known label",
    },
    "false_negative_note": {
        "ar": "حالة احتيال فائتة (سلبي خاطئ)",
        "en": "Missed fraud case (false negative)",
    },
    "false_positive_note": {
        "ar": "مراجعة غير ضرورية (إيجابي خاطئ)",
        "en": "Unnecessary review (false positive)",
    },
    "validation_help": {
        "ar": "يقارن هذا تنبؤ النموذج بالتصنيف الحقيقي المعروف لعينة العرض التوضيحي",
        "en": "This compares the model's prediction against the known ground-truth label of the demo sample",
    },
    "observed_cues_title": {
        "ar": "إشارات سياقية مُلاحظة",
        "en": "Observed case cues",
    },
    "observed_cues_help": {
        "ar": "هذه إشارات سياقية مبنية على بيانات المعاملة وليست تفسيراً مباشراً لقرار النموذج. النموذج يستخدم حقولاً إضافية مشفّرة.",
        "en": "These are contextual cues based on the transaction data, not a direct explanation of the model's decision. The model uses additional encoded features.",
    },
    "no_cues": {
        "ar": "لا تتوفر إشارات مقروءة لهذه العينة. التقدير يعتمد أيضاً على حقول مشفّرة.",
        "en": "No readable risk cues are available for this sample; the score also uses encoded background features.",
    },
    "raises_risk": {
        "ar": "يرفع المخاطر",
        "en": "Raises risk",
    },
    "reduces_risk": {
        "ar": "يقلل المخاطر",
        "en": "Reduces risk",
    },
    "neutral_context": {
        "ar": "سياق محايد",
        "en": "Neutral context",
    },
    "why_this_result": {
        "ar": "لماذا هذه النتيجة؟",
        "en": "Why this result?",
    },
    "previous_page": {
        "ar": "السابق",
        "en": "Previous",
    },
    "next_page": {
        "ar": "التالي",
        "en": "Next",
    },
    "case_facts_title": {
        "ar": "تفاصيل المعاملة المحددة",
        "en": "Selected case details",
    },
    "review_instruction": {
        "ar": "اختر عينة من البطاقات أدناه ثم اضغط تحليل",
        "en": "Select a sample from the cards below, then press Analyze",
    },
    "risk_help": {
        "ar": "هذا احتمال تقديري من النموذج. العتبات: أقل من 30% منخفض، 30-60% يحتاج مراجعة، أعلى من 60% مشبوه. هذا تقدير وليس قرار نهائي.",
        "en": "This is an estimated probability from the model. Thresholds: below 30% is low risk, 30-60% needs review, above 60% is suspicious. This is an estimate, not a final decision.",
    },
    "cm_help": {
        "ar": "مصفوفة الارتباك تقارن تنبؤات النموذج بالنتائج الفعلية. الإيجابي الخاطئ يعني إزعاج عميل، السلبي الخاطئ يعني خسارة مالية.",
        "en": "The confusion matrix compares model predictions with actual outcomes. A false positive means an inconvenienced customer, a false negative means financial loss.",
    },
    "f1_help": {
        "ar": "F1-Score هو المتوسط التوافقي بين الدقة والاسترجاع. قيمة أعلى تعني توازناً أفضل.",
        "en": "F1-Score is the harmonic mean of Precision and Recall. A higher value means a better balance.",
    },
    "auc_help": {
        "ar": "ROC-AUC يقيس قدرة النموذج على التمييز بين الفئتين. 1.0 مثالي، 0.5 عشوائي.",
        "en": "ROC-AUC measures the model's ability to distinguish between classes. 1.0 is perfect, 0.5 is random.",
    },
    "recall_help": {
        "ar": "الاسترجاع هو نسبة حالات الاحتيال الفعلية التي اكتشفها النموذج.",
        "en": "Recall is the proportion of actual fraud cases the model successfully detected.",
    },
    "hourly_help": {
        "ar": "يعرض الرسم العلوي حجم المعاملات لكل ساعة، والسفلي معدل الاحتيال. ساعة مزدحمة ليست بالضرورة عالية الخطورة.",
        "en": "The upper panel shows transaction volume per hour, the lower shows fraud rate. A busy hour is not necessarily high-risk.",
    },
    "signals_help": {
        "ar": "هذه إشارات سياقية من الحقول المقروءة وليست تفسيراً مباشراً لقرار النموذج",
        "en": "These are contextual cues from readable fields, not a direct explanation of the model's decision",
    },
}

UI_STRINGS = {
    "hourly_key_note": ("A busy hour is not automatically a high-risk hour", "الساعة المزدحمة ليست بالضرورة ساعة عالية الخطورة"),
    "hourly_headline": ("Highest observed fraud rate, at {hour}", "أعلى معدل احتيال مُلاحظ، عند الساعة {hour}"),
    "cm_subtitle": ("How the model's predictions compare with the actual outcome", "كيف تقارن تنبؤات النموذج بالنتائج الفعلية"),
    "adv_caption": ("Top features by overall importance", "أهم المتغيرات حسب الأهمية الإجمالية"),
    "fi_unavailable": ("Feature importance data not available", "بيانات أهمية المتغيرات غير متوفرة"),
    "f1_tt": ("F1-Score {v}: balance of precision and recall", "F1-Score {v}: التوازن بين الدقة والاسترجاع"),
    "auc_tt": ("ROC-AUC {v}: how well the model separates the two classes", "ROC-AUC {v}: قدرة النموذج على التمييز بين الفئتين"),
    "recall_tt": ("Recall {v}: the model catches about {p}% of all fraud", "Recall {v}: النموذج يكتشف نحو {p}% من حالات الاحتيال"),
    "cm_tn_q": ("Predicted <em>legit</em> → it was <em>legit</em>", "تنبأ <em>شرعي</em> ← والفعلي <em>شرعي</em>"),
    "cm_tp_q": ("Predicted <em>fraud</em> → it was <em>fraud</em>", "تنبأ <em>احتيال</em> ← والفعلي <em>احتيال</em>"),
    "cm_fp_q": ("Predicted <em>fraud</em> → it was <em>legit</em>", "تنبأ <em>احتيال</em> ← والفعلي <em>شرعي</em>"),
    "cm_fn_q": ("Predicted <em>legit</em> → it was <em>fraud</em>", "تنبأ <em>شرعي</em> ← والفعلي <em>احتيال</em>"),
    "cm_tn_res": ("The customer pays without friction", "العميل يدفع بدون إزعاج"),
    "cm_tp_res": ("The company's money is protected", "أموال الشركة محمية"),
    "cm_fp_res": ("An honest customer gets blocked and annoyed", "عميل صادق يتعطل ويشعر بالإزعاج"),
    "cm_fn_res": ("The fraud slips through and the company loses money", "الاحتيال يمر والشركة تخسر"),
    "step1_title": ("Choose a sample", "اختر عينة"),
    "step_range": ("Showing samples {a}–{b}", "عرض العينات {a}–{b}"),
    "sample_label": ("Sample {id}", "عينة {id}"),
    "card_time": ("Time", "الوقت"),
    "card_product": ("Product", "المنتج"),
    "card_device": ("Device", "الجهاز"),
    "card_card": ("Card", "البطاقة"),
    "card_email": ("Email", "البريد"),
    "select_btn": ("Select", "اختيار"),
    "selected_btn": ("✓ Selected", "✓ محدّدة"),
    "page_of": ("Page {a} of {b}", "صفحة {a} من {b}"),
    "prev_help": ("Previous samples", "العينات السابقة"),
    "next_help": ("Next samples", "العينات التالية"),
    "analyzing": ("Analyzing…", "جارٍ التحليل…"),
    "empty_results": ("Select a sample and press Analyze to see the results", "اختر عينة واضغط تحليل لعرض النتائج"),
    "stale_results": ("Results show Sample {id}. Press Analyze to update.", "النتائج المعروضة للعينة {id}. اضغط تحليل للتحديث."),
    "samples_unavailable": ("Sample transactions not available", "العينات غير متوفرة"),
    "prob_unavailable": ("Could not compute fraud probability for this transaction.", "تعذّر حساب احتمالية الاحتيال لهذه المعاملة."),
    "step2_title": ("Results for Sample {id}", "نتائج العينة {id}"),
    "details_title": ("Transaction details", "تفاصيل المعاملة"),
    "det_sample_id": ("Sample ID", "رقم العينة"),
    "det_amount": ("Amount", "المبلغ"),
    "det_time": ("Time", "الوقت"),
    "det_product": ("Product", "المنتج"),
    "det_device": ("Device", "الجهاز"),
    "det_card": ("Card", "البطاقة"),
    "det_network": ("Network", "شبكة"),
    "det_email": ("Email", "البريد"),
    "actual_outcome_lbl": ("Actual outcome", "النتيجة الفعلية"),
    "model_prediction_lbl": ("Model prediction", "تنبؤ النموذج"),
    "false_negative": ("False negative", "سلبي خاطئ"),
    "false_positive": ("False positive", "إيجابي خاطئ"),
    "chart_vol_title": ("Transactions per hour", "المعاملات لكل ساعة"),
    "chart_rate_title": ("Fraud rate (%)", "معدل الاحتيال (%)"),
    "chart_x_title": ("Hour of day", "ساعة اليوم"),
    "chart_vol_name": ("Transaction volume", "حجم المعاملات"),
    "chart_rate_name": ("Fraud rate", "معدل الاحتيال"),
    "chart_above_name": ("Above high-risk level", "فوق مستوى الخطر"),
    "chart_baseline_name": ("Baseline {rate}%", "المستوى الأساسي {rate}%"),
    "chart_window": ("High-risk window {label}", "نافذة الخطورة {label}"),
    "cues_note": (
        "A simplified reading of this transaction's visible details. The model itself weighs hundreds of features together, so these cues show context, not its actual reasoning.",
        "قراءة مبسّطة للتفاصيل الظاهرة في المعاملة. المودل نفسه يوازن مئات المتغيرات مع بعض، فهذه الإشارات توضح السياق وليست طريقة تفكيره الفعلية.",
    ),
    "risk_help_dynamic": (
        "This is the model's estimated probability. The model flags a transaction as fraud from {t}% and up (the threshold that gave the best F1 on the evaluation month). Above {h}% is treated as suspicious. This is an estimate, not a final decision.",
        "هذا احتمال تقديري من النموذج. النموذج يصنّف المعاملة احتيال من {t}% وفوق (العتبة اللي أعطت أفضل F1 في شهر التقييم). فوق {h}% تعتبر مشبوهة. هذا تقدير وليس قرار نهائي.",
    ),
    "card_txn_id": ("Transaction ID", "رقم المعاملة"),
    "det_txn_id": ("Transaction ID", "رقم المعاملة"),
    "chart_transactions": ("Transactions", "المعاملات"),
    "gauge_low": ("Low", "منخفض"),
    "gauge_medium": ("Medium", "متوسط"),
    "gauge_high": ("High", "عالي"),
    "cm_legit": ("Legit", "شرعي"),
    "cm_fraud": ("Fraud", "احتيال"),
    "cm_pred_axis": ("Predicted", "المتوقع"),
    "cm_actual_axis": ("Actual", "الفعلي"),
    "cm_fn_short": ("Fraud missed", "احتيال فات النموذج"),
    "cm_tp_short": ("Fraud caught", "احتيال مكتشف"),
    "cm_tn_short": ("Legit cleared", "تصنيف شرعي صحيح"),
    "cm_fp_short": ("False alarm", "إنذار خاطئ"),
    "cm_count": ("Count", "العدد"),
    "cm_share": ("Share of all transactions", "النسبة من كل المعاملات"),
    "cm_meaning": ("Meaning", "المعنى"),
    "fi_x_title": ("Importance", "الأهمية"),
}

for _k, (_en, _ar) in UI_STRINGS.items():
    TRANSLATIONS.setdefault(_k, {"en": _en, "ar": _ar})


def t(key, lang=DEFAULT_LANG):
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", key))
