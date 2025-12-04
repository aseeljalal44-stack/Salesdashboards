"""
لوحة تحكم المبيعات الذكية - ملف واحد موحد مع نظام ترجمة كامل وتقرير نصي مدمج
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import re
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO

# ==================== نظام الترجمة الكامل ====================

class TranslationSystem:
    """نظام ترجمة متكامل ثنائي اللغة"""
    
    TRANSLATIONS = {
        'ar': {
            # العنوان الرئيسي
            'dashboard_title': '📊 لوحة تحكم المبيعات الذكية',
            'dashboard_subtitle': 'تحليل ذكي لبيانات المبيعات - رفع ملفات Excel/CSV متعددة',
            
            # الشريط الجانبي
            'sidebar_settings': '⚙️ الإعدادات',
            'language': 'اللغة',
            'theme': 'المظهر',
            'light_theme': '☀️ فاتح',
            'dark_theme': '🌙 مظلم',
            'load_settings': '📥 تحميل الإعدادات',
            'save_settings': '💾 حفظ الإعدادات',
            'settings_loaded': 'تم تحميل الإعدادات السابقة',
            'settings_saved': 'تم حفظ الإعدادات',
            'no_settings': 'لا توجد إعدادات سابقة',
            'reset': '🔄 إعادة تعيين',
            
            # رفع الملفات
            'step_1': 'الخطوة 1: رفع الملفات',
            'upload_title': '📤 رفع ملفات المبيعات',
            'upload_hint': 'اسحب وأفلت ملفات Excel أو CSV هنا أو انقر للاختيار',
            'upload_supported': 'يدعم: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ تم تحميل {count} ملف بنجاح!',
            'upload_error': '❌ خطأ في تحميل الملف:',
            'file_info': '📄 معلومات الملف',
            'file_name': 'اسم الملف',
            'file_size': 'حجم الملف',
            'rows': 'عدد الصفوف',
            'columns': 'عدد الأعمدة',
            'preview': '👀 معاينة البيانات',
            'preview_rows': 'عرض أول 5 صفوف',
            'merge_files': '🔗 دمج الملفات',
            'use_merged': 'استخدام البيانات المدمجة',
            'use_single': 'استخدام ملف واحد',
            'merged_success': '✅ تم دمج الملفات بنجاح!',
            
            # الإحصائيات
            'statistics': '📈 الإحصائيات',
            'total_files': 'عدد الملفات',
            'total_records': 'عدد السجلات',
            'total_columns': 'عدد الأعمدة',
            'numeric_columns': 'أعمدة رقمية',
            'merged_data': 'بيانات مدمجة',
            'individual_file': 'ملف فردي',
            
            # تعيين الأعمدة
            'step_2': 'الخطوة 2: تعيين الأعمدة',
            'mapping_title': '🎯 تعيين أعمدة البيانات',
            'auto_detection': '💡 التعرف التلقائي',
            'auto_detection_desc': 'النظام حاول تخمين أنواع الأعمدة. يمكنك تعديلها يدوياً إذا لزم الأمر.',
            'not_available': '❌ غير متوفر',
            
            # فئات الأعمدة
            'category_order': 'معلومات الطلب',
            'category_customer': 'معلومات العميل',
            'category_product': 'معلومات المنتج',
            'category_financial': 'المعلومات المالية',
            'category_location': 'الموقع',
            'category_sales': 'معلومات المبيعات',
            
            # أسماء الحقول
            'field_order_id': 'رقم الطلب',
            'field_customer_id': 'رقم العميل',
            'field_customer_name': 'اسم العميل',
            'field_product_id': 'رقم المنتج',
            'field_product_name': 'اسم المنتج',
            'field_category': 'الفئة',
            'field_quantity': 'الكمية',
            'field_unit_price': 'سعر الوحدة',
            'field_total_amount': 'المبلغ الإجمالي',
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
            
            # التحليل
            'step_3': 'الخطوة 3: التحليل',
            'analyze_button': '🚀 بدء التحليل',
            'analysis_title': '📊 نتائج تحليل المبيعات',
            'loading_analysis': 'جاري تحليل البيانات...',
            
            # KPIs
            'kpis_title': '📈 المؤشرات الرئيسية',
            'kpi_transactions': 'إجمالي المعاملات',
            'kpi_sales': 'إجمالي المبيعات',
            'kpi_avg_transaction': 'متوسط قيمة المعاملة',
            'kpi_profit': 'إجمالي الربح',
            'kpi_customers': 'عدد العملاء',
            'kpi_products': 'عدد المنتجات',
            'kpi_avg_quantity': 'متوسط الكمية',
            'kpi_discount_rate': 'معدل الخصم',
            
            # الرسوم البيانية
            'charts_title': '📊 الرسوم البيانية',
            'chart_sales_trend': 'اتجاه المبيعات الشهري',
            'chart_top_products': 'أفضل 10 منتجات مبيعاً',
            'chart_region_dist': 'توزيع المبيعات حسب المنطقة',
            'chart_category_dist': 'توزيع المبيعات حسب الفئة',
            'chart_sales_performance': 'أداء مندوبي المبيعات',
            'chart_price_quantity': 'العلاقة بين السعر والكمية',
            'chart_payment_methods': 'توزيع طرق الدفع',
            'chart_profit_dist': 'توزيع الأرباح',
            'no_charts_data': '⚠️ لا توجد بيانات كافية لإنشاء الرسوم البيانية',
            
            # التحليل المتقدم
            'advanced_analysis': '🔍 تحليل متقدم',
            'correlation_matrix': 'مصفوفة الارتباط',
            'outlier_detection': 'كشف القيم الشاذة',
            'outliers_found': 'تم اكتشاف {count} قيمة شاذة',
            'no_outliers': '✅ لم يتم اكتشاف قيم شاذة',
            'zero_std': 'انحراف معياري صفري - لا يمكن كشف القيم الشاذة',
            
            # التقرير
            'report_title': '📄 التقرير التحليلي',
            'generate_report': '📋 إنشاء التقرير',
            'copy_report': '📋 نسخ التقرير',
            'report_copied': '✅ تم نسخ التقرير إلى الحافظة',
            'executive_summary': 'الملخص التنفيذي',
            'data_overview': 'نظرة عامة على البيانات',
            'key_findings': 'النقاط الرئيسية',
            'performance_analysis': 'تحليل الأداء',
            'recommendations': 'التوصيات',
            'data_quality': 'جودة البيانات',
            'report_date': 'تاريخ التقرير',
            'analysis_period': 'فترة التحليل',
            'total_analysis': 'إجمالي التحليل',
            'top_performers': 'الأفضل أداءً',
            'areas_improvement': 'مجالات التحسين',
            
            # جودة البيانات
            'data_quality_title': '🔍 جودة البيانات',
            'missing_values': 'قيم مفقودة',
            'duplicates': 'سجلات مكررة',
            'negative_amounts': 'مبالغ سلبية',
            'invalid_quantities': 'كميات غير منطقية',
            'future_dates': 'تواريخ مستقبلية',
            
            # الأزرار العامة
            'download': 'تحميل',
            'copy': 'نسخ',
            'close': 'إغلاق',
            'back': 'رجوع',
            'next': 'التالي',
            'finish': 'إنهاء',
            
            # الرسائل
            'no_data': 'لم يتم تحميل بيانات بعد',
            'select_file_first': 'يرجى رفع ملف أولاً',
            'select_columns': 'يرجى تعيين الأعمدة أولاً',
            'analysis_complete': 'تم التحليل بنجاح',
            'error': 'خطأ',
            'warning': 'تحذير',
            'success': 'نجاح',
            'info': 'معلومة',
        },
        
        'en': {
            # Main Title
            'dashboard_title': '📊 Smart Sales Analytics Dashboard',
            'dashboard_subtitle': 'Intelligent sales data analysis - Upload multiple Excel/CSV files',
            
            # Sidebar
            'sidebar_settings': '⚙️ Settings',
            'language': 'Language',
            'theme': 'Theme',
            'light_theme': '☀️ Light',
            'dark_theme': '🌙 Dark',
            'load_settings': '📥 Load Settings',
            'save_settings': '💾 Save Settings',
            'settings_loaded': 'Previous settings loaded',
            'settings_saved': 'Settings saved',
            'no_settings': 'No previous settings',
            'reset': '🔄 Reset',
            
            # File Upload
            'step_1': 'Step 1: Upload Files',
            'upload_title': '📤 Upload Sales Files',
            'upload_hint': 'Drag and drop Excel or CSV files here or click to browse',
            'upload_supported': 'Supports: Excel (.xlsx, .xls), CSV',
            'upload_success': '✅ Successfully uploaded {count} file(s)!',
            'upload_error': '❌ Error loading file:',
            'file_info': '📄 File Information',
            'file_name': 'File Name',
            'file_size': 'File Size',
            'rows': 'Rows',
            'columns': 'Columns',
            'preview': '👀 Data Preview',
            'preview_rows': 'Show first 5 rows',
            'merge_files': '🔗 Merge Files',
            'use_merged': 'Use Merged Data',
            'use_single': 'Use Single File',
            'merged_success': '✅ Files merged successfully!',
            
            # Statistics
            'statistics': '📈 Statistics',
            'total_files': 'Total Files',
            'total_records': 'Total Records',
            'total_columns': 'Total Columns',
            'numeric_columns': 'Numeric Columns',
            'merged_data': 'Merged Data',
            'individual_file': 'Individual File',
            
            # Column Mapping
            'step_2': 'Step 2: Map Columns',
            'mapping_title': '🎯 Data Column Mapping',
            'auto_detection': '💡 Auto Detection',
            'auto_detection_desc': 'System tried to guess column types. You can adjust manually if needed.',
            'not_available': '❌ Not Available',
            
            # Column Categories
            'category_order': 'Order Information',
            'category_customer': 'Customer Information',
            'category_product': 'Product Information',
            'category_financial': 'Financial Information',
            'category_location': 'Location',
            'category_sales': 'Sales Information',
            
            # Field Names
            'field_order_id': 'Order ID',
            'field_customer_id': 'Customer ID',
            'field_customer_name': 'Customer Name',
            'field_product_id': 'Product ID',
            'field_product_name': 'Product Name',
            'field_category': 'Category',
            'field_quantity': 'Quantity',
            'field_unit_price': 'Unit Price',
            'field_total_amount': 'Total Amount',
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
            
            # Analysis
            'step_3': 'Step 3: Analysis',
            'analyze_button': '🚀 Start Analysis',
            'analysis_title': '📊 Sales Analysis Results',
            'loading_analysis': 'Analyzing data...',
            
            # KPIs
            'kpis_title': '📈 Key Performance Indicators',
            'kpi_transactions': 'Total Transactions',
            'kpi_sales': 'Total Sales',
            'kpi_avg_transaction': 'Average Transaction Value',
            'kpi_profit': 'Total Profit',
            'kpi_customers': 'Number of Customers',
            'kpi_products': 'Number of Products',
            'kpi_avg_quantity': 'Average Quantity',
            'kpi_discount_rate': 'Discount Rate',
            
            # Charts
            'charts_title': '📊 Charts & Visualizations',
            'chart_sales_trend': 'Monthly Sales Trend',
            'chart_top_products': 'Top 10 Selling Products',
            'chart_region_dist': 'Sales Distribution by Region',
            'chart_category_dist': 'Sales Distribution by Category',
            'chart_sales_performance': 'Salesperson Performance',
            'chart_price_quantity': 'Price vs Quantity Relationship',
            'chart_payment_methods': 'Payment Methods Distribution',
            'chart_profit_dist': 'Profit Distribution',
            'no_charts_data': '⚠️ Insufficient data to generate charts',
            
            # Advanced Analysis
            'advanced_analysis': '🔍 Advanced Analysis',
            'correlation_matrix': 'Correlation Matrix',
            'outlier_detection': 'Outlier Detection',
            'outliers_found': 'Found {count} outliers',
            'no_outliers': '✅ No outliers detected',
            'zero_std': 'Zero standard deviation - Cannot detect outliers',
            
            # Report
            'report_title': '📄 Analytical Report',
            'generate_report': '📋 Generate Report',
            'copy_report': '📋 Copy Report',
            'report_copied': '✅ Report copied to clipboard',
            'executive_summary': 'Executive Summary',
            'data_overview': 'Data Overview',
            'key_findings': 'Key Findings',
            'performance_analysis': 'Performance Analysis',
            'recommendations': 'Recommendations',
            'data_quality': 'Data Quality',
            'report_date': 'Report Date',
            'analysis_period': 'Analysis Period',
            'total_analysis': 'Total Analysis',
            'top_performers': 'Top Performers',
            'areas_improvement': 'Areas for Improvement',
            
            # Data Quality
            'data_quality_title': '🔍 Data Quality',
            'missing_values': 'Missing Values',
            'duplicates': 'Duplicate Records',
            'negative_amounts': 'Negative Amounts',
            'invalid_quantities': 'Invalid Quantities',
            'future_dates': 'Future Dates',
            
            # General Buttons
            'download': 'Download',
            'copy': 'Copy',
            'close': 'Close',
            'back': 'Back',
            'next': 'Next',
            'finish': 'Finish',
            
            # Messages
            'no_data': 'No data loaded yet',
            'select_file_first': 'Please upload a file first',
            'select_columns': 'Please map columns first',
            'analysis_complete': 'Analysis completed successfully',
            'error': 'Error',
            'warning': 'Warning',
            'success': 'Success',
            'info': 'Info',
        }
    }
    
    @classmethod
    def t(cls, key, **kwargs):
        """ترجمة النص بناءً على اللغة الحالية"""
        lang = st.session_state.get('language', 'ar')
        translation = cls.TRANSLATIONS.get(lang, cls.TRANSLATIONS['ar']).get(key, key)
        
        if kwargs:
            try:
                return translation.format(**kwargs)
            except:
                return translation
        return translation
    
    @classmethod
    def get_language_direction(cls):
        """الحصول على اتجاه النص للغة الحالية"""
        lang = st.session_state.get('language', 'ar')
        return 'rtl' if lang == 'ar' else 'ltr'
    
    @classmethod
    def get_font_family(cls):
        """الحصول على خط النص للغة الحالية"""
        lang = st.session_state.get('language', 'ar')
        return "'Cairo', 'Segoe UI', sans-serif" if lang == 'ar' else "'Segoe UI', Tahoma, Geneva, sans-serif"

# ==================== 1. وحدة التعرف التلقائي على الأعمدة ====================

class SalesAutoColumnMapper:
    def __init__(self, dataframe):
        self.df = dataframe
        self.column_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self):
        """تهيئة الأنماط للتعرف على أعمدة المبيعات"""
        return {
            'order_id': {
                'patterns': ['order.*id', 'order.*no', 'transaction.*id', 'رقم.*الطلب', 'معرف.*الطلب'],
                'keywords': ['order', 'transaction', 'طلب', 'معرف']
            },
            'customer_id': {
                'patterns': ['customer.*id', 'client.*id', 'cust.*id', 'رقم.*العميل', 'معرف.*العميل'],
                'keywords': ['customer', 'client', 'عميل', 'زبون']
            },
            'customer_name': {
                'patterns': ['customer.*name', 'client.*name', 'اسم.*العميل', 'العميل'],
                'keywords': ['customer', 'client', 'اسم', 'name']
            },
            'product_id': {
                'patterns': ['product.*id', 'item.*id', 'sku', 'رقم.*المنتج', 'معرف.*المنتج'],
                'keywords': ['product', 'item', 'sku', 'منتج', 'سلعة']
            },
            'product_name': {
                'patterns': ['product.*name', 'item.*name', 'اسم.*المنتج', 'المنتج'],
                'keywords': ['product', 'item', 'اسم', 'name', 'منتج']
            },
            'category': {
                'patterns': ['category', 'type', 'class', 'فئة', 'تصنيف', 'نوع'],
                'keywords': ['category', 'type', 'فئة', 'تصنيف']
            },
            'quantity': {
                'patterns': ['quantity', 'qty', 'amount', 'الكمية', 'عدد', 'مقدار'],
                'keywords': ['quantity', 'qty', 'كمية', 'عدد']
            },
            'price': {
                'patterns': ['price', 'unit.*price', 'cost', 'سعر', 'السعر', 'التكلفة'],
                'keywords': ['price', 'cost', 'سعر', 'تكلفة']
            },
            'total_amount': {
                'patterns': ['total', 'amount', 'revenue', 'المبلغ', 'الإجمالي', 'الإيراد'],
                'keywords': ['total', 'amount', 'revenue', 'إجمالي', 'مبلغ']
            },
            'order_date': {
                'patterns': ['order.*date', 'transaction.*date', 'date', 'تاريخ.*الطلب', 'التاريخ'],
                'keywords': ['date', 'تاريخ', 'order', 'طلب']
            },
            'region': {
                'patterns': ['region', 'area', 'zone', 'منطقة', 'المنطقة', 'الفرع'],
                'keywords': ['region', 'area', 'zone', 'منطقة']
            },
            'city': {
                'patterns': ['city', 'town', 'المدينة', 'مدينة'],
                'keywords': ['city', 'town', 'مدينة']
            },
            'country': {
                'patterns': ['country', 'state', 'البلد', 'الدولة'],
                'keywords': ['country', 'state', 'بلد', 'دولة']
            },
            'salesperson': {
                'patterns': ['salesperson', 'seller', 'agent', 'مندوب', 'البائع', 'الموظف'],
                'keywords': ['sales', 'seller', 'agent', 'مندوب', 'بائع']
            },
            'payment_method': {
                'patterns': ['payment.*method', 'payment.*type', 'طريقة.*الدفع', 'نوع.*الدفع'],
                'keywords': ['payment', 'دفع', 'method', 'طريقة']
            },
            'discount': {
                'patterns': ['discount', 'off', 'خصم', 'التخفيض'],
                'keywords': ['discount', 'خصم', 'تخفيض']
            },
            'profit': {
                'patterns': ['profit', 'margin', 'ربح', 'الربح', 'هامش'],
                'keywords': ['profit', 'margin', 'ربح', 'هامش']
            },
            'status': {
                'patterns': ['status', 'state', 'condition', 'حالة', 'الحالة'],
                'keywords': ['status', 'state', 'حالة']
            }
        }
    
    def auto_detect_columns(self):
        """التعرف التلقائي على أنواع الأعمدة"""
        suggestions = {}
        columns = self.df.columns.tolist()
        
        for column in columns:
            column_lower = str(column).lower()
            
            for field_type, patterns_info in self.column_patterns.items():
                for pattern in patterns_info['patterns']:
                    if re.search(pattern, column_lower, re.IGNORECASE):
                        suggestions[field_type] = column
                        break
                
                if field_type not in suggestions:
                    for keyword in patterns_info['keywords']:
                        if keyword.lower() in column_lower:
                            suggestions[field_type] = column
                            break
            
            if self._is_date_column(column):
                if 'order_date' not in suggestions:
                    suggestions['order_date'] = column
        
        return suggestions
    
    def _is_date_column(self, column_name):
        """فحص إذا كان العمود يحتوي على تواريخ"""
        if column_name not in self.df.columns:
            return False
        
        column_sample = self.df[column_name].dropna().head(10)
        
        if len(column_sample) == 0:
            return False
        
        try:
            if pd.api.types.is_datetime64_any_dtype(self.df[column_name]):
                return True
            
            test_dates = pd.to_datetime(column_sample, errors='coerce')
            success_rate = test_dates.notna().sum() / len(column_sample)
            
            return success_rate > 0.7
        except:
            return False

# ==================== 2. وحدة التحليل الذكي ====================

class SalesDataAnalyzer:
    def __init__(self, dataframe, column_mapping):
        self.df = dataframe.copy()
        self.mapping = column_mapping
    
    def analyze_all(self):
        """إجراء جميع التحليلات المتاحة للمبيعات"""
        analysis_results = {
            'kpis': {},
            'distributions': {},
            'trends': {},
            'insights': [],
            'warnings': [],
            'top_performers': {}
        }
        
        analysis_results['kpis'] = self._calculate_kpis()
        analysis_results['distributions'] = self._analyze_distributions()
        analysis_results['trends'] = self._analyze_trends()
        analysis_results['insights'] = self._extract_insights()
        analysis_results['warnings'] = self._check_data_quality()
        analysis_results['top_performers'] = self._identify_top_performers()
        
        return analysis_results
    
    def _calculate_kpis(self):
        """حساب مؤشرات أداء المبيعات"""
        kpis = {}
        
        # إجمالي عدد المعاملات
        total_transactions = len(self.df)
        kpis['total_transactions'] = {
            'value': total_transactions,
            'formatted': f"{total_transactions:,}",
            'label': TranslationSystem.t('kpi_transactions'),
            'icon': '🛒'
        }
        
        # إجمالي المبيعات
        if 'total_amount' in self.mapping:
            amount_col = self.mapping['total_amount']
            if amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    total_sales = self.df[amount_col].sum()
                    kpis['total_sales'] = {
                        'value': total_sales,
                        'formatted': f"${total_sales:,.0f}",
                        'label': TranslationSystem.t('kpi_sales'),
                        'icon': '💰'
                    }
                    
                    avg_transaction = total_sales / total_transactions if total_transactions > 0 else 0
                    kpis['avg_transaction'] = {
                        'value': avg_transaction,
                        'formatted': f"${avg_transaction:,.0f}",
                        'label': TranslationSystem.t('kpi_avg_transaction'),
                        'icon': '📊'
                    }
                except:
                    pass
        
        # إجمالي الربح
        if 'profit' in self.mapping:
            profit_col = self.mapping['profit']
            if profit_col in self.df.columns:
                try:
                    self.df[profit_col] = pd.to_numeric(self.df[profit_col], errors='coerce')
                    total_profit = self.df[profit_col].sum()
                    kpis['total_profit'] = {
                        'value': total_profit,
                        'formatted': f"${total_profit:,.0f}",
                        'label': TranslationSystem.t('kpi_profit'),
                        'icon': '📈'
                    }
                except:
                    pass
        
        # عدد العملاء الفريدين
        if 'customer_id' in self.mapping:
            customer_col = self.mapping['customer_id']
            if customer_col in self.df.columns:
                unique_customers = self.df[customer_col].nunique()
                kpis['unique_customers'] = {
                    'value': unique_customers,
                    'formatted': f"{unique_customers:,}",
                    'label': TranslationSystem.t('kpi_customers'),
                    'icon': '👥'
                }
        
        # عدد المنتجات الفريدة
        if 'product_id' in self.mapping:
            product_col = self.mapping['product_id']
            if product_col in self.df.columns:
                unique_products = self.df[product_col].nunique()
                kpis['unique_products'] = {
                    'value': unique_products,
                    'formatted': f"{unique_products:,}",
                    'label': TranslationSystem.t('kpi_products'),
                    'icon': '📦'
                }
        
        # متوسط الكمية لكل معاملة
        if 'quantity' in self.mapping:
            quantity_col = self.mapping['quantity']
            if quantity_col in self.df.columns:
                try:
                    self.df[quantity_col] = pd.to_numeric(self.df[quantity_col], errors='coerce')
                    avg_quantity = self.df[quantity_col].mean()
                    kpis['avg_quantity'] = {
                        'value': avg_quantity,
                        'formatted': f"{avg_quantity:.1f}",
                        'label': TranslationSystem.t('kpi_avg_quantity'),
                        'icon': '⚖️'
                    }
                except:
                    pass
        
        return kpis
    
    def _analyze_distributions(self):
        """تحليل توزيع بيانات المبيعات"""
        distributions = {}
        
        if 'region' in self.mapping:
            region_col = self.mapping['region']
            if region_col in self.df.columns:
                region_dist = self.df[region_col].value_counts().to_dict()
                distributions['region'] = region_dist
        
        if 'category' in self.mapping:
            category_col = self.mapping['category']
            if category_col in self.df.columns:
                category_dist = self.df[category_col].value_counts().to_dict()
                distributions['category'] = category_dist
        
        if 'product_name' in self.mapping:
            product_col = self.mapping['product_name']
            if product_col in self.df.columns:
                product_dist = self.df[product_col].value_counts().head(10).to_dict()
                distributions['top_products'] = product_dist
        
        if 'payment_method' in self.mapping:
            payment_col = self.mapping['payment_method']
            if payment_col in self.df.columns:
                payment_dist = self.df[payment_col].value_counts().to_dict()
                distributions['payment_method'] = payment_dist
        
        return distributions
    
    def _analyze_trends(self):
        """تحليل اتجاهات المبيعات"""
        trends = {}
        
        if 'order_date' in self.mapping and 'total_amount' in self.mapping:
            date_col = self.mapping['order_date']
            amount_col = self.mapping['total_amount']
            
            if date_col in self.df.columns and amount_col in self.df.columns:
                try:
                    df_copy = self.df.copy()
                    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
                    df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
                    
                    df_clean = df_copy.dropna(subset=[date_col, amount_col])
                    
                    if len(df_clean) > 0:
                        df_clean['year_month'] = df_clean[date_col].dt.to_period('M')
                        monthly_trend = df_clean.groupby('year_month')[amount_col].agg(['sum', 'count']).reset_index()
                        monthly_trend['year_month'] = monthly_trend['year_month'].astype(str)
                        
                        trends['monthly'] = monthly_trend.to_dict('records')
                except:
                    pass
        
        return trends
    
    def _extract_insights(self):
        """استخلاص رؤى من بيانات المبيعات"""
        insights = []
        
        if 'region' in self.mapping and 'total_amount' in self.mapping:
            region_col = self.mapping['region']
            amount_col = self.mapping['total_amount']
            
            if region_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    region_sales = self.df.groupby(region_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(region_sales) > 0:
                        top_region = region_sales.index[0]
                        top_sales = region_sales.iloc[0]
                        if TranslationSystem.t('language') == 'ar':
                            insights.append(f"🏆 **أفضل منطقة مبيعات**: {top_region} (${top_sales:,.0f})")
                        else:
                            insights.append(f"🏆 **Top Sales Region**: {top_region} (${top_sales:,.0f})")
                except:
                    pass
        
        if 'product_name' in self.mapping and 'quantity' in self.mapping:
            product_col = self.mapping['product_name']
            quantity_col = self.mapping['quantity']
            
            if product_col in self.df.columns and quantity_col in self.df.columns:
                try:
                    self.df[quantity_col] = pd.to_numeric(self.df[quantity_col], errors='coerce')
                    product_sales = self.df.groupby(product_col)[quantity_col].sum().sort_values(ascending=False)
                    
                    if len(product_sales) > 0:
                        top_product = product_sales.index[0]
                        top_qty = product_sales.iloc[0]
                        if TranslationSystem.t('language') == 'ar':
                            insights.append(f"📦 **أكثر منتج مبيعاً**: {top_product} ({top_qty:,} وحدة)")
                        else:
                            insights.append(f"📦 **Top Selling Product**: {top_product} ({top_qty:,} units)")
                except:
                    pass
        
        return insights
    
    def _identify_top_performers(self):
        """تحديد الأفضل أداءً"""
        top_performers = {}
        
        if 'salesperson' in self.mapping and 'total_amount' in self.mapping:
            salesperson_col = self.mapping['salesperson']
            amount_col = self.mapping['total_amount']
            
            if salesperson_col in self.df.columns and amount_col in self.df.columns:
                try:
                    self.df[amount_col] = pd.to_numeric(self.df[amount_col], errors='coerce')
                    salesperson_performance = self.df.groupby(salesperson_col)[amount_col].sum().sort_values(ascending=False)
                    
                    if len(salesperson_performance) > 0:
                        top_performers['salesperson'] = {
                            'name': salesperson_performance.index[0],
                            'value': salesperson_performance.iloc[0]
                        }
                except:
                    pass
        
        if 'product_name' in self.mapping and 'profit' in self.mapping:
            product_col = self.mapping['product_name']
            profit_col = self.mapping['profit']
            
            if product_col in self.df.columns and profit_col in self.df.columns:
                try:
                    self.df[profit_col] = pd.to_numeric(self.df[profit_col], errors='coerce')
                    product_profit = self.df.groupby(product_col)[profit_col].sum().sort_values(ascending=False)
                    
                    if len(product_profit) > 0:
                        top_performers['product_profit'] = {
                            'name': product_profit.index[0],
                            'value': product_profit.iloc[0]
                        }
                except:
                    pass
        
        return top_performers
    
    def _check_data_quality(self):
        """فحص جودة بيانات المبيعات"""
        warnings = []
        
        missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        high_missing = missing_percentage[missing_percentage > 20].index.tolist()
        
        if high_missing:
            if TranslationSystem.t('language') == 'ar':
                warnings.append(f"⚠️ أعمدة بها قيم مفقودة >20%: {', '.join(high_missing[:3])}")
            else:
                warnings.append(f"⚠️ Columns with missing values >20%: {', '.join(high_missing[:3])}")
        
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            if TranslationSystem.t('language') == 'ar':
                warnings.append(f"⚠️ يوجد {duplicates} سجل مكرر")
            else:
                warnings.append(f"⚠️ Found {duplicates} duplicate records")
        
        if 'total_amount' in self.mapping:
            amount_col = self.mapping['total_amount']
            if amount_col in self.df.columns:
                try:
                    amount_data = pd.to_numeric(self.df[amount_col], errors='coerce')
                    negative_amounts = (amount_data < 0).sum()
                    if negative_amounts > 0:
                        if TranslationSystem.t('language') == 'ar':
                            warnings.append(f"⚠️ يوجد {negative_amounts} معاملة بمبلغ سالب")
                        else:
                            warnings.append(f"⚠️ Found {negative_amounts} transactions with negative amounts")
                except:
                    pass
        
        return warnings
    
    def generate_text_report(self, analysis_results):
        """إنشاء تقرير نصي احترافي"""
        lang = TranslationSystem.t('language')
        
        if lang == 'ar':
            report = f"""
{'='*80}
تقرير تحليل بيانات المبيعات
{'='*80}

تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}

الملخص التنفيذي
{'-'*40}

تم تحليل بيانات المبيعات بنجاح، فيما يلي النتائج الرئيسية:

نظرة عامة على البيانات
{'-'*40}

• عدد السجلات: {analysis_results['kpis'].get('total_transactions', {}).get('formatted', 'N/A')}
• عدد الأعمدة: {len(self.df.columns)}
• فترة البيانات: {self._get_date_range()}

المؤشرات الرئيسية (KPIs)
{'-'*40}
"""
            
            for kpi_name, kpi_info in analysis_results['kpis'].items():
                report += f"• {kpi_info['label']}: {kpi_info['formatted']}\n"
            
            report += f"""
النقاط الرئيسية
{'-'*40}
"""
            
            for insight in analysis_results['insights']:
                report += f"• {insight.replace('**', '')}\n"
            
            if analysis_results['top_performers']:
                report += f"""
الأفضل أداءً
{'-'*40}
"""
                if 'salesperson' in analysis_results['top_performers']:
                    sp = analysis_results['top_performers']['salesperson']
                    report += f"• أفضل مندوب مبيعات: {sp['name']} (${sp['value']:,.0f})\n"
                
                if 'product_profit' in analysis_results['top_performers']:
                    pp = analysis_results['top_performers']['product_profit']
                    report += f"• أكثر منتج ربحية: {pp['name']} (${pp['value']:,.0f})\n"
            
            if analysis_results['warnings']:
                report += f"""
جودة البيانات
{'-'*40}
"""
                for warning in analysis_results['warnings']:
                    report += f"• {warning}\n"
            
            report += f"""
التوصيات
{'-'*40}

1. التركيز على المناطق ذات الأداء العالي
2. تحسين المنتجات الأكثر مبيعاً
3. تحفيز مندوبي المبيعات بناءً على الأداء
4. معالجة مشاكل جودة البيانات
5. تحليل تأثير الخصومات على المبيعات

{'='*80}
تم إنشاء التقرير بواسطة نظام تحليل المبيعات الذكي
{'='*80}
"""
        else:
            report = f"""
{'='*80}
Sales Data Analysis Report
{'='*80}

Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Executive Summary
{'-'*40}

Sales data analysis completed successfully. Key findings include:

Data Overview
{'-'*40}

• Total Records: {analysis_results['kpis'].get('total_transactions', {}).get('formatted', 'N/A')}
• Number of Columns: {len(self.df.columns)}
• Data Period: {self._get_date_range()}

Key Performance Indicators (KPIs)
{'-'*40}
"""
            
            for kpi_name, kpi_info in analysis_results['kpis'].items():
                report += f"• {kpi_info['label']}: {kpi_info['formatted']}\n"
            
            report += f"""
Key Findings
{'-'*40}
"""
            
            for insight in analysis_results['insights']:
                report += f"• {insight.replace('**', '')}\n"
            
            if analysis_results['top_performers']:
                report += f"""
Top Performers
{'-'*40}
"""
                if 'salesperson' in analysis_results['top_performers']:
                    sp = analysis_results['top_performers']['salesperson']
                    report += f"• Top Salesperson: {sp['name']} (${sp['value']:,.0f})\n"
                
                if 'product_profit' in analysis_results['top_performers']:
                    pp = analysis_results['top_performers']['product_profit']
                    report += f"• Most Profitable Product: {pp['name']} (${pp['value']:,.0f})\n"
            
            if analysis_results['warnings']:
                report += f"""
Data Quality Issues
{'-'*40}
"""
                for warning in analysis_results['warnings']:
                    report += f"• {warning}\n"
            
            report += f"""
Recommendations
{'-'*40}

1. Focus on high-performing regions
2. Optimize top-selling products
3. Motivate sales team based on performance
4. Address data quality issues
5. Analyze discount impact on sales

{'='*80}
Generated by Smart Sales Analytics System
{'='*80}
"""
        
        return report
    
    def _get_date_range(self):
        """الحصول على نطاق التاريخ من البيانات"""
        if 'order_date' in self.mapping:
            date_col = self.mapping['order_date']
            if date_col in self.df.columns:
                try:
                    dates = pd.to_datetime(self.df[date_col], errors='coerce')
                    min_date = dates.min()
                    max_date = dates.max()
                    
                    if pd.notna(min_date) and pd.notna(max_date):
                        if TranslationSystem.t('language') == 'ar':
                            return f"{min_date.strftime('%Y-%m-%d')} إلى {max_date.strftime('%Y-%m-%d')}"
                        else:
                            return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
                except:
                    pass
        
        if TranslationSystem.t('language') == 'ar':
            return "غير متوفر"
        else:
            return "Not available"

# ==================== 3. وحدة الرسوم البيانية ====================

class SalesVisualizer:
    def __init__(self, dataframe, column_mapping, analysis_results):
        self.df = dataframe
        self.mapping = column_mapping
        self.analysis = analysis_results
    
    def generate_all_charts(self):
        """توليد جميع الرسوم البيانية الممكنة للمبيعات"""
        charts = []
        
        charts.append(self._create_sales_trend_chart())
        charts.append(self._create_top_products_chart())
        charts.append(self._create_region_chart())
        charts.append(self._create_category_chart())
        charts.append(self._create_salesperson_chart())
        charts.append(self._create_price_quantity_chart())
        charts.append(self._create_payment_method_chart())
        charts.append(self._create_profit_chart())
        
        return [chart for chart in charts if chart is not None]
    
    def _create_sales_trend_chart(self):
        """إنشاء رسم اتجاه المبيعات عبر الزمن"""
        if 'order_date' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        date_col = self.mapping['order_date']
        amount_col = self.mapping['total_amount']
        
        if date_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            df_clean = df_copy.dropna(subset=[date_col, amount_col])
            
            if len(df_clean) == 0:
                return None
            
            df_clean['year_month'] = df_clean[date_col].dt.to_period('M').dt.to_timestamp()
            sales_trend = df_clean.groupby('year_month')[amount_col].sum().reset_index()
            
            fig = px.line(
                sales_trend,
                x='year_month',
                y=amount_col,
                title=TranslationSystem.t('chart_sales_trend'),
                labels={'year_month': TranslationSystem.t('order_date'), amount_col: TranslationSystem.t('total_amount')}
            )
            
            fig.update_traces(mode='lines+markers')
            
            return {
                'title': TranslationSystem.t('chart_sales_trend'),
                'figure': fig
            }
        except:
            return None
    
    def _create_top_products_chart(self):
        """إنشاء رسم أفضل المنتجات مبيعاً"""
        if 'product_name' not in self.mapping or 'quantity' not in self.mapping:
            return None
        
        product_col = self.mapping['product_name']
        quantity_col = self.mapping['quantity']
        
        if product_col not in self.df.columns or quantity_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[quantity_col] = pd.to_numeric(df_copy[quantity_col], errors='coerce')
            
            product_sales = df_copy.groupby(product_col)[quantity_col].sum().reset_index()
            product_sales = product_sales.sort_values(quantity_col, ascending=False).head(10)
            
            fig = px.bar(
                product_sales,
                x=quantity_col,
                y=product_col,
                orientation='h',
                color=quantity_col,
                color_continuous_scale='Viridis',
                title=TranslationSystem.t('chart_top_products')
            )
            
            fig.update_layout(
                xaxis_title=TranslationSystem.t('quantity'),
                yaxis_title=TranslationSystem.t('product_name'),
                coloraxis_showscale=False
            )
            
            return {
                'title': TranslationSystem.t('chart_top_products'),
                'figure': fig
            }
        except:
            return None
    
    def _create_region_chart(self):
        """إنشاء رسم توزيع المبيعات حسب المنطقة"""
        if 'region' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        region_col = self.mapping['region']
        amount_col = self.mapping['total_amount']
        
        if region_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            region_sales = df_copy.groupby(region_col)[amount_col].sum().reset_index()
            
            fig = px.pie(
                region_sales,
                values=amount_col,
                names=region_col,
                title=TranslationSystem.t('chart_region_dist'),
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return {
                'title': TranslationSystem.t('chart_region_dist'),
                'figure': fig
            }
        except:
            return None
    
    def _create_category_chart(self):
        """إنشاء رسم توزيع المبيعات حسب الفئة"""
        if 'category' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        category_col = self.mapping['category']
        amount_col = self.mapping['total_amount']
        
        if category_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            category_sales = df_copy.groupby(category_col)[amount_col].sum().reset_index()
            category_sales = category_sales.sort_values(amount_col, ascending=False).head(8)
            
            fig = px.bar(
                category_sales,
                x=category_col,
                y=amount_col,
                color=amount_col,
                color_continuous_scale='Blues',
                title=TranslationSystem.t('chart_category_dist')
            )
            
            fig.update_layout(
                xaxis_title=TranslationSystem.t('category'),
                yaxis_title=TranslationSystem.t('total_amount'),
                coloraxis_showscale=False
            )
            
            return {
                'title': TranslationSystem.t('chart_category_dist'),
                'figure': fig
            }
        except:
            return None
    
    def _create_salesperson_chart(self):
        """إنشاء رسم أداء مندوبي المبيعات"""
        if 'salesperson' not in self.mapping or 'total_amount' not in self.mapping:
            return None
        
        salesperson_col = self.mapping['salesperson']
        amount_col = self.mapping['total_amount']
        
        if salesperson_col not in self.df.columns or amount_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[amount_col] = pd.to_numeric(df_copy[amount_col], errors='coerce')
            
            salesperson_performance = df_copy.groupby(salesperson_col)[amount_col].sum().reset_index()
            salesperson_performance = salesperson_performance.sort_values(amount_col, ascending=False).head(10)
            
            fig = px.bar(
                salesperson_performance,
                x=salesperson_col,
                y=amount_col,
                color=amount_col,
                color_continuous_scale='RdYlGn',
                title=TranslationSystem.t('chart_sales_performance')
            )
            
            fig.update_layout(
                xaxis_title=TranslationSystem.t('salesperson'),
                yaxis_title=TranslationSystem.t('total_amount'),
                coloraxis_showscale=False
            )
            
            return {
                'title': TranslationSystem.t('chart_sales_performance'),
                'figure': fig
            }
        except:
            return None
    
    def _create_price_quantity_chart(self):
        """إنشاء رسم علاقة السعر بالكمية"""
        if 'price' not in self.mapping or 'quantity' not in self.mapping:
            return None
        
        price_col = self.mapping['price']
        quantity_col = self.mapping['quantity']
        
        if price_col not in self.df.columns or quantity_col not in self.df.columns:
            return None
        
        try:
            df_copy = self.df.copy()
            df_copy[price_col] = pd.to_numeric(df_copy[price_col], errors='coerce')
            df_copy[quantity_col] = pd.to_numeric(df_copy[quantity_col], errors='coerce')
            
            df_clean = df_copy.dropna(subset=[price_col, quantity_col])
            
            if len(df_clean) == 0:
                return None
            
            fig = px.scatter(
                df_clean,
                x=price_col,
                y=quantity_col,
                trendline="ols",
                title=TranslationSystem.t('chart_price_quantity'),
                labels={price_col: TranslationSystem.t('unit_price'), quantity_col: TranslationSystem.t('quantity')}
            )
            
            return {
                'title': TranslationSystem.t('chart_price_quantity'),
                'figure': fig
            }
        except:
            return None
    
    def _create_payment_method_chart(self):
        """إنشاء رسم توزيع طرق الدفع"""
        if 'payment_method' not in self.mapping:
            return None
        
        payment_col = self.mapping['payment_method']
        
        if payment_col not in self.df.columns:
            return None
        
        payment_counts = self.df[payment_col].value_counts().reset_index()
        payment_counts.columns = ['payment_method', 'count']
        
        fig = px.pie(
            payment_counts,
            values='count',
            names='payment_method',
            title=TranslationSystem.t('chart_payment_methods'),
            hole=0.3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return {
            'title': TranslationSystem.t('chart_payment_methods'),
            'figure': fig
        }
    
    def _create_profit_chart(self):
        """إنشاء رسم تحليل الربحية"""
        if 'profit' not in self.mapping:
            return None
        
        profit_col = self.mapping['profit']
        
        if profit_col not in self.df.columns:
            return None
        
        try:
            profit_data = pd.to_numeric(self.df[profit_col], errors='coerce').dropna()
            
            if len(profit_data) == 0:
                return None
            
            fig = px.histogram(
                profit_data,
                nbins=30,
                title=TranslationSystem.t('chart_profit_dist'),
                labels={'value': TranslationSystem.t('profit'), 'count': 'Count'}
            )
            
            avg_profit = profit_data.mean()
            fig.add_vline(
                x=avg_profit,
                line_dash="dash",
                line_color="green",
                annotation_text=f"Average: ${avg_profit:,.0f}",
                annotation_position="top right"
            )
            
            return {
                'title': TranslationSystem.t('chart_profit_dist'),
                'figure': fig
            }
        except:
            return None

# ==================== 4. وظائف المساعدة ====================

def load_multiple_files(uploaded_files):
    """تحميل عدة ملفات Excel/CSV"""
    dataframes = []
    file_info_list = []
    
    for uploaded_file in uploaded_files:
        try:
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.csv'):
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
            st.error(f"{TranslationSystem.t('upload_error')} {uploaded_file.name}: {str(e)}")
    
    return dataframes, file_info_list
def merge_dataframes(dataframes):
    """دمج عدة dataframes في dataframe واحد"""
    if dataframes is None or len(dataframes) == 0:
        return None
    
    try:
        merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
        return merged_df
    except Exception as e:
        st.error(f"خطأ في دمج الملفات: {str(e)}")
        return None
def load_css():
    """تحميل CSS مع دعم متعدد اللغات"""
    direction = TranslationSystem.get_language_direction()
    font_family = TranslationSystem.get_font_family()
    
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
        direction: {direction};
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
        direction: {direction};
    }}
    
    .file-card {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-family: {font_family};
        direction: {direction};
    }}
    
    .warning-box {{
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: {font_family};
        direction: {direction};
    }}
    
    .report-box {{
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        font-family: {font_family};
        direction: {direction};
        white-space: pre-wrap;
        font-size: 14px;
        line-height: 1.6;
        max-height: 500px;
        overflow-y: auto;
    }}
    
    .stApp {{
        font-family: {font_family};
        text-align: {direction};
    }}
    
    .stButton > button {{
        border-radius: 8px;
        font-family: {font_family};
    }}
    
    .stSelectbox, .stTextInput, .stNumberInput {{
        font-family: {font_family};
    }}
    </style>
    
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    """
    st.markdown(css, unsafe_allow_html=True)

# ==================== 5. تهيئة حالة الجلسة ====================

# إعدادات الصفحة
st.set_page_config(
    page_title=TranslationSystem.t('dashboard_title'),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
if 'text_report' not in st.session_state:
    st.session_state.text_report = ""

# وظائف تبديل اللغة والمظهر
def toggle_language():
    st.session_state.language = 'en' if st.session_state.language == 'ar' else 'ar'
    st.rerun()

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# تحميل CSS
load_css()

# ==================== 6. الشريط الجانبي ====================

with st.sidebar:
    st.markdown(f"### {TranslationSystem.t('sidebar_settings')}")
    
    # تبديل اللغة
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{TranslationSystem.t('language')}**")
    with col2:
        current_lang = "العربية" if st.session_state.language == 'en' else "English"
        if st.button(f"🌐 {current_lang}", use_container_width=True):
            toggle_language()
    
    # تبديل المظهر
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{TranslationSystem.t('theme')}**")
    with col2:
        current_theme = TranslationSystem.t('dark_theme') if st.session_state.theme == 'light' else TranslationSystem.t('light_theme')
        if st.button(current_theme, use_container_width=True):
            toggle_theme()
    
    st.divider()
    
    # تحميل الإعدادات السابقة
    if st.button(TranslationSystem.t('load_settings'), use_container_width=True, icon="📥"):
        if os.path.exists('sales_config.json'):
            with open('sales_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                st.session_state.column_mapping = config.get('column_mapping', {})
                st.session_state.language = config.get('language', 'ar')
                st.session_state.theme = config.get('theme', 'light')
                st.success(TranslationSystem.t('settings_loaded'))
                st.rerun()
        else:
            st.warning(TranslationSystem.t('no_settings'))
    
    # حفظ الإعدادات
    if st.session_state.column_mapping:
        if st.button(TranslationSystem.t('save_settings'), use_container_width=True, icon="💾"):
            config = {
                'column_mapping': st.session_state.column_mapping,
                'saved_at': datetime.now().isoformat(),
                'language': st.session_state.language,
                'theme': st.session_state.theme
            }
            with open('sales_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            st.success(TranslationSystem.t('settings_saved'))
    
    # إعادة التعيين
    if st.button(TranslationSystem.t('reset'), use_container_width=True, icon="🔄"):
        for key in list(st.session_state.keys()):
            if key not in ['language', 'theme']:
                del st.session_state[key]
        st.rerun()

# ==================== 7. العنوان الرئيسي ====================

st.markdown(f"""
<div class="main-header">
    <h1>{TranslationSystem.t('dashboard_title')}</h1>
    <p>{TranslationSystem.t('dashboard_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ==================== 8. تحميل الملفات المتعددة ====================

st.markdown(f"## 📤 {TranslationSystem.t('step_1')}")

uploaded_files = st.file_uploader(
    TranslationSystem.t('upload_hint'),
    type=['xlsx', 'xls', 'csv'],
    help=TranslationSystem.t('upload_supported'),
    accept_multiple_files=True,
    key="sales_file_uploader"
)

if uploaded_files and len(uploaded_files) > 0:
    try:
        with st.spinner(TranslationSystem.t('loading')):
            dataframes, file_info_list = load_multiple_files(uploaded_files)
        
        if dataframes and file_info_list:
            st.session_state.dataframes = dataframes
            st.session_state.file_info_list = file_info_list
            st.session_state.files_uploaded = True
            
            st.success(TranslationSystem.t('upload_success', count=len(dataframes)))
            
            # عرض معلومات الملفات
            st.markdown(f"### 📁 {TranslationSystem.t('file_info')}")
            
            for i, file_info in enumerate(file_info_list):
                with st.expander(f"{file_info['name']} ({file_info['rows']} {TranslationSystem.t('rows')}, {file_info['columns']} {TranslationSystem.t('columns')})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(TranslationSystem.t('file_size'), f"{file_info['size']:,} bytes")
                    with col2:
                        st.metric(TranslationSystem.t('rows'), file_info['rows'])
                    with col3:
                        st.metric(TranslationSystem.t('columns'), file_info['columns'])
                    
                    if st.checkbox(f"{TranslationSystem.t('preview')} {i+1}", key=f"preview_{i}"):
                        st.dataframe(file_info['dataframe'].head(), use_container_width=True)
            
            # خيارات دمج الملفات
            if len(dataframes) > 1:
                st.markdown("### 🔗 خيارات الدمج")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(TranslationSystem.t('merge_files'), use_container_width=True, icon="🔗"):
                        merged_df = merge_dataframes(dataframes)
                        if merged_df is not None:
                            st.session_state.merged_df = merged_df
                            st.session_state.use_merged = True
                            st.session_state.current_df = merged_df
                            st.success(TranslationSystem.t('merged_success'))
                
                with col2:
                    if st.button(TranslationSystem.t('use_single'), use_container_width=True, icon="📄"):
                        st.session_state.use_merged = False
                        st.session_state.current_df = dataframes[0]
                        st.info(f"📄 {TranslationSystem.t('individual_file')}")
            
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
                st.info(f"📊 **{TranslationSystem.t('merged_data')}**: {len(df_to_use)} {TranslationSystem.t('rows')}, {len(df_to_use.columns)} {TranslationSystem.t('columns')}")
            else:
                st.info(f"📊 **{TranslationSystem.t('individual_file')}**: {len(df_to_use)} {TranslationSystem.t('rows')}, {len(df_to_use.columns)} {TranslationSystem.t('columns')}")
            
            # عرض عينة من البيانات
            with st.expander(f"{TranslationSystem.t('preview')} ({TranslationSystem.t('preview_rows')})"):
                st.dataframe(df_to_use.head(), use_container_width=True)
            
            # عرض معلومات البيانات
            st.markdown(f"### 📈 {TranslationSystem.t('statistics')}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(TranslationSystem.t('total_files'), len(dataframes))
            with col2:
                st.metric(TranslationSystem.t('total_records'), len(df_to_use))
            with col3:
                st.metric(TranslationSystem.t('total_columns'), len(df_to_use.columns))
            with col4:
                numeric_cols = df_to_use.select_dtypes(include=[np.number]).columns.tolist()
                st.metric(TranslationSystem.t('numeric_columns'), len(numeric_cols))
        
    except Exception as e:
        st.error(f"{TranslationSystem.t('upload_error')} {str(e)}")

# ==================== 9. تعيين أعمدة المبيعات ====================

if st.session_state.files_uploaded and st.session_state.current_df is not None:
    st.markdown(f"## 🎯 {TranslationSystem.t('step_2')}")
    
    df = st.session_state.current_df
    columns = df.columns.tolist()
    
    # التعرف التلقائي على الأعمدة
    mapper = SalesAutoColumnMapper(df)
    auto_suggestions = mapper.auto_detect_columns()
    
    st.markdown(f"**{TranslationSystem.t('auto_detection')}**")
    st.info(TranslationSystem.t('auto_detection_desc'))
    
    # إنشاء تخطيط تعيين الأعمدة
    column_mapping = {}
    
    # عرض تعيين الأعمدة لكل فئة
    categories = {
        TranslationSystem.t('category_order'): ["order_id", "order_date", "status"],
        TranslationSystem.t('category_customer'): ["customer_name", "customer_id"],
        TranslationSystem.t('category_product'): ["product_name", "product_id", "category"],
        TranslationSystem.t('category_financial'): ["quantity", "price", "total_amount", "discount", "profit"],
        TranslationSystem.t('category_location'): ["region", "city", "country"],
        TranslationSystem.t('category_sales'): ["salesperson", "payment_method"]
    }
    
    for category, fields in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(3)
        for idx, field in enumerate(fields):
            with cols[idx % 3]:
                field_display = TranslationSystem.t(f'field_{field}')
                suggested_column = auto_suggestions.get(field, TranslationSystem.t('not_available'))
                
                options = [f"❌ {TranslationSystem.t('not_available')}"] + columns
                default_idx = 0
                if suggested_column in columns:
                    default_idx = columns.index(suggested_column) + 1
                
                selected = st.selectbox(
                    f"**{field_display}**",
                    options=options,
                    index=default_idx,
                    key=f"sales_map_{field}"
                )
                
                if selected != f"❌ {TranslationSystem.t('not_available')}":
                    column_mapping[field] = selected
    
    st.session_state.column_mapping = column_mapping
    
    # زر للمتابعة للتحليل
    if st.button(TranslationSystem.t('analyze_button'), type="primary", use_container_width=True, icon="🚀"):
        st.session_state.analysis_ready = True
        st.rerun()

# ==================== 10. التحليل الذكي للمبيعات ====================

if st.session_state.get('analysis_ready', False):
    st.markdown(f"## 📊 {TranslationSystem.t('step_3')}")
    
    analyzer = SalesDataAnalyzer(
        st.session_state.current_df, 
        st.session_state.column_mapping
    )
    
    # التحليل الذكي للبيانات
    with st.spinner(TranslationSystem.t('loading_analysis')):
        analysis = analyzer.analyze_all()
    
    st.session_state.analysis_results = analysis
    
    # عرض النتائج الرئيسية
    st.markdown(f"### 📈 {TranslationSystem.t('kpis_title')}")
    
    # بطاقات KPIs
    kpis = analysis.get('kpis', {})
    if kpis:
        kpi_keys = list(kpis.keys())
        
        # عرض KPIs في أعمدة
        cols_per_row = 4
        for i in range(0, len(kpi_keys), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(kpi_keys):
                    kpi_key = kpi_keys[i + j]
                    with cols[j]:
                        kpi_info = kpis[kpi_key]
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div style="font-size: 2rem; margin-bottom: 10px;">
                                {kpi_info.get('icon', '📊')}
                            </div>
                            <div style="font-size: 1.8rem; font-weight: bold; color: #4F46E5;">
                                {kpi_info['formatted']}
                            </div>
                            <div style="color: #6B7280; font-size: 0.9rem;">
                                {kpi_info['label']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # الرسوم البيانية الذكية
    st.markdown(f"### 📊 {TranslationSystem.t('charts_title')}")
    
    visualizer = SalesVisualizer(
        st.session_state.current_df,
        st.session_state.column_mapping,
        analysis
    )
    
    # عرض الرسوم حسب توفر البيانات
    charts = visualizer.generate_all_charts()
    
    if charts:
        for i in range(0, len(charts), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(charts):
                    chart_info = charts[i + j]
                    with cols[j]:
                        st.markdown(f"#### {chart_info['title']}")
                        st.plotly_chart(chart_info['figure'], use_container_width=True)
    else:
        st.warning(TranslationSystem.t('no_charts_data'))
    
    # التقرير النصي
    st.markdown(f"### 📄 {TranslationSystem.t('report_title')}")
    
    # زر إنشاء التقرير
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(TranslationSystem.t('generate_report'), use_container_width=True, icon="📋"):
            st.session_state.text_report = analyzer.generate_text_report(analysis)
    
    # عرض التقرير إذا كان موجوداً
    if st.session_state.text_report:
        st.markdown(f"#### {TranslationSystem.t('executive_summary')}")
        
        # صندوق عرض التقرير
        st.markdown(f'<div class="report-box">{st.session_state.text_report}</div>', unsafe_allow_html=True)
        
        # أزرار النسخ
        col1, col2 = st.columns(2)
        with col1:
            if st.button(TranslationSystem.t('copy_report'), use_container_width=True, icon="📋"):
                try:
                    pyperclip.copy(st.session_state.text_report)
                    st.success(TranslationSystem.t('report_copied'))
                except:
                    st.warning("⚠️ تعذر النسخ. يرجى نسخ النص يدوياً.")
        
        with col2:
            # خيار التصدير كملف نصي
            txt_file = st.session_state.text_report.encode('utf-8')
            st.download_button(
                label="📥 تحميل كملف نصي",
                data=txt_file,
                file_name=f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # تحليل إضافي
    with st.expander(TranslationSystem.t('advanced_analysis')):
        st.markdown(f"### 🔍 {TranslationSystem.t('advanced_analysis')}")
        
        # تحليل العلاقات
        numeric_cols = []
        for col in st.session_state.current_df.columns:
            if pd.api.types.is_numeric_dtype(st.session_state.current_df[col]):
                numeric_cols.append(col)
        
        if len(numeric_cols) >= 2:
            st.markdown(f"#### {TranslationSystem.t('correlation_matrix')}")
            
            numeric_df = st.session_state.current_df[numeric_cols]
            corr_matrix = numeric_df.corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu',
                aspect="auto",
                title=TranslationSystem.t('correlation_matrix')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # اكتشاف القيم الشاذة
        st.markdown(f"#### {TranslationSystem.t('outlier_detection')}")
        if 'total_amount' in st.session_state.column_mapping:
            price_col = st.session_state.column_mapping['total_amount']
            if price_col in st.session_state.current_df.columns:
                try:
                    price_data = st.session_state.current_df[price_col].dropna()
                    
                    if len(price_data) > 0:
                        mean_price = price_data.mean()
                        std_price = price_data.std()
                        
                        if std_price > 0:
                            z_scores = np.abs((price_data - mean_price) / std_price)
                            outliers_mask = z_scores > 3
                            outliers = st.session_state.current_df.loc[price_data.index[outliers_mask]]
                            
                            if len(outliers) > 0:
                                st.warning(TranslationSystem.t('outliers_found', count=len(outliers)))
                                st.dataframe(outliers.head(), use_container_width=True)
                            else:
                                st.success(TranslationSystem.t('no_outliers'))
                        else:
                            st.info(TranslationSystem.t('zero_std'))
                except Exception as e:
                    st.error(f"{TranslationSystem.t('error')}: {str(e)}")

# ==================== 11. رسالة الترحيب ====================

if not st.session_state.files_uploaded:
    st.info("""
    📋 **إرشادات الاستخدام:**
    
    1. **رفع الملفات**: قم برفع ملفات Excel أو CSV تحتوي على بيانات المبيعات
    2. **تعيين الأعمدة**: سيقوم النظام بالتعرف التلقائي على أعمدة البيانات
    3. **التحليل**: انتقل إلى التحليل للحصول على نتائج ورسوم بيانية
    4. **التقرير**: إنشاء تقرير نصي يمكن نسخه أو تحميله
    
    💡 **نصائح**:
    - يمكنك رفع ملفات متعددة ودمجها
    - تحقق من تعيين الأعمدة قبل التحليل
    - استخدم زر حفظ الإعدادات لحفظ التكوين
    """)

# ==================== 12. تذييل الصفحة ====================

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>📊 نظام تحليل المبيعات الذكي | الإصدار 2.0 | يدعم العربية والإنجليزية</p>
    </div>
    """, unsafe_allow_html=True)