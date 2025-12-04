"""
لوحة تحكم المبيعات الذكية - تعمل مع عدة ملفات Excel
الإصدار: 1.0.0 - مع دعم متعدد الملفات
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import tempfile
from datetime import datetime
from io import BytesIO

# استيراد الوحدات الخاصة بالمبيعات
from sales_auto_mapper import SalesAutoColumnMapper
from sales_analyzer import SalesDataAnalyzer
from sales_visualizer import SalesVisualizer

# إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم المبيعات الذكية",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== نظام الترجمة الكامل ====================
class SalesTranslationSystem:
    """نظام الترجمة ثنائي اللغة للمبيعات"""
    
    translations = {
        'ar': {
            # العنوان الرئيسي
            'main_title': '📈 لوحة تحكم المبيعات الذكية',
            'main_subtitle': 'تعمل مع <strong>عدة ملفات Excel</strong> - قم برفع ملفاتك وسنحلل بيانات المبيعات تلقائياً',
            
            # الشريط الجانبي
            'sidebar_settings': '⚙️ إعدادات',
            'sidebar_language': 'اللغة:',
            'sidebar_theme': 'المظهر:',
            'sidebar_load_settings': '📥 تحميل إعدادات سابقة',
            'sidebar_save_settings': '💾 حفظ الإعدادات',
            'sidebar_load_success': 'تم تحميل الإعدادات السابقة',
            'sidebar_save_success': 'تم حفظ الإعدادات',
            'sidebar_no_settings': 'لا توجد إعدادات سابقة',
            
            # رفع الملفات
            'upload_title': '📤 الخطوة 1: رفع ملفات المبيعات',
            'upload_placeholder': 'اسحب وأفلت ملفات Excel هنا أو انقر للاختيار',
            'upload_help': 'يدعم الملفات: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ تم تحميل {count} ملف بنجاح!',
            'upload_error': '❌ خطأ في تحميل الملف:',
            'preview_data': '👀 معاينة البيانات (أول 5 صفوف)',
            'merge_files': '🔗 دمج الملفات',
            'merged_success': '✅ تم دمج الملفات بنجاح!',
            'select_files': 'اختر ملفات',
            
            # إحصائيات
            'stats_records': 'عدد السجلات',
            'stats_columns': 'عدد الأعمدة',
            'stats_numeric': 'أعمدة رقمية',
            'stats_files': 'عدد الملفات',
            
            # تعيين الأعمدة
            'mapping_title': '🎯 الخطوة 2: تعيين الأعمدة',
            'mapping_auto': '💡 <strong>التعرف التلقائي</strong>: النظام حاول تخمين أنواع الأعمدة. يمكنك تعديلها يدوياً إذا كانت غير صحيحة.',
            
            # فئات الأعمدة
            'cat_order_info': 'معلومات الطلب',
            'cat_customer_info': 'معلومات العميل',
            'cat_product_info': 'معلومات المنتج',
            'cat_financial': 'المعلومات المالية',
            'cat_location': 'الموقع',
            'cat_sales_info': 'معلومات المبيعات',
            
            # أسماء الحقول
            'field_order_id': 'رقم الطلب',
            'field_customer_name': 'اسم العميل',
            'field_customer_id': 'رقم العميل',
            'field_product_name': 'اسم المنتج',
            'field_product_id': 'رقم المنتج',
            'field_category': 'الفئة',
            'field_quantity': 'الكمية',
            'field_unit_price': 'سعر الوحدة',
            'field_total_price': 'إجمالي السعر',
            'field_order_date': 'تاريخ الطلب',
            'field_region': 'المنطقة',
            'field_city': 'المدينة',
            'field_country': 'البلد',
            'field_salesperson': 'مندوب المبيعات',
            'field_payment_method': 'طريقة الدفع',
            'field_discount': 'الخصم',
            'field_profit': 'الربح',
            'field_cost': 'التكلفة',
            'field_status': 'حالة الطلب',
            
            # زر التحليل
            'analyze_button': '🚀 انتقل إلى التحليل',
            
            # نتائج التحليل
            'analysis_title': '📊 الخطوة 3: تحليل بيانات المبيعات',
            'kpis_title': '📈 النتائج الرئيسية',
            'charts_title': '📊 الرسوم البيانية التلقائية',
            'advanced_title': '🔍 تحليل متقدم',
            'correlations_title': 'العلاقات بين المتغيرات',
            'outliers_title': 'اكتشاف القيم الشاذة',
            'outliers_found': 'تم اكتشاف {} قيمة شاذة في المبيعات',
            'no_outliers': '✅ لم يتم اكتشاف قيم شاذة في المبيعات',
            'zero_std': 'انحراف المبيعات المعياري صفر، لا يمكن اكتشاف قيم شاذة',
            
            # تصدير
            'export_data': '📥 تحميل البيانات المعدلة (CSV)',
            'export_report': '📄 تحميل التقرير الكامل',
            'download_csv': '⬇️ انقر للتحميل',
            'download_report': '⬇️ انقر للتحميل',
            
            # رسائل أخرى
            'loading': 'جاري التحميل...',
            'not_available': 'غير متوفر',
            'file_info': '📄 معلومات الملف',
            'total_rows': 'إجمالي الصفوف',
            'total_columns': 'إجمالي الأعمدة',
            'merged_data': 'بيانات مدمجة',
            'individual_files': 'ملفات فردية',
        },
        'en': {
            # Main Title
            'main_title': '📈 Smart Sales Analytics Dashboard',
            'main_subtitle': 'Works with <strong>multiple Excel files</strong> - Upload your files and we will automatically analyze sales data',
            
            # Sidebar
            'sidebar_settings': '⚙️ Settings',
            'sidebar_language': 'Language:',
            'sidebar_theme': 'Theme:',
            'sidebar_load_settings': '📥 Load Previous Settings',
            'sidebar_save_settings': '💾 Save Settings',
            'sidebar_load_success': 'Previous settings loaded',
            'sidebar_save_success': 'Settings saved',
            'sidebar_no_settings': 'No previous settings',
            
            # File Upload
            'upload_title': '📤 Step 1: Upload Sales Files',
            'upload_placeholder': 'Drag and drop Excel files here or click to browse',
            'upload_help': 'Supports: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ {count} files uploaded successfully!',
            'upload_error': '❌ Error loading file:',
            'preview_data': '👀 Data Preview (First 5 rows)',
            'merge_files': '🔗 Merge Files',
            'merged_success': '✅ Files merged successfully!',
            'select_files': 'Select Files',
            
            # Statistics
            'stats_records': 'Number of Records',
            'stats_columns': 'Number of Columns',
            'stats_numeric': 'Numeric Columns',
            'stats_files': 'Number of Files',
            
            # Column Mapping
            'mapping_title': '🎯 Step 2: Map Columns',
            'mapping_auto': '💡 <strong>Auto-detection</strong>: System tried to guess column types. You can adjust manually if incorrect.',
            
            # Column Categories
            'cat_order_info': 'Order Information',
            'cat_customer_info': 'Customer Information',
            'cat_product_info': 'Product Information',
            'cat_financial': 'Financial Information',
            'cat_location': 'Location',
            'cat_sales_info': 'Sales Information',
            
            # Field Names
            'field_order_id': 'Order ID',
            'field_customer_name': 'Customer Name',
            'field_customer_id': 'Customer ID',
            'field_product_name': 'Product Name',
            'field_product_id': 'Product ID',
            'field_category': 'Category',
            'field_quantity': 'Quantity',
            'field_unit_price': 'Unit Price',
            'field_total_price': 'Total Price',
            'field_order_date': 'Order Date',
            'field_region': 'Region',
            'field_city': 'City',
            'field_country': 'Country',
            'field_salesperson': 'Salesperson',
            'field_payment_method': 'Payment Method',
            'field_discount': 'Discount',
            'field_profit': 'Profit',
            'field_cost': 'Cost',
            'field_status': 'Order Status',
            
            # Analysis Button
            'analyze_button': '🚀 Proceed to Analysis',
            
            # Analysis Results
            'analysis_title': '📊 Step 3: Sales Data Analysis',
            'kpis_title': '📈 Key Results',
            'charts_title': '📊 Automatic Charts',
            'advanced_title': '🔍 Advanced Analysis',
            'correlations_title': 'Variable Correlations',
            'outliers_title': 'Outlier Detection',
            'outliers_found': 'Found {} outliers in sales',
            'no_outliers': '✅ No outliers detected in sales',
            'zero_std': 'Sales standard deviation is zero, cannot detect outliers',
            
            # Export
            'export_data': '📥 Download Modified Data (CSV)',
            'export_report': '📄 Download Full Report',
            'download_csv': '⬇️ Click to Download',
            'download_report': '⬇️ Click to Download',
            
            # Other Messages
            'loading': 'Loading...',
            'not_available': 'Not Available',
            'file_info': '📄 File Information',
            'total_rows': 'Total Rows',
            'total_columns': 'Total Columns',
            'merged_data': 'Merged Data',
            'individual_files': 'Individual Files',
        }
    }
    
    @staticmethod
    def get_translation(key, language='ar'):
        """الحصول على ترجمة المفتاح باللغة المطلوبة"""
        lang_data = SalesTranslationSystem.translations.get(language, SalesTranslationSystem.translations['ar'])
        return lang_data.get(key, key)
    
    @staticmethod
    def translate(key, **kwargs):
        """ترجمة المفتاح بناءً على اللغة الحالية"""
        language = st.session_state.get('language', 'ar')
        text = SalesTranslationSystem.get_translation(key, language)
        return text.format(**kwargs) if kwargs else text

# تهيئة نظام الترجمة
translator = SalesTranslationSystem()

# تحميل CSS مع دعم متعدد اللغات
def load_sales_css(language='ar'):
    """تحميل CSS مع دعم اتجاه النص"""
    text_align = 'right' if language == 'ar' else 'left'
    font_family = "'Cairo', 'Segoe UI', Tahoma, sans-serif" if language == 'ar' else "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    
    css = f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        font-family: {font_family};
    }}
    
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        font-family: {font_family};
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .upload-box {{
        border: 2px dashed #4F46E5;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        background: #f7fafc;
        margin: 20px 0;
        font-family: {font_family};
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    .file-card {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-family: {font_family};
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    .warning-box {{
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: {font_family};
        direction: {'rtl' if language == 'ar' else 'ltr'};
    }}
    
    /* تنسيق عام للصفحة */
    .stApp {{
        font-family: {font_family};
        text-align: {text_align};
    }}
    
    /* تنسيق الأزرار */
    .stButton > button {{
        border-radius: 8px;
        font-family: {font_family};
    }}
    
    /* تنسيق حقول الإدخال */
    .stSelectbox, .stTextInput, .stNumberInput {{
        font-family: {font_family};
    }}
    </style>
    
    <!-- تحميل خط Cairo للعربية -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    """
    st.markdown(css, unsafe_allow_html=True)

# وظائف لتحميل الملفات المتعددة
def load_multiple_files(uploaded_files):
    """تحميل عدة ملفات Excel/CSV"""
    dataframes = []
    file_info_list = []
    
    for uploaded_file in uploaded_files:
        try:
            # تحديد نوع الملف
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.csv'):
                # محاولة ترميزات مختلفة لملفات CSV
                content = uploaded_file.getvalue()
                encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1256', 'windows-1256']
                
                for encoding in encodings:
                    try:
                        df = pd.read_csv(BytesIO(content), encoding=encoding)
                        break
                    except:
                        continue
                else:
                    df = pd.read_csv(BytesIO(content), encoding='utf-8', errors='ignore')
                    
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                st.error(f"نوع الملف غير مدعوم: {file_name}")
                continue
            
            # حفظ معلومات الملف
            file_info = {
                'name': uploaded_file.name,
                'size': len(uploaded_file.getvalue()),
                'rows': len(df),
                'columns': len(df.columns),
                'dataframe': df
            }
            
            file_info_list.append(file_info)
            dataframes.append(df)
            
        except Exception as e:
            st.error(f"{translator.translate('upload_error')} {uploaded_file.name}: {str(e)}")
    
    return dataframes, file_info_list

def merge_dataframes(dataframes):
    """دمج عدة dataframes في dataframe واحد"""
    if not dataframes:
        return None
    
    try:
        # محاولة الدمج مع معالجة أسماء الأعمدة المختلفة
        merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
        return merged_df
    except Exception as e:
        st.error(f"خطأ في دمج الملفات: {str(e)}")
        return None

# تهيئة حالة الجلسة
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'files_uploaded' not in st.session_state:
    st.session_state.files_uploaded = False
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = []
if 'file_info_list' not in st.session_state:
    st.session_state.file_info_list = []
if 'merged_df' not in st.session_state:
    st.session_state.merged_df = None
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'use_merged' not in st.session_state:
    st.session_state.use_merged = False

# وظائف تبديل اللغة والمظهر
def toggle_language():
    st.session_state.language = 'en' if st.session_state.language == 'ar' else 'ar'
    st.rerun()

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# تحميل CSS بناءً على اللغة
load_sales_css(st.session_state.language)

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### {translator.translate('sidebar_settings')}")
    
    # تبديل اللغة
    current_lang = 'العربية' if st.session_state.language == 'en' else 'English'
    lang_button = st.button(f"🌐 {current_lang}", use_container_width=True)
    if lang_button:
        toggle_language()
    
    # تبديل المظهر
    current_theme = '🌙 مظلم' if st.session_state.theme == 'light' else '☀️ فاتح'
    theme_button = st.button(current_theme, use_container_width=True)
    if theme_button:
        toggle_theme()
    
    st.divider()
    
    # تحميل الإعدادات السابقة
    if st.button(translator.translate('sidebar_load_settings'), use_container_width=True):
        if os.path.exists('sales_config.json'):
            with open('sales_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                st.session_state.column_mapping = config.get('column_mapping', {})
                st.success(translator.translate('sidebar_load_success'))
        else:
            st.warning(translator.translate('sidebar_no_settings'))
    
    # حفظ الإعدادات
    if st.session_state.column_mapping:
        if st.button(translator.translate('sidebar_save_settings'), use_container_width=True):
            config = {
                'column_mapping': st.session_state.column_mapping,
                'saved_at': datetime.now().isoformat(),
                'language': st.session_state.language,
                'theme': st.session_state.theme
            }
            with open('sales_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            st.success(translator.translate('sidebar_save_success'))

# ==================== العنوان الرئيسي ====================
st.markdown(f"""
<div class="main-header">
    <h1>{translator.translate('main_title')}</h1>
    <p>{translator.translate('main_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== تحميل الملفات المتعددة ====================
st.markdown(f"## {translator.translate('upload_title')}")

uploaded_files = st.file_uploader(
    translator.translate('upload_placeholder'),
    type=['xlsx', 'xls', 'csv'],
    help=translator.translate('upload_help'),
    accept_multiple_files=True,
    key="sales_file_uploader"
)

if uploaded_files and len(uploaded_files) > 0:
    try:
        # تحميل الملفات المتعددة
        with st.spinner(translator.translate('loading')):
            dataframes, file_info_list = load_multiple_files(uploaded_files)
        
        if dataframes and file_info_list:
            st.session_state.dataframes = dataframes
            st.session_state.file_info_list = file_info_list
            st.session_state.files_uploaded = True
            
            st.success(translator.translate('upload_success', count=len(dataframes)))
            
            # عرض معلومات الملفات
            st.markdown(f"### 📁 {translator.translate('file_info')}")
            
            for i, file_info in enumerate(file_info_list):
                with st.expander(f"{file_info['name']} ({file_info['rows']} صفوف، {file_info['columns']} أعمدة)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("حجم الملف", f"{file_info['size']:,} بايت")
                    with col2:
                        st.metric(translator.translate('stats_records'), file_info['rows'])
                    with col3:
                        st.metric(translator.translate('stats_columns'), file_info['columns'])
                    
                    # معاينة البيانات
                    if st.checkbox(f"معاينة {file_info['name']}", key=f"preview_{i}"):
                        st.dataframe(file_info['dataframe'].head(), use_container_width=True)
            
            # خيارات دمج الملفات
            if len(dataframes) > 1:
                st.markdown("### 🔗 خيارات الدمج")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(translator.translate('merge_files'), use_container_width=True):
                        merged_df = merge_dataframes(dataframes)
                        if merged_df is not None:
                            st.session_state.merged_df = merged_df
                            st.session_state.use_merged = True
                            st.session_state.current_df = merged_df
                            st.success(translator.translate('merged_success'))
                
                with col2:
                    if st.button(translator.translate('individual_files'), use_container_width=True):
                        st.session_state.use_merged = False
                        st.session_state.current_df = dataframes[0]
                        st.info("جارٍ استخدام الملف الأول فقط")
            
            # تحديد البيانات التي سيتم استخدامها
            if not st.session_state.current_df:
                if st.session_state.merged_df is not None:
                    st.session_state.current_df = st.session_state.merged_df
                    st.session_state.use_merged = True
                else:
                    st.session_state.current_df = dataframes[0]
                    st.session_state.use_merged = False
            
            # عرض إحصائيات البيانات
            df_to_use = st.session_state.current_df
            
            if st.session_state.use_merged and st.session_state.merged_df is not None:
                st.info(f"📊 **{translator.translate('merged_data')}**: {len(df_to_use)} سجل، {len(df_to_use.columns)} عمود")
            else:
                st.info(f"📊 **{translator.translate('individual_files')}**: {len(df_to_use)} سجل، {len(df_to_use.columns)} عمود")
            
            # عرض عينة من البيانات
            with st.expander(translator.translate('preview_data')):
                st.dataframe(df_to_use.head(), use_container_width=True)
            
            # عرض معلومات البيانات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(translator.translate('stats_files'), len(dataframes))
            with col2:
                st.metric(translator.translate('stats_records'), len(df_to_use))
            with col3:
                st.metric(translator.translate('stats_columns'), len(df_to_use.columns))
            with col4:
                numeric_cols = df_to_use.select_dtypes(include=[np.number]).columns.tolist()
                st.metric(translator.translate('stats_numeric'), len(numeric_cols))
        
    except Exception as e:
        st.error(f"{translator.translate('upload_error')} {str(e)}")

# ==================== تعيين أعمدة المبيعات ====================
if st.session_state.files_uploaded and st.session_state.current_df is not None:
    st.markdown(f"## {translator.translate('mapping_title')}")
    
    df = st.session_state.current_df
    columns = df.columns.tolist()
    
    # التعرف التلقائي على الأعمدة
    mapper = SalesAutoColumnMapper(df)
    auto_suggestions = mapper.auto_detect_columns()
    
    st.markdown(translator.translate('mapping_auto'), unsafe_allow_html=True)
    
    # إنشاء تخطيط تعيين الأعمدة
    column_mapping = {}
    
    # عرض تعيين الأعمدة لكل فئة
    categories = {
        translator.translate('cat_order_info'): ["order_id", "order_date", "status"],
        translator.translate('cat_customer_info'): ["customer_name", "customer_id"],
        translator.translate('cat_product_info'): ["product_name", "product_id", "category"],
        translator.translate('cat_financial'): ["quantity", "unit_price", "total_price", "discount", "profit", "cost"],
        translator.translate('cat_location'): ["region", "city", "country"],
        translator.translate('cat_sales_info'): ["salesperson", "payment_method"]
    }
    
    for category, fields in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(3)
        for idx, field in enumerate(fields):
            with cols[idx % 3]:
                # ترجمة اسم الحقل للعرض
                field_display = translator.translate(f'field_{field}')
                
                # اقتراح تلقائي إن وجد
                suggested_column = auto_suggestions.get(field, translator.translate('not_available'))
                
                # إنشاء selectbox
                options = [f"❌ {translator.translate('not_available')}"] + columns
                default_idx = 0
                if suggested_column in columns:
                    default_idx = columns.index(suggested_column) + 1
                
                selected = st.selectbox(
                    f"**{field_display}**",
                    options=options,
                    index=default_idx,
                    key=f"sales_map_{field}_{st.session_state.language}"
                )
                
                if selected != f"❌ {translator.translate('not_available')}":
                    column_mapping[field] = selected
    
    st.session_state.column_mapping = column_mapping
    
    # زر للمتابعة للتحليل
    if st.button(translator.translate('analyze_button'), type="primary", use_container_width=True):
        st.session_state.analysis_ready = True
        st.rerun()

# ==================== التحليل الذكي للمبيعات ====================
if st.session_state.get('analysis_ready', False):
    st.markdown(f"## {translator.translate('analysis_title')}")
    
    analyzer = SalesDataAnalyzer(
        st.session_state.current_df, 
        st.session_state.column_mapping
    )
    
    # التحليل الذكي للبيانات
    with st.spinner(translator.translate('loading')):
        analysis = analyzer.analyze_all()
    
    st.session_state.analysis_results = analysis
    
    # عرض النتائج الرئيسية
    st.markdown(f"### {translator.translate('kpis_title')}")
    
    # بطاقات KPIs
    kpis = analysis.get('kpis', {})
    if kpis:
        # عرض أول 4 KPIs في صف واحد
        cols = st.columns(4)
        kpi_keys = list(kpis.keys())[:4]
        
        for idx, (col, kpi_key) in enumerate(zip(cols, kpi_keys)):
            with col:
                value = kpis[kpi_key]['value']
                label = kpis[kpi_key]['label']
                
                st.markdown(f"""
                <div class="kpi-card">
                    <div style="font-size: 2rem; margin-bottom: 10px;">
                        {kpis[kpi_key].get('icon', '📊')}
                    </div>
                    <div style="font-size: 2rem; font-weight: bold; color: #4F46E5;">
                        {value}
                    </div>
                    <div style="color: #6B7280;">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # عرض KPIs إضافية إذا وجدت
        if len(kpis) > 4:
            additional_kpis = list(kpis.keys())[4:8]
            if additional_kpis:
                cols = st.columns(4)
                for idx, (col, kpi_key) in enumerate(zip(cols, additional_kpis)):
                    with col:
                        value = kpis[kpi_key]['value']
                        label = kpis[kpi_key]['label']
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div style="font-size: 1.5rem; margin-bottom: 10px;">
                                {kpis[kpi_key].get('icon', '📊')}
                            </div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #10B981;">
                                {value}
                            </div>
                            <div style="color: #6B7280;">
                                {label}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # الرسوم البيانية الذكية
    st.markdown(f"### {translator.translate('charts_title')}")
    
    visualizer = SalesVisualizer(
        st.session_state.current_df,
        st.session_state.column_mapping,
        analysis
    )
    
    # عرض الرسوم حسب توفر البيانات
    charts = visualizer.generate_all_charts()
    
    if charts:
        # عرض الرسوم البيانية في أعمدة
        for i in range(0, len(charts), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(charts):
                    chart_info = charts[i + j]
                    if chart_info['available']:
                        with cols[j]:
                            st.markdown(f"#### {chart_info['title']}")
                            st.plotly_chart(chart_info['figure'], use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات كافية لإنشاء الرسوم البيانية. يرجى التحقق من تعيين الأعمدة.")
    
    # تحليل إضافي
    with st.expander(translator.translate('advanced_title')):
        st.markdown(f"### {translator.translate('advanced_title')}")
        
        # تحليل العلاقات
        numeric_cols = []
        for col in st.session_state.current_df.columns:
            if pd.api.types.is_numeric_dtype(st.session_state.current_df[col]):
                numeric_cols.append(col)
        
        if len(numeric_cols) >= 2:
            st.markdown(f"#### {translator.translate('correlations_title')}")
            
            # خريطة حرارية للعلاقات
            numeric_df = st.session_state.current_df[numeric_cols]
            corr_matrix = numeric_df.corr()
            
            import plotly.express as px
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu',
                aspect="auto",
                title=translator.translate('correlations_title')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # اكتشاف القيم الشاذة
        st.markdown(f"#### {translator.translate('outliers_title')}")
        if 'total_price' in st.session_state.column_mapping:
            price_col = st.session_state.column_mapping['total_price']
            if price_col in st.session_state.current_df.columns:
                try:
                    price_data = st.session_state.current_df[price_col].dropna()
                    
                    if len(price_data) > 0:
                        # حساب z-score يدويًا باستخدام numpy
                        mean_price = price_data.mean()
                        std_price = price_data.std()
                        
                        if std_price > 0:  # تجنب القسمة على صفر
                            z_scores = np.abs((price_data - mean_price) / std_price)
                            outliers_mask = z_scores > 3
                            outliers = st.session_state.current_df.loc[price_data.index[outliers_mask]]
                            
                            if len(outliers) > 0:
                                st.warning(translator.translate('outliers_found').format(len(outliers)))
                                st.dataframe(outliers[[price_col]], use_container_width=True)
                            else:
                                st.success(translator.translate('no_outliers'))
                        else:
                            st.info(translator.translate('zero_std'))
                except Exception as e:
                    st.error(f"خطأ في اكتشاف القيم الشاذة: {str(e)}")
    
    # تحميل التقارير
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # تصدير البيانات المعدلة
        if st.button(translator.translate('export_data'), use_container_width=True):
            modified_df = analyzer.get_modified_dataframe()
            csv = modified_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label=translator.translate('download_csv'),
                data=csv,
                file_name="sales_data_modified.csv",
                mime="text/csv"
            )
    
    with col2:
        # تصدير التقرير
        if st.button(translator.translate('export_report'), use_container_width=True):
            report = analyzer.generate_report()
            st.download_button(
                label=translator.translate('download_report'),
                data=report,
                file_name="sales_analysis_report.txt",
                mime="text/plain"
            )